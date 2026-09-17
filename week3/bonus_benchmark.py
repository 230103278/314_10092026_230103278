import time
from multiprocessing import Pool
import threading
import matplotlib.pyplot as plt

def cpu_work(n):
    # Pure CPU crunch
    count = 0
    for i in range(n):
        count += i * i
    return count

def run_threading(workers, total_work=50_000_000):
    n_per_worker = total_work // workers
    threads = []
    start = time.perf_counter()
    for _ in range(workers):
        t = threading.Thread(target=cpu_work, args=(n_per_worker,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start

def run_multiprocessing(workers, total_work=50_000_000):
    n_per_worker = total_work // workers
    start = time.perf_counter()
    with Pool(processes=workers) as pool:
        pool.map(cpu_work, [n_per_worker] * workers)
    return time.perf_counter() - start

if __name__ == "__main__":
    worker_counts = [1, 2, 4, 8, 16, 32]
    threading_times = []
    multiprocessing_times = []

    print("=== Bonus Benchmark: threading.Thread vs multiprocessing.Pool ===")
    print(f"Total work: 50,000,000 iterations\n")
    print(f"{'Workers':<10} | {'Threading Time (s)':<22} | {'Multiprocessing Time (s)':<25}")
    print("-" * 65)

    for w in worker_counts:
        t_thread = run_threading(w)
        t_proc = run_multiprocessing(w)
        threading_times.append(t_thread)
        multiprocessing_times.append(t_proc)
        print(f"{w:<10} | {t_thread:<22.4f} | {t_proc:<25.4f}")

    # Generate plot
    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(worker_counts, threading_times, 'ro-', linewidth=2, markersize=8, label='threading.Thread (GIL bound)')
    plt.plot(worker_counts, multiprocessing_times, 'bs-', linewidth=2, markersize=8, label='multiprocessing.Pool (True Parallelism)')
    plt.axvline(x=6, color='green', linestyle='--', label='Physical Cores (6 Cores)')
    plt.axvline(x=12, color='orange', linestyle=':', label='Logical SMT Threads (12 Threads)')
    plt.title('Bonus Task: Threading vs Multiprocessing Scaling (total_work=50M)', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Workers (T)', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.xticks(worker_counts)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('/home/duklet/CSS_314/week3/bonus_empirical_curve.png')
    print("\nSaved plot to /home/duklet/CSS_314/week3/bonus_empirical_curve.png")
