import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

doc = docx.Document()

for section in doc.sections:
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def format_cell(cell, text, bold=False, color_rgb=(0,0,0), font_size=9, align=WD_ALIGN_PARAGRAPH.LEFT, bg_hex=None):
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    if p.runs:
        run = p.runs[0]
        run.bold = bold
        run.font.name = 'Calibri'
        run.font.size = Pt(font_size)
        run.font.color.rgb = RGBColor(*color_rgb)
    if bg_hex:
        set_cell_background(cell, bg_hex)

header_p = doc.add_paragraph()
header_p.paragraph_format.space_after = Pt(2)
r0 = header_p.add_run("ZEBA ACADEMY / INSTRUCTOR – SUFYAN BIN UZAYR\n")
r0.font.size = Pt(9)
r0.font.bold = True
r0.font.color.rgb = RGBColor(90, 90, 90)

r1 = header_p.add_run("Advanced Parallel Programming & Architecture\n")
r1.font.size = Pt(15)
r1.font.bold = True
r1.font.color.rgb = RGBColor(20, 40, 80)

r2 = header_p.add_run("Laboratory Examination & Silicon Profiling Worksheet: Empirical Microarchitectural Bottlenecks\n")
r2.font.size = Pt(10)
r2.font.italic = True

r3 = header_p.add_run("Session Duration: 120 Minutes | Total Evaluation: 100 Points | Mode: Individual Bare-Metal Execution")
r3.font.size = Pt(9)
r3.font.bold = True

meta_table = doc.add_table(rows=8, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Student & Hardware Metadata Field", "Laboratory Session Specifications & Target Machine Declaration"),
    ("Student Full Name", "Kogersh1n"),
    ("Student Identification Number", "230103278"),
    ("Date & Laboratory Session", "September 17, 2026 | Week 3 Laboratory Session"),
    ("Workstation / Laptop Make & Model", "Lenovo LOQ 15AHP9 (Machine Type: 83DX)"),
    ("Processor SKU / SoC Model", "AMD Ryzen 5 8645HS w/ Radeon 760M Graphics"),
    ("Core Topology (Physical P-cores / E-cores)", "Physical Cores: 6 (Zen 4 performance cores) | Logical SMT Threads: 12"),
    ("Cache Hierarchy Capacity", "L1: 32 KB L1d + 32 KB L1i per core (384 KB total) | L2: 1 MB per core (6 MB total) | L3: 16 MB Unified"),
    ("Host OS & Python Runtime", "Linux Kernel 7.2.4-arch1-2 (Arch Linux x86_64) / CPython 3.14.7")
]
while len(meta_table.rows) < len(meta_data):
    meta_table.add_row()

for i, (col1, col2) in enumerate(meta_data):
    row = meta_table.rows[i]
    if i == 0:
        format_cell(row.cells[0], col1, bold=True, color_rgb=(255,255,255), font_size=9, bg_hex="1B365D")
        format_cell(row.cells[1], col2, bold=True, color_rgb=(255,255,255), font_size=9, bg_hex="1B365D")
    else:
        bg = "F4F6F9" if i % 2 == 1 else "FFFFFF"
        format_cell(row.cells[0], col1, bold=True, color_rgb=(30,30,30), font_size=8.5, bg_hex=bg)
        format_cell(row.cells[1], col2, bold=False, color_rgb=(10,10,10), font_size=8.5, bg_hex=bg)

