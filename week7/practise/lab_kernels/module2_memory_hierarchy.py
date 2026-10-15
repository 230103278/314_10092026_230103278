#Module 2: Memory Hierarchy & Shared Memory (Tasks 9-10).
from numba import cuda, float32

BLOCK_SIZE = 256


# Task 09: Coalesced vs Strided Memory Access Benchmark
@cuda.jit
def _strided_copy_kernel(in_arr, out_arr, stride):
    # stride == 1: neighbouring threads read neighbouring words (coalesced).
    # stride > 1: each thread hits a different memory segment.
    i = cuda.grid(1)
    if i < out_arr.size:
        out_arr[i] = in_arr[i * stride]


def benchmark_strided_access(in_arr, out_arr, stride, repeats=10):
    """out_arr[i] = in_arr[i * stride]. Returns effective bandwidth in GB/s."""
    n = out_arr.size
    assert in_arr.size >= (n - 1) * stride + 1, "in_arr too small for this stride"
    d_in = cuda.to_device(in_arr)
    d_out = cuda.device_array_like(out_arr)
    grid = (n + BLOCK_SIZE - 1) // BLOCK_SIZE

    _strided_copy_kernel[grid, BLOCK_SIZE](d_in, d_out, stride)  # warm-up / JIT
    start, end = cuda.event(), cuda.event()
    start.record()
    for _ in range(repeats):
        _strided_copy_kernel[grid, BLOCK_SIZE](d_in, d_out, stride)
    end.record()
    end.synchronize()
    ms = cuda.event_elapsed_time(start, end) / repeats

    d_out.copy_to_host(out_arr)
    bytes_moved = 2 * n * out_arr.itemsize  # one read + one write per element
    return bytes_moved / (ms * 1e-3) / 1e9


# Task 10: 1D Stencil / Moving Average with shared-memory halo
@cuda.jit
def _stencil_1d_kernel(in_arr, out_arr, radius):
    tile = cuda.shared.array(0, float32)  # dynamic: BLOCK_SIZE + 2*radius floats
    n = in_arr.size
    tx = cuda.threadIdx.x
    block_start = cuda.blockIdx.x * cuda.blockDim.x
    i = block_start + tx

    # Cooperative load of center + halos, clamping indices to [0, n-1]
    for s in range(tx, cuda.blockDim.x + 2 * radius, cuda.blockDim.x):
        g = min(max(block_start + s - radius, 0), n - 1)
        tile[s] = in_arr[g]
    cuda.syncthreads()

    if i < n:
        acc = float32(0.0)
        for k in range(2 * radius + 1):
            acc += tile[tx + k]
        out_arr[i] = acc / (2 * radius + 1)


def stencil_1d_shared(in_arr, out_arr, radius):
    n = out_arr.size
    shared_bytes = (BLOCK_SIZE + 2 * radius) * 4
    _stencil_1d_kernel[(n + BLOCK_SIZE - 1) // BLOCK_SIZE, BLOCK_SIZE, 0, shared_bytes](in_arr, out_arr, radius)
