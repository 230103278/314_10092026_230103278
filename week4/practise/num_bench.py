# // --- Python 3: Numerical Integration Benchmarking ---
import numpy as np
import time
from numba import njit, prange
N_STEPS = 100_000_000
# 1. Serial Baseline
@njit
def calc_pi_serial(num_steps: int) -> float:
    step = 1.0 / num_steps
    total_sum = 0.0
    for i in range(num_steps):
        x = (i + 0.5) * step
        total_sum += 4.0 / (1.0 + x * x)
    return total_sum * step

# 2. Parallel Reduction (Numba compiles prange reduction into OpenMP-style tree reduction)
@njit(parallel=True)
def calc_pi_reduction(num_steps: int) -> float:
    step = 1.0 / num_steps
    total_sum = 0.0
    for i in prange(num_steps):
        x = (i + 0.5) * step
        total_sum += 4.0 / (1.0 + x * x) # Numba automatically infers parallel reduction
    return total_sum * step
if __name__ == "__main__":
# Warm-up JIT compilation
    _ = calc_pi_serial(1000)
    _ = calc_pi_reduction(1000)
# Benchmark Serial
    t0 = time.perf_counter()
    pi_serial = calc_pi_serial(N_STEPS)
    t1 = time.perf_counter()
    time_serial = t1 - t0
# Benchmark Parallel Reduction
    t2 = time.perf_counter()
    pi_parallel = calc_pi_reduction(N_STEPS)
    t3 = time.perf_counter()
    time_parallel = t3 - t2
    print(f"Serial: Pi = {pi_serial:.12f} | Time = {time_serial:.4f}s | Error ={abs(pi_serial - np.pi):.2e}")
    print(f"Parallel: Pi = {pi_parallel:.12f} | Time = {time_parallel:.4f}s | Error ={abs(pi_parallel - np.pi):.2e}")
    print(f"Observed Speedup: {time_serial / time_parallel:.2f}x")