def add_header(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(title)
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(27, 54, 93)

def add_qa(q_text, a_text):
    qp = doc.add_paragraph()
    qp.paragraph_format.space_before = Pt(4)
    qp.paragraph_format.space_after = Pt(2)
    qr = qp.add_run(q_text)
    qr.font.size = Pt(9.5)
    qr.font.bold = True
    qr.font.color.rgb = RGBColor(0, 51, 102)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.rows[0].cells[0]
    format_cell(c, f"Student Response & Architectural Justification:\n{a_text}", font_size=8.5, bg_hex="F8FAFC")

# TASK 1
add_header("TASK 1: AMDAHL'S LAW & PHYSICAL SILICON SATURATION")
t1_table = doc.add_table(rows=7, cols=5)
t1_table.alignment = WD_TABLE_ALIGNMENT.CENTER
t1_headers = ["Worker Cores (p)", "Measured Time T(p) [s]", "Observed Speedup S(p)", "Ideal Linear Speedup", "Parallel Efficiency"]
for j, h in enumerate(t1_headers):
    format_cell(t1_table.rows[0].cells[j], h, bold=True, color_rgb=(255,255,255), font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="1B365D")

t1_rows = [
    ("p = 1 (Baseline)", "2.0869 s", "1.00x (base=5.54s)", "1.00x", "100.0%"),
    ("p = 2", "1.0064 s", "2.07x (term: 5.50x)", "2.00x", "103.5%"),
    ("p = 4", "0.5180 s", "4.03x (term: 10.69x)", "4.00x", "100.8%"),
    ("p = 8", "0.3833 s", "5.44x (term: 14.45x)", "8.00x", "68.0%"),
    ("p = 12", "0.3463 s", "6.03x (term: 15.99x)", "12.00x", "50.3%"),
    ("p = 16", "0.4181 s", "4.99x (term: 13.25x)", "16.00x", "31.2%"),
]
for i, rdata in enumerate(t1_rows):
    bg = "F9FAFC" if i % 2 == 1 else "FFFFFF"
    for j, val in enumerate(rdata):
        format_cell(t1_table.rows[i+1].cells[j], val, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex=bg)

add_qa("[Q1.1] Identify the exact inflection point (core count p*) where your observed speedup curve flattens or degrades. Correlate to hardware topology. (8 Points)",
"""• Flattening Inflection (p* = 6 Physical Cores): The AMD Ryzen 5 8645HS has 6 physical Zen 4 cores (12 SMT threads). For p <= 4, scaling is linear (100.8% efficiency) as each worker has a private physical core. Beyond 6 cores (at p=8 and p=12), SMT logical hyperthreads are engaged, which share dispatch ports, ALUs, and caches rather than duplicating pipelines, reducing efficiency to 68.0% and 50.3%.
• Inversion/Degradation Cliff (p* = 12 -> 16): At p = 16, core allocation exceeds total logical threads (12). Execution time increases from 0.3463s to 0.4181s due to OS scheduler preemption, context-switching overhead, and cache evictions.""")

add_qa("[Q1.2] Using empirical T(1) and T(4), calculate the exact value of P (parallel fraction). Show complete algebraic derivation. (9 Points)",
"""• Algebraic Derivation:
   S(4) = T(1)/T(4) = 1 / [(1 - P) + P/4]  ==>  1/S(4) = 1 - (3/4)P  ==>  P = (4/3) * [1 - T(4)/T(1)]
• Empirical Calculation (T(1)=2.0869s, T(4)=0.5180s, S(4)=4.029x):
   P = (4/3) * [1 - (0.5180 / 2.0869)] = (4/3) * (0.751785) = 1.0024 ≈ 1.000 (100.0% parallel fraction).
   (Demonstrates near-ideal parallel scaling with slight super-linear boost from AMD Precision Boost multi-core clocking).""")

add_qa("[Q1.3] Compute Asymptotic Limit S_max = 1 / (1 - P). Explain implications for a 128-core server node. (8 Points)",
"""• Asymptotic Limit: S_max = 1 / (1 - P). For 1% serial fraction (P=0.99), S_max = 100.0x.
• 128-Core Server Implication: S(128) = 1 / [(1 - 0.99) + 0.99/128] = 56.4x. Parallel efficiency collapses to 56.4 / 128 = 44.0%. Over 56% of server capacity is wasted waiting on serial overhead. Strong scaling fixed workloads yields diminishing returns; problem size must scale proportionally (Gustafson's Law).""")

# TASK 2
add_header("TASK 2: CACHE COHERENCE & THE FALSE SHARING TRAP")
t2_table = doc.add_table(rows=3, cols=6)
t2_table.alignment = WD_TABLE_ALIGNMENT.CENTER
t2_headers = ["Memory Layout Configuration", "Trial 1 [s]", "Trial 2 [s]", "Trial 3 [s]", "Median [s]", "Slowdown Penalty"]
for j, h in enumerate(t2_headers):
    format_cell(t2_table.rows[0].cells[j], h, bold=True, color_rgb=(255,255,255), font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="1B365D")

t2_rows = [
    ("Adjacent Indices (False Sharing)", "0.8425 s", "0.8248 s", "0.8604 s", "0.8425 s", "— [Baseline]"),
    ("Padded Indices (Cache-Aligned)", "0.8551 s", "0.8628 s", "0.8461 s", "0.8551 s", "0.99x (~1.00x)")
]
for i, rdata in enumerate(t2_rows):
    bg = "F9FAFC" if i % 2 == 1 else "FFFFFF"
    for j, val in enumerate(rdata):
        format_cell(t2_table.rows[i+1].cells[j], val, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex=bg)

add_qa("[Q2.1] Calculate memory footprint of 64-bit integer pointer. Prove why stride 16 guarantees cache-line isolation. (8 Points)",
"""• Footprint: In 64-bit CPython, list pointers (PyObject*) occupy 8 bytes (64 bits).
• L1 Geometry: AMD Zen 4 L1 line = 64 bytes ==> 64 / 8 = 8 pointers per cache line.
• Proof for Stride 16: Thread k writes index k*16. ΔAddress = 16 * 8 bytes = 128 bytes = 2 * 64-byte lines.
  Since 128 bytes >= 2 full lines, floor(Addr(k+1)/64) - floor(Addr(k)/64) >= 2. Adjacent thread writes can never touch the same 64-byte L1 cache line, completely preventing false sharing.""")

add_qa("[Q2.2] Trace MESI state transitions for shared cache line (Core 0 writes idx 0, Core 1 writes idx 1). (9 Points)",
"""1. Shared: Both cores read line into L1 ==> Core 0: Shared (S), Core 1: Shared (S).
2. Core 0 Write (idx 0): Core 0 broadcasts BusRdX (Invalidate). Core 1 snoops and shifts Shared -> Invalid (I). Core 0 updates line and shifts Shared -> Modified (M).
3. Core 1 Write (idx 1): Core 1 hits Invalidation Miss (state I). Core 1 broadcasts BusRdX. Core 0 snoops, stalls, flushes line to L3/RAM, and shifts Modified -> Invalid (I). Core 1 receives line and shifts Invalid -> Modified (M).
• Consequence: Alternating writes force ping-pong state bouncing (Shared -> Modified -> Invalid -> Modified), congesting interconnect and stalling CPU pipelines.""")

add_qa("[Q2.3] Describe two industry-standard compile-time or VM-level mechanisms used to eliminate false sharing. (8 Points)",
"""1. C++11/C17 alignas(64): struct alignas(64) WorkerState { uint64_t val; }; enforces 64-byte boundary alignment and padding at compile time (or using std::hardware_destructive_interference_size).
2. Java @Contended (JEP 142): HotSpot JIT compiler dynamically injects 128 bytes of padding around annotated fields in object memory layout, isolating lines without manual array padding.""")

# TASK 3
add_header("TASK 3: THE SYNCHRONIZATION TAX & LOCKLESS REDESIGN")
t3_table = doc.add_table(rows=3, cols=6)
t3_table.alignment = WD_TABLE_ALIGNMENT.CENTER
t3_headers = ["Counter Architecture", "Target Sum", "Actual Sum", "Defect Count", "Execution Time", "Contention Overhead"]
for j, h in enumerate(t3_headers):
    format_cell(t3_table.rows[0].cells[j], h, bold=True, color_rgb=(255,255,255), font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="1B365D")

t3_rows = [
    ("Unsafe Accumulator (Race Condition)", "2,000,000", "2,000,000", "0", "0.1137 s", "1.00x [Baseline]"),
    ("Locked Accumulator (threading.Lock)", "2,000,000", "2,000,000", "0 (Protected)", "0.2758 s", "2.43x")
]
for i, rdata in enumerate(t3_rows):
    bg = "F9FAFC" if i % 2 == 1 else "FFFFFF"
    for j, val in enumerate(rdata):
        format_cell(t3_table.rows[i+1].cells[j], val, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex=bg)

add_qa("[Q3.1] Analyze Unsafe Accumulator output. Explain low-level LOAD, ADD, STORE sequence causing lost updates. (7 Points)",
"""• Empirical Finding: Actual count = 2,000,000 (0 defect). In CPython 3.14, the GIL eval_breaker is checked strictly at loop back-edges (JUMP_BACKWARD) and calls (RESUME). Inside inc(), LOAD_ATTR -> BINARY_OP (+=) -> STORE_ATTR has no backward jump and executes atomically with respect to GIL switching.
• Native Assembly RMW Race: In un-synchronized native execution (C OpenMP), val += 1 compiles to:
  1. LOAD (movq (%rdi), %rax), 2. ADD (addq $1, %rax), 3. STORE (movq %rax, (%rdi)).
  Interleaving: Thread A reads 100. Before A stores, Thread B reads 100. Thread A computes 101 and stores 101. Thread B computes 101 and stores 101. Two increments occurred, but val only increased by 1 (lost update defect).""")

add_qa("[Q3.2] Provide Lockless Thread-Local Accumulator implementation, measured time, and speedup over LockedCounter. (11 Points)",
"""• Implementation (Map-Reduce Partitioning):
class LocklessAccumulator:
    def __init__(self, num_threads=4):
        self.buffers = [0] * num_threads
    def worker(self, tid, ops):
        local_val = 0
        for _ in range(ops): local_val += 1
        self.buffers[tid] = local_val
    def run(self, total_ops=2_000_000):
        ops = total_ops // 4
        threads = [threading.Thread(target=self.worker, args=(i, ops)) for i in range(4)]
        t0 = time.perf_counter()
        for t in threads: t.start()
        for t in threads: t.join()
        return sum(self.buffers), time.perf_counter() - t0
• Empirical Results: LockedCounter: 0.2838 s | LocklessCounter: 0.0904 s ==> Speedup: 3.14x (>2.0x requirement strictly met). Correctness: Deterministically 2,000,000 every run.""")

add_qa("[Q3.3] Why is eliminating shared mutable state fundamentally superior to optimizing lock primitives? (7 Points)",
"""1. Zero Cache Invalidation Traffic: Locks mutate shared atomic flags (CAS/test-and-set), generating bus invalidation traffic on every acquire/release. Thread-local state operates in private registers/lines with zero coherence traffic.
2. Eliminates Amdahl Bottleneck: Locks enforce serialization (1 - P) and futex kernel stalls. Thread-local partitioning is an embarrassingly parallel Map (O(N/p)) with tiny reduction (O(p)), scaling linearly.
3. Concurrency Safety: Completely immune to deadlocks, livelocks, priority inversion, and lock convoying.""")

# TASK 4
add_header("TASK 4: THE MEMORY WALL VS. COMPUTE SATURATION")
t4_table = doc.add_table(rows=4, cols=5)
t4_table.alignment = WD_TABLE_ALIGNMENT.CENTER
t4_headers = ["Worker Allocation", "Compute-Bound Time [s]", "Compute Scaling [Tw / T1]", "Memory-Bound Time [s]", "Memory Degradation [Tw / T1]"]
for j, h in enumerate(t4_headers):
    format_cell(t4_table.rows[0].cells[j], h, bold=True, color_rgb=(255,255,255), font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="1B365D")

t4_rows = [
    ("w = 1 Worker (Baseline)", "1.0610 s", "1.00x", "0.1411 s", "1.00x"),
    ("w = 2 Workers", "0.9108 s", "0.86x", "0.2766 s", "1.96x"),
    ("w = 4 Workers", "0.9106 s", "0.86x", "0.7453 s", "5.28x")
]
for i, rdata in enumerate(t4_rows):
    bg = "F9FAFC" if i % 2 == 1 else "FFFFFF"
    for j, val in enumerate(rdata):
        format_cell(t4_table.rows[i+1].cells[j], val, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex=bg)

add_qa("[Q4.1] Analyze scaling divergence: why compute tasks complete in same elapsed time while memory tasks spike? (9 Points)",
"""• Compute-Bound (High Arithmetic Intensity): compute_heavy executes 25M float multiply-adds entirely in registers. AMD Zen 4 cores have dedicated private ALU/FPU execution units. Under weak scaling, running 4 tasks on 4 physical cores executes concurrently without resource contention; elapsed time stays flat (~0.91s).
• Memory-Bound (Low Arithmetic Intensity & Bus Saturation): memory_heavy streams 50M floats (400 MB) per worker (0.25 FLOP/byte). 400 MB bypasses L1/L2/L3 caches (L3=16MB), forcing DRAM streaming. All cores share a single off-chip memory bus. 4 concurrent workers (1.6 GB) saturate bus bandwidth, causing memory queue stalls that spike time by 5.28x.""")

add_qa("[Q4.2] Physical memory specifications, theoretical peak bandwidth calculation, and bus width limits. (8 Points)",
"""• Specs: Lenovo LOQ 15AHP9, AMD Ryzen 5 8645HS, 16 GB DDR5, 128-bit dual-channel bus (16 bytes).
• Theoretical Peak Bandwidth:
  - DDR5-5600: 5,600 MT/s * 16 bytes = 89.6 GB/s.  |  DDR5-4800: 4,800 MT/s * 16 bytes = 76.8 GB/s.
• Bus Width Limits: The 128-bit bus sets a hard bandwidth ceiling (B_max). Once parallel core demand exceeds B_max, adding cores yields zero throughput; each core receives only B_max/p, stalling CPU pipelines.""")

add_qa("[Q4.3] Memory-bandwidth saturated ML embedding pipeline: CUDA GPU kernels vs CPU OpenMP. Justify. (8 Points)",
"""• Choice: CUDA GPU Kernels.
• Justification:
  1. Superior Bandwidth: Vector embedding is strictly memory-bandwidth bound (Time = Size / Bandwidth). CPU DDR5 provides <= 89.6 GB/s, while discrete GPUs provide 192-224 GB/s (RTX 4050) up to 3,350 GB/s (H100 HBM3).
  2. Latency Hiding: GPU Warp Schedulers instantly hide memory stalls across thousands of active threads.
  3. CPU OpenMP Penalty: Adding CPU OpenMP threads to a memory-saturated workload causes bus contention and negative scaling (5.28x slowdown in Task 4).""")

# BONUS TASK
add_header("BONUS TASK: THREADING VS. MULTIPROCESSING AUTOPSY")
tb_table = doc.add_table(rows=7, cols=3)
tb_table.alignment = WD_TABLE_ALIGNMENT.CENTER
tb_headers = ["Workers (T)", "threading.Thread Time [s]", "multiprocessing.Pool Time [s]"]
for j, h in enumerate(tb_headers):
    format_cell(tb_table.rows[0].cells[j], h, bold=True, color_rgb=(255,255,255), font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="1B365D")

tb_rows = [
    ("1", "2.4078 s", "2.9233 s"),
    ("2", "2.6083 s", "1.3793 s"),
    ("4", "2.6133 s", "0.7291 s"),
    ("8", "2.7548 s", "0.4875 s"),
    ("16", "2.7060 s", "0.4690 s"),
    ("32", "2.6974 s", "0.4739 s")
]
for i, rdata in enumerate(tb_rows):
    bg = "F9FAFC" if i % 2 == 1 else "FFFFFF"
    for j, val in enumerate(rdata):
        format_cell(tb_table.rows[i+1].cells[j], val, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex=bg)

plot_path = "/home/duklet/CSS_314/week3/bonus_empirical_curve.png"
if os.path.exists(plot_path):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.add_run("Bonus Deliverable 1: Empirical Worker Scaling Curve Plot\n").bold = True
    doc.add_picture(plot_path, width=Inches(5.5))

add_qa("Bonus Deliverables 2 & 3: Inflection Cliff & Architectural Autopsy",
"""1. GIL Serialization: CPython's GIL serializes bytecode to 1 thread at a time. Threads in threading.Thread cannot execute concurrently across physical cores, flatlining at ~2.7s. multiprocessing.Pool uses separate OS processes with private GILs, achieving true multi-core scaling (2.92s -> 0.47s, >6.2x speedup).
2. CPU Topology: AMD Ryzen 5 8645HS: 6 Physical Zen 4 Cores, 12 Logical SMT Threads.
3. Core Saturation & Context-Switching Cliff:
   - Physical core saturation occurs at T = 6. Up to T = 4, each process gets a dedicated core (2.92s -> 0.73s). From T = 6 to 12, SMT logical threads share pipelines with diminishing returns.
   - At T = 32 (T > 12 logical threads), execution degrades (0.4690s -> 0.4739s) due to OS preemption, register save/restore overhead, TLB flushes, and L1/L2 cache pollution.""")

out_path = "/home/duklet/CSS_314/week3/COMPLETED_WORKSHEET.docx"
doc.save(out_path)
print(f"Generated concise docx: {os.path.getsize(out_path)} bytes")
