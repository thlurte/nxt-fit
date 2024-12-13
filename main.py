# main.py
from src.memory_manager import MemoryManager
from src.allocation_strategy import NextFitStrategy  # Import strategies

if __name__ == "__main__":
    # Example using Next Fit Strategy
    memory_manager_nf = MemoryManager(total_size=100, allocation_strategy=NextFitStrategy())
    print("Initial Memory Map (Next Fit):")
    print(memory_manager_nf.get_memory_map())

    pid1 = memory_manager_nf.allocate(1, 30)
    pid2 = memory_manager_nf.allocate(2, 20)
    pid3 = memory_manager_nf.allocate(3, 10)

    print("\nMemory Map after allocations (Next Fit):")
    print(memory_manager_nf.get_memory_map())

    memory_manager_nf.deallocate(2)
    print("\nMemory map after deallocating process 2 (Next Fit) :")
    print(memory_manager_nf.get_memory_map())
    pid4 = memory_manager_nf.allocate(4, 15)

    print("\nMemory Map after allocating process 4(Next Fit) : ")
    print(memory_manager_nf.get_memory_map())