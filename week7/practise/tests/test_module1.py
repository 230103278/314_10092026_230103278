import numpy as np
import pytest

from lab_kernels.module1_execution_model import (
    matrix_add_2d, matrix_transpose_naive, rgb_to_grayscale, vector_add_1d,
    vector_lerp, vector_scale_grid_stride, vector_threshold, volume_init_3d,
)

rng = np.random.default_rng(0)


@pytest.mark.parametrize("n", [1, 255, 256, 1024, 1000003])
def test_vector_add_1d(n):
    a, b = rng.random(n, dtype=np.float32), rng.random(n, dtype=np.float32)
    out = np.zeros(n, np.float32)
    vector_add_1d(a, b, out)
    np.testing.assert_allclose(out, a + b, atol=1e-5)


def test_vector_scale_grid_stride():
    n = 10**7  # far more elements than the 64*256 launched threads
    x = rng.random(n, dtype=np.float32)
    out = np.zeros(n, np.float32)
    vector_scale_grid_stride(x, np.float32(2.5), out)
    np.testing.assert_allclose(out, x * np.float32(2.5), atol=1e-5)


def test_matrix_add_2d():
    A, B = rng.random((513, 1021), dtype=np.float32), rng.random((513, 1021), dtype=np.float32)
    C = np.zeros_like(A)
    matrix_add_2d(A, B, C)
    np.testing.assert_allclose(C, A + B, atol=1e-5)


def test_matrix_transpose_naive():
    A = rng.random((300, 77), dtype=np.float32)
    B = np.zeros((77, 300), np.float32)
    matrix_transpose_naive(A, B)
    np.testing.assert_allclose(B, A.T, atol=1e-5)


def test_volume_init_3d():
    D, H, W = 33, 47, 65
    vol = np.zeros((D, H, W), np.int32)
    volume_init_3d(vol, D, H, W)
    z, y, x = np.indices((D, H, W))
    np.testing.assert_equal(vol, z * 10000 + y * 100 + x)


@pytest.mark.parametrize("dtype", [np.uint8, np.float32])
def test_rgb_to_grayscale(dtype):
    img = (rng.random((123, 457, 3)) * 255).astype(dtype)
    gray = np.zeros((123, 457), np.float32)
    rgb_to_grayscale(img, gray)
    R, G, B = (img[..., c].astype(np.float64) for c in range(3))
    np.testing.assert_allclose(gray, 0.299 * R + 0.587 * G + 0.114 * B, atol=1e-4)


def test_vector_lerp():
    n = 100001
    a, b, t = (rng.random(n, dtype=np.float32) for _ in range(3))
    out = np.zeros(n, np.float32)
    vector_lerp(a, b, t, out)
    np.testing.assert_allclose(out, (1 - t) * a + t * b, atol=1e-5)


def test_vector_threshold():
    x = rng.random(1000003, dtype=np.float32)
    mask = np.zeros(x.size, np.uint8)
    vector_threshold(x, np.float32(0.5), mask)
    np.testing.assert_equal(mask, (x >= 0.5).astype(np.uint8))
