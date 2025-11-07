from typing import Set 


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


    def read_page(self, page_number: int):
        if page_number >= self.disk_page_count or page_number < 0:
            raise InvalidPageNumber("Attempting to address an invalid page number")

        self.total_reads += 1
        # Check if the page is in memory
        if page_number in self._memory_pages:
            return

        # Evict a page from memory if necessary
        if len(self._memory_pages) >= self.memory_page_count:
            page_to_evict = self._find_page_to_evict()
            self.memory_pages.remove(page_to_evict)

        # Add page to memory
        self._memory_pages.add(page_number)
        self.total_page_faults += 1
        self.page_faults.append(self.total_reads)


    def _find_page_to_evict(self) -> int:
        raise NotImplementedError()
    
class Page0ReplacementMemoryManager(MemoryManager):
    def __init__(self, memory_page_count, disk_page_count):
        super().__init__(memory_page_count, disk_page_count)

    def _find_page_to_evict(self) -> int:
        """Always returns the 0'th page for replacement"""
        return 0