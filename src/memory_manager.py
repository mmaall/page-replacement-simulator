from dataclasses import dataclass
from functools import total_ordering
import random
from typing import Dict, Set
from collections import deque
import math


class MemoryManagerException(Exception):
    pass


class InvalidPageNumber(Exception):
    pass


@total_ordering
@dataclass
class PageRead:
    page: int
    time: int
    frequency: int
    sort_mode: str = "time"

    def __eq__(self, other):
        if self.sort_mode == "frequency":
            return self.frequency == other.frequency
        else:
            # Defaults to time
            return self.time == other.time

    def __lt__(self, other):
        if self.sort_mode == "frequency":
            return self.frequency < other.frequency
        else:
            # Defaults to time
            return self.time < other.time


class MemoryManager:

    def __init__(self, memory_page_count: int, disk_page_count: int):
        self.memory_page_count = memory_page_count
        self.disk_page_count = disk_page_count
        self._memory_pages: Set[int] = set()

        # Operations to keep track of
        self.total_reads: int = 0
        self.total_page_faults: int = 0
        self.page_faults: list[int] = []

    def read_page(self, page_number: int) -> bool:
        """Read a page with the given page number. Returns true if a page fault occured

        :param page_number: The page number to read
        :type page_number: int
        :return: Returns whether a page fault occured. True indicates yes
        :rtype: bool
        """
        if page_number >= self.disk_page_count or page_number < 0:
            raise InvalidPageNumber("Attempting to address an invalid page number")

        self.total_reads += 1
        # Check if the page is in memory
        if page_number in self._memory_pages:
            return False

        # Evict a page from memory if necessary
        if len(self._memory_pages) >= self.memory_page_count:
            page_to_evict = self._evict_page()

        # Add page to memory
        self._memory_pages.add(page_number)
        self.total_page_faults += 1
        self.page_faults.append(self.total_reads)

        return True

    def _evict_page(self) -> int:
        raise NotImplementedError()


class RandomReplacementMemoryManager(MemoryManager):
    def __init__(self, memory_page_count, disk_page_count):
        super().__init__(memory_page_count, disk_page_count)

    def _evict_page(self) -> int:
        """Always returns the 0'th page for replacement"""
        page_to_evict = random.choice(list(self._memory_pages))
        self._memory_pages.remove(page_to_evict)
        return page_to_evict


class FifoMemoryManager(MemoryManager):
    def __init__(self, memory_page_count, disk_page_count):
        self._input_queue = deque()
        super().__init__(memory_page_count, disk_page_count)

    def read_page(self, page_number: int, *args, **kwargs):
        page_fault = super(FifoMemoryManager, self).read_page(page_number, *args, **kwargs)

        if page_fault:
            self._input_queue.append(page_number)

        return page_fault

    def _evict_page(self) -> int:
        """Evict in FIFO fashion"""

        # Pop the head element
        page_at_head = self._input_queue.popleft()
        self._memory_pages.remove(page_at_head)

        return page_at_head


class LruMemoryManager(MemoryManager):
    def __init__(self, memory_page_count, disk_page_count):
        self._recency_statistics: dict[int, PageRead] = {}
        super().__init__(memory_page_count, disk_page_count)

    def read_page(self, page_number: int, *args, **kwargs):
        page_fault = super(LruMemoryManager, self).read_page(page_number, *args, **kwargs)

        # Minus 1 for read epoch because the superclass read will add 1
        read_epoch = self.total_reads - 1

        if page_fault:
            # We need to add this record to the stastics
            self._recency_statistics[page_number] = PageRead(page_number, read_epoch, frequency=0)

        else:
            # We need to update the statistic because this has been used more recently.
            self._recency_statistics[page_number].time = read_epoch

        return page_fault

    def _evict_page(self) -> int:
        """Evict most recently used page"""

        lru_page = min(self._recency_statistics, key=self._recency_statistics.get)
        # Remove the memory page
        self._memory_pages.remove(lru_page)
        # Remove the page from the statistics as we're no longer tracking it.
        self._recency_statistics.pop(lru_page)

        return lru_page


class MruMemoryManager(MemoryManager):
    def __init__(self, memory_page_count, disk_page_count):
        self._recency_statistics: dict[int, PageRead] = {}
        super().__init__(memory_page_count, disk_page_count)

    def read_page(self, page_number: int, *args, **kwargs):
        page_fault = super(MruMemoryManager, self).read_page(page_number, *args, **kwargs)

        # Minus 1 for read epoch because the superclass read will add 1
        read_epoch = self.total_reads - 1

        if page_fault:
            # We need to add this record to the stastics
            self._recency_statistics[page_number] = PageRead(page_number, read_epoch, frequency=0)

        else:
            # We need to update the statistic because this has been used more recently.
            self._recency_statistics[page_number].time = read_epoch

        return page_fault

    def _evict_page(self) -> int:
        """Evict most recently used page"""

        mru_page = max(self._recency_statistics, key=self._recency_statistics.get)
        # Remove the memory page
        self._memory_pages.remove(mru_page)
        # Remove the page from the statistics as we're no longer tracking it.
        self._recency_statistics.pop(mru_page)

        return mru_page


