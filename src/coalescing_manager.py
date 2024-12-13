# coalescing_manager.py
from .block_operations import BlockOperations

class CoalescingManager:
    """
    Manages the coalescing of free memory blocks.
    """

    def coalesce(self, memory_pool):
        """
        Merges adjacent free memory blocks in the memory pool.

        Args:
            memory_pool (list[MemoryBlock]): The list of memory blocks to coalesce.

        Returns:
             list[MemoryBlock]: Updated memory pool after coalescing.
        """
        i = 0
        while i < len(memory_pool) - 1:
          current_block = memory_pool[i]
          next_block = memory_pool[i+1]
          merged_block = BlockOperations.merge_blocks(current_block,next_block)
          if merged_block:
              memory_pool[i:i+2] = [merged_block]
          else:
              i += 1
        return memory_pool