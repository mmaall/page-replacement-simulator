from enum import Enum, auto
from random import randint


class WorkloadType(Enum):
    scan = auto()
    random = auto()


def generate_page_accesses(
    total_page_count: int, total_reads: int, workload: WorkloadType
) -> list[int]:
    """Generates a list of page accesses as if it was a linear scan.

    :param total_page_count: The total number of pages that the scan will access.
    :type total_page_count: int
    :param total_reads: The total number of reads that will occur
    :type total_reads: int
    :param workload: The type of page accesses that will occur
    :type workload: WorkloadType
    :return: A list of len(total_reads) containing the pages to be read.
    :rtype: list[int]
    """
    read_order = []

    if workload == WorkloadType.scan:
        for i in range(total_reads):
            read_order.append(i % total_page_count)
    elif workload == WorkloadType.random:
        for i in range(total_reads):
            read_order.append(randint(0, total_page_count - 1))

    return read_order
