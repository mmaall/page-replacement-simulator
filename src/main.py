from memory_manager import (
    MemoryManager,
    FifoMemoryManager,
    RandomReplacementMemoryManager,
    MruMemoryManager,
    LfuMemoryManager,
    LruKMemoryManager
)
from page_access_generators import generate_page_accesses, WorkloadType
import csv


def main():
    total_pages_to_access = 1000
    default_total_reads = 10000
    buffer_sizes = [50, 100, 150, 200, 250, 300, 350, 400, 450]

    test_workloads = [WorkloadType.random, WorkloadType.scan, WorkloadType.gaussian, WorkloadType.postgres_trace_tpcc, WorkloadType.postgres_trace_tpcc_medium_concurrency, WorkloadType.postgres_trace_tpch]
    test_memory_managers: list[(MemoryManager, dict)] = [
        (MruMemoryManager, {}, "MRU"),
        (RandomReplacementMemoryManager, {}, "Random"),
        (FifoMemoryManager, {}, "FIFO"),
        (LfuMemoryManager, {}, "LFU"),
        (LruKMemoryManager, {"k":1, "c_ref_period": 0}, "LRU1"),
        (LruKMemoryManager, {"k":2, "c_ref_period": 0}, "LRU2-0"),
        (LruKMemoryManager, {"k":2, "c_ref_period": 5}, "LRU2-5"),
        (LruKMemoryManager, {"k":2, "c_ref_period": 20}, "LRU2-20"),
        (LruKMemoryManager, {"k":2, "c_ref_period": 40}, "LRU2-40"),
        (LruKMemoryManager, {"k":2, "c_ref_period": 80}, "LRU2-80"),
        (LruKMemoryManager, {"k":2, "c_ref_period": 200}, "LRU2-200"),
        (LruKMemoryManager, {"k":2, "c_ref_period": 500}, "LRU2-500"),
        (LruKMemoryManager, {"k":2, "c_ref_period": 1000}, "LRU2-1000"),
        (LruKMemoryManager, {"k":3, "c_ref_period": 0}, "LRU3-0"),
        (LruKMemoryManager, {"k":3, "c_ref_period": 5}, "LRU3-5"),
        (LruKMemoryManager, {"k":3, "c_ref_period": 20}, "LRU3-20"),
        (LruKMemoryManager, {"k":3, "c_ref_period": 40}, "LRU3-40"),
        (LruKMemoryManager, {"k":3, "c_ref_period": 80}, "LRU3-80"),
        (LruKMemoryManager, {"k":3, "c_ref_period": 200}, "LRU3-200"),
        (LruKMemoryManager, {"k":3, "c_ref_period": 500}, "LRU3-500"),
        (LruKMemoryManager, {"k":3, "c_ref_period": 1000}, "LRU3-1000"),
    ]

    output_rows = []

    for workload in test_workloads:
        for buffer_size in buffer_sizes:
            print(f"Testing {workload.name} with buffer size {buffer_size}")
            output_row = [workload.name, buffer_size]
            scan_page_accesses = generate_page_accesses(
                total_page_count=total_pages_to_access, total_reads=default_total_reads, workload=workload
            )
            for memory_manager, kargs, name in test_memory_managers:
                print(f"{name}")


                m = memory_manager(
                    memory_page_count=buffer_size, disk_page_count=max(scan_page_accesses)+1, **kargs
                )

                for page in scan_page_accesses:
                    m.read_page(page)

                print(f"Page Faults: {m.total_page_faults}")
                print(f"Total Reads: {m.total_reads}")
                print(f"Page Fault Rate: {m.total_page_faults/m.total_reads}")
                output_row.append(m.total_page_faults / m.total_reads)

            output_rows.append(output_row)

    header = ["workload", "bufferSize"] + [memory_manager_tuple[2] for memory_manager_tuple in test_memory_managers]
    with open(f"output.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(header)

        for row in output_rows:
            csv_writer.writerow(row)


if __name__ == "__main__":
    main()
