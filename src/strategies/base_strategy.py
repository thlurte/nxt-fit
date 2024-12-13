from abc import ABC, abstractmethod

class AllocationStrategy(ABC):
    """
    Abstract base class for memory allocation strategies.
    """
    @abstractmethod
    def find_available_block(self, memory_pool, size):
        """
        Finds an available memory block of the given size.

        Args:
            memory_pool (list[MemoryBlock]): The list of memory blocks.
            size (int): The size of the memory block to find.

        Returns:
            int: The index of the available block if found, -1 otherwise.
        """
        pass