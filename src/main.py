from memory_manager import (
    FifoMemoryManager,
    RandomReplacementMemoryManager,
    LruMemoryManager,
    LfuMemoryManager,
)
from page_access_generators import generate_page_accesses, WorkloadType


def main():
    total_pages_to_access = 20
    pages_in_memory = 8

    test_workloads = [WorkloadType.random, WorkloadType.scan, WorkloadType.gaussian]
    test_memory_managers = [
        FifoMemoryManager,
        RandomReplacementMemoryManager,
        LruMemoryManager,
        LfuMemoryManager,
    ]

    for workload in test_workloads:
        print(f"Testing {workload.name}")
        for memory_manager in test_memory_managers:

            print(f"{memory_manager.__name__}")
            m = memory_manager(
                memory_page_count=pages_in_memory, disk_page_count=total_pages_to_access
            )

            scan_page_accesses = generate_page_accesses(
                total_page_count=total_pages_to_access, total_reads=10000, workload=workload
            )

            for page in scan_page_accesses:
                m.read_page(page)

            print(f"Page Faults: {m.total_page_faults}")
            print(f"Total Reads: {m.total_reads}")
            print(f"Page Fault Rate: {m.total_page_faults/m.total_reads}")


if __name__ == "__main__":
    main()
