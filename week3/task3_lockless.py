import threading
import time

TOTAL_OPS = 2_000_000
NUM_THREADS = 4

class LockedCounter:
    def __init__(self):
        self.val = 0
        self.lock = threading.Lock()
    def inc(self):
        with self.lock:
            self.val += 1

def bench_locked():
    c = LockedCounter()
    ops_per_thread = TOTAL_OPS // NUM_THREADS
    def work():
        for _ in range(ops_per_thread):
            c.inc()
    threads = [threading.Thread(target=work) for _ in range(NUM_THREADS)]
    start = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    return c.val, time.perf_counter() - start

class LocklessAccumulator:
    """
    Lockless Thread-Local Accumulator using Map-Reduce Partitioning.
    Each thread increments its own private, thread-local register/accumulator,
    eliminating lock contention and shared memory cache line invalidation entirely.
    A final reduction step sums the thread-local results after thread join.
    """
    def __init__(self, num_threads=4):
        self.num_threads = num_threads
        self.buffers = [0] * num_threads

    def worker(self, thread_idx, ops):
        local_val = 0
        for _ in range(ops):
            local_val += 1
        self.buffers[thread_idx] = local_val

    def run(self, total_ops=2_000_000):
        ops_per_thread = total_ops // self.num_threads
        threads = [
            threading.Thread(target=self.worker, args=(i, ops_per_thread))
            for i in range(self.num_threads)
        ]
        start = time.perf_counter()
        for t in threads: t.start()
        for t in threads: t.join()
        
        # Reduction stage (O(num_threads))
        total = sum(self.buffers)
        elapsed = time.perf_counter() - start
        return total, elapsed

if __name__ == "__main__":
    print("=== TASK 3: ARCHITECTURAL REDESIGN BENCHMARK ===")
    val_locked, t_locked = bench_locked()
    print(f"LockedCounter:     Value = {val_locked:,} | Time: {t_locked:.4f}s")
    
    lockless = LocklessAccumulator(NUM_THREADS)
    val_lockless, t_lockless = lockless.run(TOTAL_OPS)
    print(f"LocklessCounter:   Value = {val_lockless:,} | Time: {t_lockless:.4f}s")
    
    speedup = t_locked / t_lockless
    print(f"Speedup Factor over LockedCounter: {speedup:.2f}x")
    assert val_lockless == TOTAL_OPS, "Correctness failed!"
    print(f"Deterministic Correctness Check: PASSED (Exact {TOTAL_OPS:,})")
