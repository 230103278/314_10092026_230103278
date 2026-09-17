import random
import threading
import time

BENCH_POINTS = 5_000_000
NUM_THREADS = 4
POINTS_PER_THREAD = BENCH_POINTS // NUM_THREADS

def run_single_threaded():
    hits = 0
    start = time.perf_counter()
    for _ in range(BENCH_POINTS):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            hits += 1
    elapsed = time.perf_counter() - start
    pi_val = 4.0 * hits / BENCH_POINTS
    return hits, pi_val, elapsed

sync_hits = 0
lock = threading.Lock()

def sync_worker():
    global sync_hits
    for _ in range(POINTS_PER_THREAD):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            with lock:
                sync_hits += 1

def run_synchronized():
    global sync_hits
    sync_hits = 0
    threads = [threading.Thread(target=sync_worker) for _ in range(NUM_THREADS)]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start
    pi_val = 4.0 * sync_hits / BENCH_POINTS
    return sync_hits, pi_val, elapsed

if __name__ == "__main__":
    _, pi_single, t_single = run_single_threaded()
    _, pi_sync, t_sync = run_synchronized()

    print(f"Single-Threaded:  Pi = {pi_single:.5f} | Time = {t_single:.3f}s")
    print(f"Synchronized (4T): Pi = {pi_sync:.5f} | Time = {t_sync:.3f}s")
    print(f"Slowdown Penalty: {t_sync / t_single:.2f}x")
