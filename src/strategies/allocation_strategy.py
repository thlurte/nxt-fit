# allocation_strategy.py
from .base_strategy import AllocationStrategy

class NextFitStrategy(AllocationStrategy):
    """
    Implements the Next Fit allocation strategy.
    """
    def __init__(self):
        self.next_fit_pointer = 0

    def find_available_block(self, memory_pool, size):
        """
        Finds an available memory block using Next Fit.
        """
        start_index = self.next_fit_pointer
        for _ in range(len(memory_pool)):
            block = memory_pool[start_index]
            if not block.allocated and block.size >= size:
                self.next_fit_pointer = (start_index + 1) % len(memory_pool)
                return start_index
            start_index = (start_index + 1) % len(memory_pool)
        return -1  # Not found
