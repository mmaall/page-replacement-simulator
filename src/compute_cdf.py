import numpy as np
import matplotlib.pyplot as plt
from page_access_generators import generate_page_accesses, WorkloadType

workloads = [
    (WorkloadType.gaussian, "Normal Distribution"),
    (WorkloadType.random, "Random Distribution"),
    (WorkloadType.scan, "Scan Distribution"),
    (WorkloadType.postgres_trace_tpcc, "TPC-C"),
    (WorkloadType.postgres_trace_tpch, "TPC-H"),
]


# Normalizing to TPCC which is biggest benchmark
tpcc_read_order =generate_page_accesses(total_page_count = 0, total_reads = 0, workload= WorkloadType.postgres_trace_tpcc)
total_page_count = max(tpcc_read_order)
total_reads = len(tpcc_read_order)

tpch_read_order =generate_page_accesses(total_page_count = 0, total_reads = 0, workload= WorkloadType.postgres_trace_tpch)
print(max(tpch_read_order))
print(len(set(tpcc_read_order)))

for workload, name in workloads:
    Z = generate_page_accesses(total_page_count=total_page_count, total_reads=total_reads, workload=workload)
    H, X1 = np.histogram(Z, bins=100, density=True)
    dx = X1[1] - X1[0]
    F1 = np.cumsum(H) * dx

    plt.plot(X1[1:], F1, label=name)


plt.legend()
plt.show()
