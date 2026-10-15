import numpy as np
import pytest

from lab_kernels.module2_memory_hierarchy import benchmark_strided_access, stencil_1d_shared

rng = np.random.default_rng(0)


def test_benchmark_strided_access():
    n = 1 << 22
    in_arr = rng.random(n * 32, dtype=np.float32)
    bw = {}
    for stride in [1, 2, 4, 8, 16, 32]:
        out = np.zeros(n, np.float32)
        bw[stride] = benchmark_strided_access(in_arr, out, stride)
        np.testing.assert_equal(out, in_arr[::stride][:n])
    print({s: f"{b:.1f} GB/s" for s, b in bw.items()})
    assert bw[1] > 2 * bw[32]


@pytest.mark.parametrize("n,radius", [(1, 3), (1000, 1), (100003, 3), (4096, 16)])
def test_stencil_1d_shared(n, radius):
    x = rng.random(n, dtype=np.float32)
    out = np.zeros(n, np.float32)
    stencil_1d_shared(x, out, radius)
    # Same as scipy.ndimage.uniform_filter1d(x, 2*radius+1, mode='nearest')
    ref = np.convolve(np.pad(x, radius, mode="edge"), np.ones(2 * radius + 1) / (2 * radius + 1), "valid")
    np.testing.assert_allclose(out, ref, atol=1e-4)
