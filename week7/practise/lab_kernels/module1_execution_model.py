#Module 1: CUDA Execution Model Tasks 1-8
from numba import cuda


# Task 01: 1D Vector Addition with Boundary Checks
@cuda.jit
def _vector_add_1d_kernel(a, b, out):
    i = cuda.grid(1)
    if i < out.size:
        out[i] = a[i] + b[i]


def vector_add_1d(a, b, out):
    n = out.size
    _vector_add_1d_kernel[(n + 255) // 256, 256](a, b, out)


# Task 02: 1D Grid-Stride Loop Element-wise Scaling
@cuda.jit
def _vector_scale_grid_stride_kernel(x, alpha, out):
    start = cuda.grid(1)
    stride = cuda.gridsize(1)  # gridDim.x * blockDim.x
    for i in range(start, out.size, stride):
        out[i] = x[i] * alpha


def vector_scale_grid_stride(x, alpha, out):
    # Fixed launch size, independent of N
    _vector_scale_grid_stride_kernel[64, 256](x, alpha, out)


# Task 03: 2D Matrix Element-wise Addition & Index Mapping
@cuda.jit
def _matrix_add_2d_kernel(A, B, C):
    row = cuda.blockIdx.y * cuda.blockDim.y + cuda.threadIdx.y
    col = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
    if row < C.shape[0] and col < C.shape[1]:
        C[row, col] = A[row, col] + B[row, col]


def matrix_add_2d(A, B, C):
    M, N = C.shape
    _matrix_add_2d_kernel[((N + 15) // 16, (M + 15) // 16), (16, 16)](A, B, C)


# Task 04: 2D Matrix Transpose (Naive Global Memory)
@cuda.jit
def _matrix_transpose_naive_kernel(A, B):
    col, row = cuda.grid(2)
    if row < A.shape[0] and col < A.shape[1]:
        B[col, row] = A[row, col]  # coalesced read, strided write


def matrix_transpose_naive(A, B):
    M, N = A.shape
    _matrix_transpose_naive_kernel[((N + 15) // 16, (M + 15) // 16), (16, 16)](A, B)


# Task 05: 3D Grid Volume Initialization & Index Flattening
@cuda.jit
def _volume_init_3d_kernel(flat, D, H, W):
    x, y, z = cuda.grid(3)
    if x < W and y < H and z < D:
        flat[z * H * W + y * W + x] = z * 10000 + y * 100 + x


def volume_init_3d(vol, D, H, W):
    # Writes through a flat 1D view to exercise the row-major flattening formula
    flat = vol.reshape(-1)
    _volume_init_3d_kernel[((W + 7) // 8, (H + 7) // 8, (D + 7) // 8), (8, 8, 8)](flat, D, H, W)


# Task 06: Color Image to Grayscale Luminance Conversion (ITU-R BT.601)
@cuda.jit
def _rgb_to_grayscale_kernel(img_rgb, img_gray):
    x, y = cuda.grid(2)
    if y < img_gray.shape[0] and x < img_gray.shape[1]:
        img_gray[y, x] = 0.299 * img_rgb[y, x, 0] + 0.587 * img_rgb[y, x, 1] + 0.114 * img_rgb[y, x, 2]


def rgb_to_grayscale(img_rgb, img_gray):
    H, W = img_gray.shape
    _rgb_to_grayscale_kernel[((W + 15) // 16, (H + 15) // 16), (16, 16)](img_rgb, img_gray)


# Task 07: Vector Linear Interpolation (LERP)
@cuda.jit
def _vector_lerp_kernel(a, b, t, out):
    i = cuda.grid(1)
    if i < out.size:
        out[i] = (1.0 - t[i]) * a[i] + t[i] * b[i]  # NVVM contracts this into FMAs


def vector_lerp(a, b, t, out):
    n = out.size
    _vector_lerp_kernel[(n + 255) // 256, 256](a, b, t, out)


# Task 08: Thresholding & Boolean Mask Generation
@cuda.jit
def _vector_threshold_kernel(x, thresh, mask):
    start = cuda.grid(1)
    stride = cuda.gridsize(1)
    for i in range(start, mask.size, stride):
        mask[i] = x[i] >= thresh  # predicated store, no branch


def vector_threshold(x, thresh, mask):
    _vector_threshold_kernel[64, 256](x, thresh, mask)
