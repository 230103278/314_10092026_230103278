import random
import threading
import time

TOTAL_POINTS = 50_000_000
NUM_THREADS = 4
POINTS_PER_THREAD = TOTAL_POINTS // NUM_THREADS

total_hits = 0


def worker():
    global total_hits
    for _ in range(POINTS_PER_THREAD):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            total_hits += 1


def run_phantom_experiment():
    global total_hits
    total_hits = 0
    threads = [
        threading.Thread(target=worker) for _ in range(NUM_THREADS)
    ]

    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start

    pi_approx = 4.0 * total_hits / TOTAL_POINTS
    return total_hits, pi_approx, elapsed


if __name__ == "__main__":
    for trial in range(1, 6):
        hits, pi_val, duration = run_phantom_experiment()
        print(
            f"Run {trial}: Hits = {hits:,} | Pi Approx = {pi_val:.5f} | Time = {duration:.2f}s"
        )
