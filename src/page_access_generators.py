from enum import Enum, auto
from random import randint, gauss


class WorkloadType(Enum):
    scan = auto()
    random = auto()
    gaussian = auto()


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
    elif workload == WorkloadType.gaussian:
        middle = int(total_page_count / 2)
        # 3 standard deviations should encapsulate almost all our data.
        std_deviation_size = int(middle / 3)

        while len(read_order) != total_reads:
            page_number = int(gauss(mu=middle, sigma=std_deviation_size))

            if page_number >= 0 and page_number < total_page_count:
                # Only take the page number if it fits in our bounds
                read_order.append(page_number)
    return read_order
