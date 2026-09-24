import os
import statistics
import threading
import time

TEAM_SIZES = [1, 2, 4, 8, 16, 32, 64]
TRIALS = 20

def run_team(num_threads: int) -> set:
    barrier = threading.Barrier(num_threads)
    tids = set()

    def worker(thread_id: int):
        tids.add(threading.get_native_id())
        barrier.wait()

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return tids

if __name__ == "__main__":
    print(f"Logical CPUs: {os.cpu_count()} | Trials per P: {TRIALS}")
    run_team(4)
    print(f"{'P':>4} | {'OS threads':>10} | {'mean ms':>8} | {'stdev ms':>8} | {'min ms':>7} | {'max ms':>7} | {'us/thread':>9}")
    print("-" * 72)
    for p in TEAM_SIZES:
        times = []
        for _ in range(TRIALS):
            t0 = time.perf_counter()
            tids = run_team(p)
            times.append((time.perf_counter() - t0) * 1e3)
        mean = statistics.mean(times)
        print(f"{p:>4} | {len(tids):>10} | {mean:>8.3f} | {statistics.stdev(times):>8.3f} | "
              f"{min(times):>7.3f} | {max(times):>7.3f} | {mean * 1e3 / p:>9.1f}")
