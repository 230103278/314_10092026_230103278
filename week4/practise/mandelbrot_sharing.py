# // --- Python 3: Mandelbrot Static Work-Sharing ---
import numpy as np
import time
from numba import njit, prange
WIDTH, HEIGHT = 1920, 1080
MAX_ITER = 1000
@njit
def compute_pixel(px, py, width, height, max_iter):
    x0 = (px - width / 2.0) * 4.0 / width
    y0 = (py - height / 2.0) * 4.0 / height
    x, y = 0.0, 0.0
    iteration = 0
    while x * x + y * y <= 4.0 and iteration < max_iter:
        xtemp = x * x - y * y + x0
        y = 2.0 * x * y + y0
        x = xtemp
        iteration += 1
    return iteration
# 1. Static Scheduling: Uniform row distribution
@njit(parallel=True)
def render_mandelbrot_static(width, height, max_iter):
    img = np.zeros((height, width), dtype=np.int32)
    for y in prange(height): # prange applies static chunking by default
        for x in range(width):
            img[y, x] = compute_pixel(x, y, width, height, max_iter)
    return img

if __name__ == "__main__":
    print(f"Rendering Mandelbrot ({WIDTH}x{HEIGHT}, Max Iter: {MAX_ITER})...")
# Warm-up
    _ = render_mandelbrot_static(100, 100, 100)
    t0 = time.perf_counter()
    image = render_mandelbrot_static(WIDTH, HEIGHT, MAX_ITER)
    t1 = time.perf_counter()
    print(f"Static Schedule Render Completed in: {t1 - t0:.4f} seconds")
