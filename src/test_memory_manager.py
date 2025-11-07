import pytest

from src.memory_manager import Page0ReplacementMemoryManager, MemoryManager, InvalidPageNumber

@pytest.fixture()
def basic_memory_manager():
    return Page0ReplacementMemoryManager(2,4)

def test_create_basic_memory_manager(basic_memory_manager):
    assert isinstance(basic_memory_manager, MemoryManager)

def test_read_memory_basic_memory_manager(basic_memory_manager):
    basic_memory_manager.read_page(0)

def test_read_invalid_page_basic_memory_manager(basic_memory_manager):
    with pytest.raises(InvalidPageNumber):
        basic_memory_manager.read_page(basic_memory_manager.disk_page_count)
