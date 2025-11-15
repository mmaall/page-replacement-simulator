import pytest

from src.memory_manager import RandomReplacementMemoryManager, MemoryManager, InvalidPageNumber


@pytest.fixture()
def basic_memory_manager():
    return RandomReplacementMemoryManager(2, 4)


def test_create_basic_memory_manager(basic_memory_manager):
    assert isinstance(basic_memory_manager, MemoryManager)


def test_read_memory_basic_memory_manager(basic_memory_manager):
    basic_memory_manager.read_page(0)


def test_read_invalid_page_basic_memory_manager(basic_memory_manager):
    with pytest.raises(InvalidPageNumber):
        basic_memory_manager.read_page(basic_memory_manager.disk_page_count)


def test_total_reads_basic_memory_manager(basic_memory_manager):
    for i in range(basic_memory_manager.memory_page_count):
        basic_memory_manager.read_page(i)

    assert basic_memory_manager.total_reads == basic_memory_manager.memory_page_count
    assert basic_memory_manager.total_page_faults == basic_memory_manager.total_reads


def test_page_faults_basic_memory_manager(basic_memory_manager):
    pages_to_read = basic_memory_manager.memory_page_count + 1
    for i in range(pages_to_read):
        basic_memory_manager.read_page(i)

    assert basic_memory_manager.total_reads == pages_to_read
    assert basic_memory_manager.total_page_faults == pages_to_read
