import math
import os
import threading
import time
from numba import njit

N_SQRT = 10_000_000
NUMBA_REPEATS = 100
NUM_THREADS = os.cpu_count()

def sqrt_python(n: int) -> float:
    s = 0.0
    for i in range(n):
        s += math.sqrt(i + 1.0)
    return s

@njit(nogil=True)
def sqrt_numba(n, repeats):
    s = 0.0
    for r in range(repeats):
        for i in range(n):
            s += math.sqrt(i + 1.0 + r)
    return s

def read_cpu_times():
    stats = {}
    with open("/proc/stat") as f:
        for line in f:
            if line.startswith("cpu") and line[3].isdigit():
                name, *vals = line.split()
                vals = list(map(int, vals))
                idle = vals[3] + vals[4]
                stats[name] = (sum(vals) - idle, sum(vals))
    return stats

def run_team(target, args, num_threads: int):
    threads = [threading.Thread(target=target, args=args) for _ in range(num_threads)]
    before = read_cpu_times()
    t0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - t0
    after = read_cpu_times()
    usage = {}
    for cpu in before:
        busy = after[cpu][0] - before[cpu][0]
        total = after[cpu][1] - before[cpu][1]
        usage[cpu] = 100.0 * busy / total if total else 0.0
    return elapsed, usage

def report(label, elapsed, usage):
    print(f"\n=== {label} ===")
    print(f"Wall time: {elapsed:.2f} s")
    for cpu, pct in sorted(usage.items(), key=lambda kv: int(kv[0][3:])):
        print(f"  {cpu:>6}: {pct:5.1f}%  {'#' * int(pct / 5)}")
    avg = sum(usage.values()) / len(usage)
    print(f"  Average across {len(usage)} logical CPUs: {avg:.1f}%  "
          f"(~{avg * len(usage) / 100:.1f} cores busy)")

if __name__ == "__main__":
    print(f"Logical CPUs: {os.cpu_count()} | Threads: {NUM_THREADS} | sqrt per thread: {N_SQRT:,}")
    sqrt_numba(10, 1)

    elapsed, usage = run_team(sqrt_python, (N_SQRT,), 1)
    report("A0) Pure Python, 1 thread (baseline)", elapsed, usage)

    elapsed, usage = run_team(sqrt_python, (N_SQRT,), NUM_THREADS)
    report(f"A) Pure Python (GIL held), {NUM_THREADS} threads", elapsed, usage)

    elapsed, usage = run_team(sqrt_numba, (N_SQRT, NUMBA_REPEATS), 1)
    report(f"B0) Numba nogil, 1 thread, {NUMBA_REPEATS}x10M sqrt (baseline)", elapsed, usage)

    elapsed, usage = run_team(sqrt_numba, (N_SQRT, NUMBA_REPEATS), NUM_THREADS)
    report(f"B) Numba nogil, {NUM_THREADS} threads, {NUMBA_REPEATS}x10M sqrt each", elapsed, usage)
