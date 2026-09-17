import multiprocessing as mp
import random
import time

TOTAL_ITERATIONS = 100_000_000


def reduction_worker(chunk_size):
    local_hits = 0
    for _ in range(chunk_size):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            local_hits += 1
    return local_hits


def benchmark_reduction(num_workers):
    chunk_size = TOTAL_ITERATIONS // num_workers
    tasks = [chunk_size] * num_workers

    start = time.perf_counter()
    with mp.Pool(processes=num_workers) as pool:
        results = pool.map(reduction_worker, tasks)
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    total_hits = sum(results)
    pi_val = 4.0 * total_hits / TOTAL_ITERATIONS
    return elapsed_ms, pi_val


if __name__ == "__main__":
    thread_counts = [1, 2, 4, 8, 16, 32]
    runtimes = {}

    print(f"Benchmarking {TOTAL_ITERATIONS:,} Iterations...")
    for t in thread_counts:
        t_ms, pi_approx = benchmark_reduction(t)
        runtimes[t] = t_ms
        speedup = runtimes[1] / t_ms
        efficiency = (speedup / t) * 100.0
        print(
            f"T={t:2d} | Runtime: {t_ms:8.2f} ms | Speedup: {speedup:5.2f}x | Efficiency: {efficiency:5.1f}%"
        )
