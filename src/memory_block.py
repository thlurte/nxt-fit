# memory_block.py

class MemoryBlock:
    """
    Represents a block of memory with a starting address, size, and allocation status.
    """
    def __init__(self, start_address, size, allocated=False):
        """
        Initializes a MemoryBlock.

        Args:
            start_address (int): The starting memory address of the block.
            size (int): The size of the memory block.
            allocated (bool): True if the block is allocated, False otherwise.
        """
        self.start_address = start_address
        self.size = size
        self.allocated = allocated
        self.process_id = None  # ID of the process using the block (if allocated)

    def __str__(self):
        """
        Returns a string representation of the memory block.
        """
        status = "Allocated" if self.allocated else "Free"
        process_info = f", Process ID: {self.process_id}" if self.allocated else ""
        return f"[{self.start_address}:{self.start_address + self.size - 1}] Size: {self.size}, Status: {status}{process_info}"

    def allocate(self, process_id):
      """Allocates the memory block to a process.

      Args:
          process_id: The ID of the process allocating the block.
      """
      if not self.allocated:
          self.allocated = True
          self.process_id = process_id
          return True
      else:
          return False

    def deallocate(self):
        """Deallocates the memory block."""
        if self.allocated:
            self.allocated = False
            self.process_id = None
            return True
        else:
            return False