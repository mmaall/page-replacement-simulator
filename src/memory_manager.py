import random
from typing import Set 
from collections import deque


class MemoryManagerException(Exception):
    pass

class InvalidPageNumber(Exception):
    pass

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
        return_value = super(FifoMemoryManager, self).read_page(page_number, *args, **kwargs)

        if return_value:
            self._input_queue.append(page_number)

        return return_value


    def _evict_page(self) -> int:
        """Evict in FIFO fashion"""

        # Pop the head element
        page_at_head = self._input_queue.popleft()
        self._memory_pages.remove(page_at_head)

        return page_at_head