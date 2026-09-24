# // --- Python 3: Fork-Join Team Emulation ---
# Task 1.1: run the starter template 10 times and save stdout.
#   for i in $(seq 1 10); do echo "===== Run $i ====="; python fork_join.py; done > lab1_task1_1.txt
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import os
def worker_task(thread_id: int, team_size: int):
    # Retrieve OS-level native thread ID
    native_tid = threading.get_native_id()
    role = "Master" if thread_id == 0 else "Worker"
    # Demonstrate execution interleaving
    time.sleep(0.001 * (thread_id % 3))
    print(f"[{role}] Logical Rank: {thread_id} of {team_size} | Native OS TID: {native_tid}")

def run_team(num_threads: int):
    print(f"--- Forking a team of {num_threads} threads ---")
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker_task, tid, num_threads) for tid in range(num_threads)]
        for f in futures:
            f.result() # Wait for all threads (implicit barrier)
    print("--- Joined thread team. Execution returned to serial master ---\n")

if __name__ == "__main__":
    run_team(4)
