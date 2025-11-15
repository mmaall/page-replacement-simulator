from memory_manager import FifoMemoryManager as MemoryManager
from page_access_generators import generate_page_accesses, WorkloadType



def main():
    total_pages_to_access = 10
    pages_in_memory = 8

    memory_manager = MemoryManager(
        memory_page_count=pages_in_memory,
        disk_page_count=total_pages_to_access
    )

    scan_page_accesses = generate_page_accesses(
        total_page_count=total_pages_to_access,
        total_reads=10000,
        workload = WorkloadType.scan
    )


    for page in scan_page_accesses:
        memory_manager.read_page(page)

    print(f"Page Faults: {memory_manager.total_page_faults}")
    print(f"Total Reads: {memory_manager.total_reads}")
    print(f"Page Fault Rate: {memory_manager.total_page_faults/memory_manager.total_reads}")


if __name__ == '__main__':
    main()