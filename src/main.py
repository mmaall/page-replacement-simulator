from memory_manager import (
    MemoryManager,
    FifoMemoryManager,
    RandomReplacementMemoryManager,
    LruMemoryManager,
    MruMemoryManager,
    LfuMemoryManager,
    LruKMemoryManager
)
from page_access_generators import generate_page_accesses, WorkloadType
import csv


def main():
    total_pages_to_access = 22181
    percent_in_memory = 0.005#0.042
    pages_in_memory = total_pages_to_access * percent_in_memory

    test_workloads = [WorkloadType.random, WorkloadType.scan, WorkloadType.gaussian, WorkloadType.postgres_trace_tpcc]
    test_memory_managers: list[MemoryManager] = [
        FifoMemoryManager,
        RandomReplacementMemoryManager,
        LruMemoryManager,
        MruMemoryManager,
        LfuMemoryManager,
        LruKMemoryManager
    ]

    output_rows = []

    for workload in test_workloads:
        output_row = [workload.name]
        print(f"Testing {workload.name}")
        for memory_manager in test_memory_managers:

            print(f"{memory_manager.__name__}")

            scan_page_accesses = generate_page_accesses(
                total_page_count=total_pages_to_access, total_reads=10000, workload=workload
            )

            print(max(scan_page_accesses))
            m = memory_manager(
                memory_page_count=pages_in_memory, disk_page_count=max(scan_page_accesses)+1
            )

            for page in scan_page_accesses:
                m.read_page(page)

            print(f"Page Faults: {m.total_page_faults}")
            print(f"Total Reads: {m.total_reads}")
            print(f"Page Fault Rate: {m.total_page_faults/m.total_reads}")
            output_row.append(m.total_page_faults / m.total_reads)

        output_rows.append(output_row)

    header = ["workload"] + [memory_manager.__name__ for memory_manager in test_memory_managers]
    with open(f"output.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(header)

        for row in output_rows:
            csv_writer.writerow(row)


if __name__ == "__main__":
    main()
