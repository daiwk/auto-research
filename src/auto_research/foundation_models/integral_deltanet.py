"""Integral DeltaNet v1: CPU recurrent/chunk reference, not FLA or LM training."""
from __future__ import annotations

import torch
from torch import nn

REQUIRES_GPU_VALIDATION = False


def _cpu(x):
    if not isinstance(x,torch.Tensor) or x.device.type!='cpu' or not x.is_floating_point() or not torch.isfinite(x).all():
        raise ValueError('finite floating CPU tensors required')


def _inputs(q,k,v,alpha,erase,write,integration,readout):
    arrays=(q,k,v,alpha,erase,write,integration,readout)
    for x in arrays:_cpu(x)
    if q.ndim!=2 or min(q.shape)<1 or k.shape!=q.shape or v.ndim!=2 or min(v.shape)<1 or len(v)!=len(q):
        raise ValueError('aligned [time,key/value channels] inputs required')
    if any(x.dtype!=q.dtype for x in arrays):raise ValueError('one common dtype required')
    if any(x.shape!=q.shape for x in (alpha,erase,integration,readout)) or write.shape!=v.shape:
        raise ValueError('channel gates must align with key/value widths')
    if any(((x<0)|(x>1)).any() for x in (alpha,erase,write,integration,readout)):
        raise ValueError('gates must lie in [0,1]')


def _initial(q,v,states):
    shape=(v.shape[1],q.shape[1])
    if states is None:return q.new_zeros(shape),q.new_zeros(shape)
    if len(states)!=2:raise ValueError('delta and integral state required')
    for x in states:
        _cpu(x)
        if x.shape!=shape or x.dtype!=q.dtype:raise ValueError('state shape/dtype mismatch')
    return states


def recurrent(q,k,v,alpha,erase,write,integration,readout,*,states=None):
    """GDN-2 delta update, Eq6 integration and Eq7 channel-wise readout.

    KDA is included by broadcasting a scalar beta to erase and write channels.
    The integral state reads the UPDATED delta state and never feeds it back.
    """
    _inputs(q,k,v,alpha,erase,write,integration,readout)
    s,x=_initial(q,v,states)
    outputs=[]
    for t in range(len(q)):
        decayed=s*alpha[t]
        correction=write[t]*v[t]-decayed@(erase[t]*k[t])
        s=decayed+correction[:,None]*k[t][None,:]
        x=s*integration[t]+x*(1-integration[t])
        outputs.append(s@(readout[t]*q[t])+x@((1-readout[t])*q[t]))
    return torch.stack(outputs),(s,x)


def chunkwise(q,k,v,alpha,erase,write,integration,readout,*,chunk_size=4,states=None):
    """Section3.2 prefix-operator reference, with no fused-kernel speed claim.

    Explicit prefix matrices are deliberately materialized for small L1 checks.
    This is independent of recurrent() and handles final partial chunks.
    """
    _inputs(q,k,v,alpha,erase,write,integration,readout)
    if type(chunk_size)!=int or chunk_size<1:raise ValueError('positive chunk size required')
    s,x=_initial(q,v,states)
    outputs=[]
    dk=q.shape[1]
    for start in range(0,len(q),chunk_size):
        p=torch.eye(dk,dtype=q.dtype)
        h=torch.zeros_like(s)
        pbar=torch.zeros_like(p); hbar=torch.zeros_like(h); retention=q.new_ones(dk)
        local=[]
        for t in range(start,min(start+chunk_size,len(q))):
            a=torch.diag(alpha[t])@(torch.eye(dk,dtype=q.dtype)-(erase[t]*k[t])[:,None]*k[t][None,:])
            b=(write[t]*v[t])[:,None]*k[t][None,:]
            p=p@a; h=h@a+b
            lam=integration[t]
            pbar=p*lam+pbar*(1-lam)
            hbar=h*lam+hbar*(1-lam)
            retention=retention*(1-lam)
            qs=p@(readout[t]*q[t])+pbar@((1-readout[t])*q[t])
            qx=retention*(1-readout[t])*q[t]
            z=h@(readout[t]*q[t])+hbar@((1-readout[t])*q[t])
            local.append(s@qs+x@qx+z)
        outputs.extend(local)
        next_s=s@p+h
        x=s@pbar+x*retention+hbar
        s=next_s
    return torch.stack(outputs),(s,x)


