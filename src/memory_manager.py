# memory_manager.py
from .memory_block import MemoryBlock
from .allocation_strategy import NextFitStrategy  # Import the strategy
from .block_operations import BlockOperations
from .coalescing_manager import CoalescingManager
from .resizing_manager import ResizingManager

class MemoryManager:
    """
    Manages a pool of memory using a specified allocation strategy.
    """
    def __init__(self, total_size, allocation_strategy=None):
        """Initializes the MemoryManager."""
        self.memory_pool = [MemoryBlock(0, total_size)]
        self.allocation_strategy = allocation_strategy or NextFitStrategy()
        self.coalescing_manager = CoalescingManager()
        self.resizing_manager = ResizingManager(self.allocation_strategy)

    def allocate(self, process_id, size):
        """Allocates a block of memory using the chosen strategy."""
        block_index = self.allocation_strategy.find_available_block(self.memory_pool, size)
        if block_index != -1:
            block = self.memory_pool[block_index]
            if block.size == size:  # Exact fit
                block.allocate(process_id)
            else:  # Split the block
                allocated_block, remaining_block = BlockOperations.split_block(block, size, process_id)
                self.memory_pool[block_index:block_index+1] = [allocated_block, remaining_block]
            return allocated_block.start_address  # Return start address on success
        return -1  # Allocation failed

    def deallocate(self, process_id):
        """Deallocates memory blocks occupied by a given process ID."""
        for block in self.memory_pool:
            if block.allocated and block.process_id == process_id:
                block.deallocate()
        self.memory_pool = self.coalescing_manager.coalesce(self.memory_pool)



    def get_memory_map(self):
        """Returns a list of strings representing the current memory map."""
        return [str(block) for block in self.memory_pool]

    def resize_allocation(self, process_id, new_size):
        """Resizes an existing allocation for a process."""
        success, updated_pool = self.resizing_manager.resize_allocation(self.memory_pool, process_id, new_size)
        self.memory_pool = updated_pool  # Update the memory pool
        if success:
            self.memory_pool = self.coalescing_manager.coalesce(self.memory_pool)  # Coalesce after resize
        return success