class LfuMemoryManager(MemoryManager):
    def __init__(self, memory_page_count, disk_page_count):
        self._inactive_page_statistics: dict[int, PageRead] = {}
        self._active_page_statistics: dict[int, PageRead] = {}
        super().__init__(memory_page_count, disk_page_count)

    def read_page(self, page_number: int, *args, **kwargs):
        page_fault = super(LfuMemoryManager, self).read_page(page_number, *args, **kwargs)

        # Minus 1 for read epoch because the superclass read will add 1
        read_epoch = self.total_reads - 1

        if page_fault:
            page_read_stats = self._inactive_page_statistics.get(page_number)
            if not page_read_stats:
                # No page found in old stats, so we must increase it.
                page_read_stats = PageRead(page_number, read_epoch, 0, sort_mode="frequency")

            # increase page frequency
            page_read_stats.frequency += 1

            # add to the active pages
            self._active_page_statistics[page_number] = page_read_stats
            # drop from inactive pages
            try:
                self._inactive_page_statistics.pop(page_number)
            except:
                # swallow key errors here
                pass

        else:
            # Increase the frequency of active pages
            self._active_page_statistics[page_number].frequency += 1

        return page_fault

    def _evict_page(self) -> int:
        """Evict most recently used page"""

        lfu_page = min(self._active_page_statistics, key=self._active_page_statistics.get)
        # Remove the memory page
        self._memory_pages.remove(lfu_page)
        # Remove the page from the statistics as we're no longer tracking it.
        lfu_page_stats = self._active_page_statistics.pop(lfu_page)
        # Add it back to inactive page tracker
        self._inactive_page_statistics[lfu_page_stats.page] = lfu_page_stats

        return lfu_page


class LruKPageStats():

    def __init__(self, page:int, k:int):
        # Page number
        self.page = page
        # History of page references
        self.history = [0] * k
        # Max references to hold onto
        self.k = k
        # Correlated reference period
        self.c_reference_period = -1
        # Last time this page was referenced
        self.last = -1

    def recalculate_history(self, new_read_time: int):

        # TODO: I think we need to check if history is uninitialized
        if(self.history[0] == 0):
            self.history[0] = new_read_time

        else:
            page_c_ref_period = self.last - self.history[0]
            for i in range(1, self.k):
                if(self.history[self.k-i-1] == 0):
                    # don't calculate history if it is based on zero
                    continue
                self.history[self.k-i] = self.history[self.k-i-1] + page_c_ref_period

        self.history[0] = new_read_time



class LruKMemoryManager(MemoryManager):
    def __init__(self, memory_page_count, disk_page_count, k:int = 1, c_ref_period:int = 0):
        self._k = k
        self._page_stats: dict[int, LruKPageStats] = {} 
        self._c_ref_period = c_ref_period
        super().__init__(memory_page_count, disk_page_count)

    def read_page(self, page_number: int, *args, **kwargs):
        page_fault = super(LruKMemoryManager, self).read_page(page_number, *args, **kwargs)

        # Minus 1 for read epoch because the superclass read will add 1
        read_time = self.total_reads - 1

        if page_fault:
            page_stats = self._page_stats.get(page_number)
            if not page_stats:
                # Page is currently not tracked in statistics
                page_stats = LruKPageStats(page_number, self._k)
                self._page_stats[page_number] = page_stats


            # shift history
            for i in range(1, self._k):
                page_stats.history[self._k-i] = page_stats.history[self._k-i-1]
            page_stats.history[0] = read_time
            page_stats.last = read_time


        else:
            # Page was already in memory, we need to update statistics
            page_stats = self._page_stats[page_number]

            if read_time - page_stats.last > self._c_ref_period:
                # We are outside of the crp, record in history 
                page_stats.recalculate_history(read_time)
            
            # Update the last access time
            page_stats.last = read_time

        return page_fault

    def _evict_page(self) -> int:
        """Evict most recently used page"""

        read_time = self.total_reads
        minimum = read_time
        victim = list(self._memory_pages)[0] # Select some arbitrary victim

        for page in self._memory_pages:
            page_stat = self._page_stats[page]

            if read_time - page_stat.last > self._c_ref_period and page_stat.history[self._k-1] < minimum:
                # Select a page if it is out of correlated reference period and it has max k distance
                # Tracking min because we're looking for the earliest time, hence oldest reference
                minimum = page_stat.history[self._k-1]
                victim = page


        # Remove the memory page
        self._memory_pages.remove(victim)

        return victim