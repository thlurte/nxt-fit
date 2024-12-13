# memory_manager.py
from .memory_block import MemoryBlock
from .allocation_strategy import NextFitStrategy  # Import the strategy

class MemoryManager:
    """
    Manages a pool of memory using a specified allocation strategy.
    """
    def __init__(self, total_size, allocation_strategy=None):
        """
        Initializes the MemoryManager.

        Args:
            total_size (int): The total size of the memory pool.
            allocation_strategy (AllocationStrategy): The strategy to use. Defaults to NextFit.
        """
        self.memory_pool = [MemoryBlock(0, total_size)]
        self.allocation_strategy = allocation_strategy or NextFitStrategy()

    def allocate(self, process_id, size):
        """
        Allocates a block of memory using the chosen strategy.
        """
        block_index = self.allocation_strategy.find_available_block(self.memory_pool, size)
        if block_index != -1:
            block = self.memory_pool[block_index]
            if block.size == size:  # Exact fit
                block.allocate(process_id)
            else:  # Split the block
                allocated_block = MemoryBlock(block.start_address, size, allocated=True)
                allocated_block.process_id = process_id
                remaining_block = MemoryBlock(block.start_address + size, block.size - size)
                self.memory_pool[block_index:block_index+1] = [allocated_block, remaining_block]

            return allocated_block.start_address
        return -1  # Allocation failed

    def deallocate(self, process_id):
       """
        Deallocates memory blocks occupied by a given process ID.
         Args:
            process_id (int): The ID of the process to deallocate memory from.

        """
       for block in self.memory_pool:
          if block.allocated and block.process_id == process_id:
            block.deallocate()

       self.coalesce() #Merge free blocks after deallocation

    def coalesce(self):
        """
        Merges adjacent free memory blocks.
        """
        i = 0
        while i < len(self.memory_pool) - 1:
            current_block = self.memory_pool[i]
            next_block = self.memory_pool[i + 1]

            if not current_block.allocated and not next_block.allocated:
                merged_block = MemoryBlock(current_block.start_address, current_block.size + next_block.size)
                self.memory_pool[i:i + 2] = [merged_block]
            else:
                i += 1

    def get_memory_map(self):
      """
      Returns a list of strings representing the current memory map.

      Returns:
          list: A list of strings describing each memory block.
      """
      return [str(block) for block in self.memory_pool]

    def resize_allocation(self, process_id, new_size):
        """
        Resizes an existing allocation for a process.

        Args:
            process_id (int): The ID of the process to resize.
            new_size (int): The new size of the allocated block.

        Returns:
            bool: True if resizing is successful, False otherwise.
        """
        for i, block in enumerate(self.memory_pool):
            if block.allocated and block.process_id == process_id:
                if new_size <= block.size:
                # Shrinking the allocation
                    if new_size < block.size:
                        remaining_block = MemoryBlock(block.start_address + new_size, block.size - new_size)
                        block.size = new_size
                        self.memory_pool.insert(i + 1, remaining_block)
                        self.coalesce()  # Attempt to merge any newly freed space
                    return True
                else:
                    # Attempt to grow the allocation
                    # Check if the next block is free and can be merged

                    if i + 1 < len(self.memory_pool) and not self.memory_pool[i+1].allocated and block.size + self.memory_pool[i+1].size >= new_size :

                         if block.size + self.memory_pool[i+1].size == new_size:
                              block.size = new_size
                              del self.memory_pool[i+1]
                              return True
                         else :
                              remaining_size = (block.size + self.memory_pool[i+1].size) - new_size
                              block.size = new_size
                              self.memory_pool[i+1] = MemoryBlock(self.memory_pool[i+1].start_address ,remaining_size)
                              return True

                     # Check if previous block is free, if so and is large enough , then shift to the block to the left and then expand
                    elif  i-1 >=0  and not self.memory_pool[i-1].allocated and block.size + self.memory_pool[i-1].size >= new_size:
                            if block.size + self.memory_pool[i-1].size == new_size :

                              block.start_address =  self.memory_pool[i-1].start_address
                              block.size = new_size
                              del self.memory_pool[i-1]

                              return True
                            else:
                                remaining_size = (block.size + self.memory_pool[i-1].size) - new_size
                                block.start_address =  self.memory_pool[i-1].start_address + remaining_size
                                block.size = new_size
                                self.memory_pool[i-1] = MemoryBlock(self.memory_pool[i-1].start_address ,remaining_size)

                                return True

                    else:
                        # Find a free block to fit the resized allocation using Next Fit.
                         block_index = self.allocation_strategy.find_available_block(self.memory_pool,new_size)

                         if block_index != -1 :

                             new_block = self.memory_pool[block_index]
                             if new_block.size == new_size :
                                  new_block.allocate(process_id)
                                  block.deallocate()
                                  self.coalesce()
                                  return True
                             else :
                                  allocated_block = MemoryBlock(new_block.start_address, new_size, allocated = True)
                                  allocated_block.process_id = process_id
                                  remaining_block = MemoryBlock(new_block.start_address + new_size,new_block.size - new_size)
                                  self.memory_pool[block_index:block_index+1] = [allocated_block,remaining_block]
                                  block.deallocate()
                                  self.coalesce()
                                  return True

                         else:
                            return False  # Cannot resize, no suitable block found
        return False  # Process not found or cannot resize