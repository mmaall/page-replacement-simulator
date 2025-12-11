from enum import Enum, auto
from random import randint, gauss
import json
from functools import lru_cache

class WorkloadType(Enum):
    scan = auto()
    random = auto()
    gaussian = auto()
    postgres_trace_tpcc = auto()
    postgres_trace_tpcc_medium_concurrency = auto()
    postgres_trace_tpcc_high_concurrency = auto()
    postgres_trace_tpch = auto()
    pgbench = auto()


@lru_cache(maxsize=256)
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
    elif workload == WorkloadType.postgres_trace_tpcc:
        read_order = read_trace_from_file("../postgresql_tracing/data/tpcc/benchbase-disk-reads-default-configuration")
    elif workload == WorkloadType.postgres_trace_tpcc_high_concurrency:
        read_order = read_trace_from_file("../postgresql_tracing/data/tpcc/benchbase-disk-reads-high-concurrency")
    elif workload == WorkloadType.postgres_trace_tpcc_medium_concurrency:
        read_order = read_trace_from_file("../postgresql_tracing/data/tpcc/benchbase-disk-reads-medium-concurrency")
    elif workload == WorkloadType.postgres_trace_tpch:
        read_order =  read_trace_from_file("../postgresql_tracing/data/tpch/benchbase_tpch_reads")
    elif workload == WorkloadType.pgbench:
        read_order = json.loads(open('../postgresql_tracing/data/pages_requested').read())
    return read_order[0:2000000]


def read_trace_from_file(filename: str) -> []:
    output = []
    with open(filename) as trace_file:
        for line in trace_file:
            output.append(int(line))

    return output
