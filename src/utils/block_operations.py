# block_operations.py
from src.core.memory_block import MemoryBlock

class BlockOperations:
    """
    Handles operations related to splitting and merging memory blocks.
    """

    @staticmethod
    def split_block(block, size, process_id):
      """
      Splits a memory block into an allocated block and a remaining free block.

      Args:
          block (MemoryBlock): The block to split.
          size (int): The size of the allocated portion.
          process_id (int): The ID of the process allocating the block.

      Returns:
          tuple: A tuple containing the allocated block and the remaining free block.
      """
      if block.size <= size:
          raise ValueError("Block size is not sufficient for splitting")
      allocated_block = MemoryBlock(block.start_address, size, allocated=True)
      allocated_block.process_id = process_id
      remaining_block = MemoryBlock(block.start_address + size, block.size - size)
      return allocated_block, remaining_block

    @staticmethod
    def merge_blocks(block1, block2):
      """
       Merges two adjacent free memory blocks.

       Args:
          block1 (MemoryBlock): The first block.
          block2 (MemoryBlock): The second block.

        Returns:
            MemoryBlock: The merged block, or None if blocks cannot be merged.
       """
      if not block1 or not block2:
            return None
      
      if not block1.allocated and not block2.allocated and block1.start_address + block1.size == block2.start_address:
         return MemoryBlock(block1.start_address, block1.size + block2.size)
      else:
         return None