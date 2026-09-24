// Lab 4: Collatz stopping time, OpenMP scaling
// Build: gcc -O2 -fopenmp collatz.c -o collatz
// Usage: ./collatz seq | par <k> | fs_naive <k> | fs_pad <k>
// par uses schedule(runtime): set OMP_SCHEDULE, e.g. OMP_SCHEDULE="dynamic,100"
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <omp.h>

#define N (10000000ULL + 3278ULL * 1000ULL) /* ID 230103278 -> 13,278,000 */
#define MOD 1000000007ULL
#define MAX_THREADS 64

static inline uint32_t collatz_steps(uint64_t n) {
    uint32_t steps = 0;
    while (n > 1) {
        if ((n & 1) == 0) n >>= 1;
        else n = 3 * n + 1;
        steps++;
    }
    return steps;
}

int hit_count[MAX_THREADS];
struct Padded { int count; char pad[60]; };
struct Padded padded[MAX_THREADS];

int main(int argc, char **argv) {
    const char *mode = argc > 1 ? argv[1] : "seq";
    int k = argc > 2 ? atoi(argv[2]) : 1;
    uint32_t maxs = 0;
    uint64_t sum = 0, hits = 0;
    double t0 = omp_get_wtime();

    if (!strcmp(mode, "seq")) {
        for (uint64_t i = 1; i <= N; i++) {
            uint32_t s = collatz_steps(i);
            if (s > maxs) maxs = s;
            sum += s;
        }
    } else if (!strcmp(mode, "par")) {
        #pragma omp parallel for num_threads(k) schedule(runtime) reduction(max:maxs) reduction(+:sum)
        for (uint64_t i = 1; i <= N; i++) {
            uint32_t s = collatz_steps(i);
            if (s > maxs) maxs = s;
            sum += s;
        }
    } else if (!strcmp(mode, "fs_naive")) {
        memset(hit_count, 0, sizeof hit_count);
        #pragma omp parallel for num_threads(k) reduction(max:maxs) reduction(+:sum)
        for (uint64_t i = 1; i <= N; i++) {
            uint32_t s = collatz_steps(i);
            if (s > maxs) maxs = s;
            sum += s;
            if (s > 100) hit_count[omp_get_thread_num()]++;
        }
        for (int t = 0; t < MAX_THREADS; t++) hits += hit_count[t];
    } else if (!strcmp(mode, "fs_pad")) {
        memset(padded, 0, sizeof padded);
        #pragma omp parallel for num_threads(k) reduction(max:maxs) reduction(+:sum)
        for (uint64_t i = 1; i <= N; i++) {
            uint32_t s = collatz_steps(i);
            if (s > maxs) maxs = s;
            sum += s;
            if (s > 100) padded[omp_get_thread_num()].count++;
        }
        for (int t = 0; t < MAX_THREADS; t++) hits += padded[t].count;
    }

    double t = omp_get_wtime() - t0;
    printf("%s,%d,%.6f,%u,%llu,%llu\n", mode, k, t, maxs,
           (unsigned long long)(sum % MOD), (unsigned long long)hits);
    return 0;
}
