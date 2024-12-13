# resizing_manager.py
from src.core.memory_block import MemoryBlock
from .block_operations import BlockOperations

class ResizingManager:
    """
    Manages resizing of allocated memory blocks.
    """

    def __init__(self, allocation_strategy):
        self.allocation_strategy = allocation_strategy

    def resize_allocation(self, memory_pool, process_id, new_size):
      """
        Resizes an existing allocation for a process.

        Args:
            memory_pool (list[MemoryBlock]): The current memory pool.
            process_id (int): The ID of the process to resize.
            new_size (int): The new size of the allocated block.

        Returns:
            bool: True if resizing is successful, False otherwise.
            list[MemoryBlock]: updated memory pool.
        """
      for i, block in enumerate(memory_pool):
          if block.allocated and block.process_id == process_id:
              if new_size <= block.size:
              # Shrinking the allocation
                  if new_size < block.size:
                      remaining_block = MemoryBlock(block.start_address + new_size, block.size - new_size)
                      block.size = new_size
                      memory_pool.insert(i + 1, remaining_block)
                      #coalesce  # Attempt to merge any newly freed space
                  return True, memory_pool
              else:
                  # Attempt to grow the allocation
                  # Check if the next block is free and can be merged

                  if i + 1 < len(memory_pool) and not memory_pool[i+1].allocated and block.size + memory_pool[i+1].size >= new_size :

                       if block.size + memory_pool[i+1].size == new_size:
                            block.size = new_size
                            del memory_pool[i+1]
                            return True, memory_pool
                       else :
                            remaining_size = (block.size + memory_pool[i+1].size) - new_size
                            block.size = new_size
                            memory_pool[i+1] = MemoryBlock(memory_pool[i+1].start_address ,remaining_size)
                            return True, memory_pool

                   # Check if previous block is free, if so and is large enough , then shift to the block to the left and then expand
                  elif  i-1 >=0  and not memory_pool[i-1].allocated and block.size + memory_pool[i-1].size >= new_size:
                          if block.size + memory_pool[i-1].size == new_size :

                            block.start_address =  memory_pool[i-1].start_address
                            block.size = new_size
                            del memory_pool[i-1]

                            return True, memory_pool
                          else:
                              remaining_size = (block.size + memory_pool[i-1].size) - new_size
                              block.start_address =  memory_pool[i-1].start_address + remaining_size
                              block.size = new_size
                              memory_pool[i-1] = MemoryBlock(memory_pool[i-1].start_address ,remaining_size)

                              return True, memory_pool

                  else:
                      # Find a free block to fit the resized allocation using Next Fit.
                       block_index = self.allocation_strategy.find_available_block(memory_pool,new_size)

                       if block_index != -1 :

                           new_block = memory_pool[block_index]
                           if new_block.size == new_size :
                                new_block.allocate(process_id)
                                block.deallocate()
                                #self.coalesce()
                                return True, memory_pool
                           else :
                                allocated_block = MemoryBlock(new_block.start_address, new_size, allocated = True)
                                allocated_block.process_id = process_id
                                remaining_block = MemoryBlock(new_block.start_address + new_size,new_block.size - new_size)
                                memory_pool[block_index:block_index+1] = [allocated_block,remaining_block]
                                block.deallocate()
                                #self.coalesce()
                                return True, memory_pool

                       else:
                          return False, memory_pool  # Cannot resize, no suitable block found
      return False, memory_pool  # Process not found or cannot resize