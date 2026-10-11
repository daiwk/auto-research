"""Optional CUDA-only implementation, imported only by the sparse runtime."""
import triton
import triton.language as tl
from triton.language.extra.cuda import libdevice


@triton.jit
def spmv(W, Bits, X, Y, ROWS: tl.constexpr, WORDS: tl.constexpr, BLOCK: tl.constexpr):
    rows = tl.program_id(0) * 4 + tl.arange(0, 4)
    blocks = tl.arange(0, BLOCK)
    valid = (rows[:, None] < ROWS) & (blocks[None, :] < WORDS)
    mask = tl.load(Bits + rows[:, None] * WORDS + blocks[None, :], valid, other=0).to(tl.uint32)
    acc = tl.full((4, BLOCK), 0, tl.float32)
    for rank in tl.static_range(16):
        column = libdevice.ffs(mask.to(tl.int32)) - 1
        x = tl.load(X + blocks[None, :] * 32 + column, valid, other=0).to(tl.float32)
        w = tl.load(W + (rows[:, None] * WORDS + blocks[None, :]) * 16 + rank, valid, other=0).to(tl.float32)
        acc += x * w
        mask = mask & (mask - 1)
    tl.store(Y + rows, tl.sum(acc, 1), rows < ROWS)
