from src.core.memory_manager import MemoryManager
from src.strategies.allocation_strategy import NextFitStrategy
from src.core.memory_block import MemoryBlock

if __name__ == "__main__":
    # Initial Memory Blocks (represented as a list of MemoryBlock objects)
    initial_memory = [
        MemoryBlock(start_address=0, size=200),
        MemoryBlock(start_address=200, size=300),
        MemoryBlock(start_address=500, size=100),
        MemoryBlock(start_address=600, size=500),
        MemoryBlock(start_address=1100, size=50),
    ]

    memory_manager_nf = MemoryManager(total_size=0, allocation_strategy=NextFitStrategy())  # total size is irrelevant here
    memory_manager_nf.memory_pool = initial_memory #setting the memory pool to our defined one

    processes = [("A", 120), ("B", 450), ("C", 90)]
    process_allocations = {} #to store allocation results

    for process_name, process_size in processes:
        start_address = memory_manager_nf.allocate(process_name, process_size)
        if start_address!= -1:
           process_allocations[process_name] = start_address

        print(f"\nMemory Map after allocating {process_name} (size {process_size}): ")
        print(memory_manager_nf.get_memory_map())

    print("\nFinal Memory Allocation:")
    for process_name, start_address in process_allocations.items():
        print(f"Process {process_name}: Allocated in Block starting at {start_address} KB")