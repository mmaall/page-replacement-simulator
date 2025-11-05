from typing import Set 


class MemoryManagerException(Exception):
    pass

class InvalidPageNumber(Exception):
    pass

class MemoryManager:

    def __init__(self, memory_page_count: int, disk_page_count: int):
        self._memory_page_count = memory_page_count
        self._disk_page_count = disk_page_count
        self._memory_pages: Set[int] = {}

        # Operations to keep track of
        self._total_reads: int = 0
        self._total_page_faults: int = 0
        self._page_faults: list[int] = []


    def read_page(self, page_number: int):
        if page_number >= self._disk_page_count or page_number < 0:
            raise InvalidPageNumber("Attempting to address an invalid page number")
        
        # Check if the page is in memory
        if page_number in self._memory_pages:
            self._total_reads += 1
            return

        # Evict a page from memory if necessary
        if len(self._memory_pages) >= self._memory_page_count:
            page_to_evict = self._find_page_to_evict()
            self._memory_pages.remove(page_to_evict)

        # Add page to memory
        self._memory_pages.add(page_number)
        self._page_faults += 1


    def _find_page_to_evict(self) -> int:
        raise NotImplementedError()
        