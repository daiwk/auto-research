"""Decoupled latent n-gram memory with GQA readout and zero sink."""

from __future__ import annotations


def _counterfactual_bits(logits):
    """Hard forward bits with a straight-through counterfactual surrogate."""
    hard = (logits > 0).to(logits.dtype)
    soft = logits.sigmoid()
    return hard + soft - soft.detach()


class LngramV2:
    """Factory-compatible wrapper returning the actual torch module."""

    def __new__(cls, width=64, routes=4, bits=3, memory_dim=16, orders=(1, 2), heads=4):
        import torch

        class Module(torch.nn.Module):
            def __init__(self):
                super().__init__()
                if routes % heads or width % heads:
                    raise ValueError("routes and width must be divisible by heads")
                self.width, self.routes, self.bits = width, routes, bits
                self.orders, self.heads, self.memory_dim = tuple(orders), heads, memory_dim
                self.norm = torch.nn.RMSNorm(width)
                self.route_projection = torch.nn.Linear(width, routes * bits, bias=False)
                alphabet = 2**bits
                self.memories = torch.nn.ParameterDict({
                    str(order): torch.nn.Parameter(torch.randn(routes, alphabet**order, memory_dim) * 0.02)
                    for order in orders
                })
                token_dim = len(orders) * memory_dim
                self.query = torch.nn.Linear(width, heads * memory_dim, bias=False)
                self.key = torch.nn.Linear(token_dim, heads * memory_dim, bias=False)
                self.value = torch.nn.Linear(token_dim, heads * memory_dim, bias=False)
                self.output = torch.nn.Linear(heads * memory_dim, width, bias=False)
                self.conv = torch.nn.Conv1d(width, width, 3, padding=2, groups=width)

            def addresses(self, hidden):
                logits = self.route_projection(self.norm(hidden)).view(*hidden.shape[:-1], routes, bits)
                bit_values = _counterfactual_bits(logits)
                powers = 2 ** torch.arange(bits, device=hidden.device, dtype=hidden.dtype)
                return (bit_values * powers).sum(-1), logits

            def forward(self, hidden, return_diagnostics=False):
                address_float, logits = self.addresses(hidden)
                address = address_float.detach().long()
                alphabet = 2**bits
                route_tokens=[]
                for route in range(routes):
                    retrieved=[]
                    for order in self.orders:
                        ids=torch.zeros_like(address[...,route])
                        for offset in range(order):
                            shifted=torch.roll(address[...,route],shifts=offset,dims=1)
                            if offset: shifted[:,:offset]=0
                            ids += shifted * (alphabet**(order-1-offset))
                        hard_memory = self.memories[str(order)][route, ids]
                        # Counterfactual lookup: keep the hard address in the
                        # forward pass, but backpropagate the value difference
                        # to the routing projection as if the lowest bit had
                        # flipped.  No soft mixture is used at inference.
                        alternative = self.memories[str(order)][route, ids ^ 1]
                        gate = logits[..., route, :].sigmoid().mean(-1, keepdim=True)
                        surrogate = gate * (alternative - hard_memory).detach()
                        retrieved.append(hard_memory + surrogate - surrogate.detach())
                    route_tokens.append(torch.cat(retrieved,dim=-1))
                tokens=torch.stack(route_tokens,dim=2)
                batch,length,_,_=tokens.shape
                q=self.query(self.norm(hidden)).view(batch,length,self.heads,self.memory_dim)
                k=self.key(tokens).view(batch,length,routes,self.heads,self.memory_dim)
                v=self.value(tokens).view(batch,length,routes,self.heads,self.memory_dim)
                sink=torch.zeros(batch,length,1,self.heads,self.memory_dim,device=hidden.device,dtype=hidden.dtype)
                k=torch.cat((k,sink),dim=2); v=torch.cat((v,sink),dim=2)
                scores=torch.einsum('blhd,blrhd->blhr',q,k)/(self.memory_dim**0.5)
                weights=torch.softmax(scores,dim=-1)
                readout=torch.einsum('blhr,blrhd->blhd',weights,v).reshape(batch,length,-1)
                residual=self.output(readout)
                convolved=self.conv(residual.transpose(1,2))[...,:length].transpose(1,2)
                output=hidden+convolved
                if return_diagnostics:
                    return output,{"route_ids":address,"sink_weight":weights[...,-1].mean(),"route_logits":logits,"activated_memory_parameters":routes*len(self.orders)*memory_dim}
                return output

        return Module()