class IntegralGates(nn.Module):
    """Low-rank learned gamma/lambda parameterization from normalized hidden states."""
    def __init__(self,hidden,key_width,rank=2):
        super().__init__()
        if any(type(n)!=int or n<1 for n in (hidden,key_width,rank)):raise ValueError('positive widths required')
        self.gamma_down=nn.Linear(hidden,rank,bias=False)
        self.gamma_up=nn.Linear(rank,key_width,bias=True)
        self.lambda_down=nn.Linear(hidden,rank,bias=False)
        self.lambda_up=nn.Linear(rank,key_width,bias=True)
        # exp(-softplus(z))=sigmoid(-z), lambda=1-gamma.
        nn.init.zeros_(self.gamma_up.weight);nn.init.zeros_(self.lambda_up.weight)
        nn.init.constant_(self.gamma_up.bias,-torch.log(torch.tensor(1023.)).item())
        nn.init.constant_(self.lambda_up.bias,-torch.log(torch.tensor(1023.)).item())

    def forward(self,normalized_hidden):
        _cpu(normalized_hidden)
        if any(p.device.type!='cpu' for p in self.parameters()):raise ValueError('CPU-only gates')
        gamma=torch.sigmoid(-self.gamma_up(self.gamma_down(normalized_hidden)))
        lam=torch.sigmoid(self.lambda_up(self.lambda_down(normalized_hidden)))
        return lam,gamma


def diagnostic(seed:int,device='cpu'):
    if type(seed)!=int or seed<0 or device!='cpu':raise ValueError('nonnegative seed and CPU-only device required')
    with torch.random.fork_rng():
        torch.manual_seed(seed)
        q=torch.randn(11,4,dtype=torch.float64)
        k=torch.nn.functional.normalize(torch.randn_like(q),dim=-1)
        v=torch.randn(11,3,dtype=torch.float64)
        gates=[torch.rand_like(q) for _ in range(4)]
        alpha,erase,lam,gamma=gates
        write=torch.rand_like(v)
        args=[q,k,v,alpha,erase,write,lam,gamma]
        r,rs=recurrent(*args)
        c,cs=chunkwise(*args,chunk_size=4)
        output_error=float((r-c).abs().max())
        state_error=float(max((a-b).abs().max() for a,b in zip(rs,cs)))
        train_args=[a.detach().clone().requires_grad_() for a in args]
        rr,_=recurrent(*train_args);gr=torch.autograd.grad(rr.square().sum(),train_args)
        cc,_=chunkwise(*train_args,chunk_size=4);gc=torch.autograd.grad(cc.square().sum(),train_args)
        grad_error=float(max((a-b).abs().max() for a,b in zip(gr,gc)))
        model=IntegralGates(6,4).double()
        hidden=torch.nn.functional.layer_norm(torch.randn(11,6,dtype=torch.float64),(6,))
        il,ig=model(hidden)
        init_error=float(max((il-1/1024).detach().abs().max(),((1-ig)-1/1024).detach().abs().max()))
        learn,_=recurrent(q,k,v,alpha,erase,write,il,ig)
        learn.square().sum().backward()
        gate_grad=float(model.lambda_up.bias.grad.norm()+model.gamma_up.bias.grad.norm())
        # Integration follows S AFTER its current write: lambda=1 makes X=S.
        one=torch.ones_like(q)
        no,_=recurrent(q,k,v,alpha,erase,write,one,torch.zeros_like(q))
        fast,_=recurrent(q,k,v,alpha,erase,write,one,one)
    return {'seed':seed,'device':device,'evaluation_tier':'l1_mechanism','diagnostic_only':True,
            'checks':{'chunk_matches_recurrence':output_error<1e-11,'both_states_match':state_error<1e-11,
                      'chunk_gradients_match':grad_error<1e-10,'learned_gate_gradients':gate_grad>0,
                      'small_integral_initialization':init_error<1e-9,'integration_uses_current_delta':bool(torch.allclose(no,fast,atol=1e-12))},
            'metrics':{'output_max_abs_error':output_error,'state_max_abs_error':state_error,
                       'gradient_max_abs_error':grad_error,'gate_initialization_max_abs_error':init_error,'gate_bias_gradient_norm':gate_grad}}
