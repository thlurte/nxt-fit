# Memory Simulation

This project simulates the Next Fit algorithm. The simulation is designed with a modular architecture for extension and maintainability.

## Features

This memory simulation offers a range of features designed for flexibility and extensibility. It implements the Next Fit allocation algorithm, managing memory blocks dynamically. The modular design, based on core components, allocation strategies, and utility modules, promotes code organization and makes it easier to integrate new functionalities. Key features include a `MemoryBlock` class for representing memory blocks, coalescing of free blocks to reduce fragmentation, and support for resizing allocated memory blocks (subject to available space). The extensible strategy pattern simplifies the addition of new allocation strategies, and a clear `MemoryManager` interface provides a straightforward way to interact with the simulation.

## Diagrams

### System Flow Diagram

```mermaid
graph TD
    A[Start] --> B["Input Number of Memory Blocks (n)"];
    B --> C{i = 0};
    C --> D{i < n?};
    D -- Yes --> E[Input Start Address and Size for Block i];
    E --> F[Add MemoryBlock to Memory Pool];
    F --> G[i++];
    G --> D;
    D -- No --> H["Input Number of Processes (m)"];
    H --> I{j = 0};
    I --> J{j < m?};
    J -- Yes --> K[Input Process ID and Size for Process j];
    K --> L["Call MemoryManager.allocate()"];
    L --> M{Allocation Successful?};
    M -- Yes --> N["Output: Allocation Details"];
    N --> O[j++];
    O --> J;
    M -- No --> P["Output: Allocation Failed"];
    P --> O;
    J -- No --> Q["Input Process ID to Terminate (optional)"];
    Q --> R{Process ID provided?};
    R -- Yes --> S["Call MemoryManager.deallocate()"];
    S --> T[Output Memory Map];
    T --> U[End];
    R -- No --> T;
```

### Next Fit Algorithm

```mermaid
graph TD
    A["Start: allocate(process_id, size)"] --> B{Start from next_fit_pointer in memory_pool};
    B --> C{Free MemoryBlock found?};
    C -- Yes --> D{MemoryBlock.size >= requested size?};
    D -- Yes --> E{"Split MemoryBlock if necessary (using BlockOperations)"};
    E --> F["Allocate MemoryBlock (set allocated=True, process_id)"];
    F --> G[Update next_fit_pointer];
    G --> H[Return MemoryBlock.start_address];
    D -- No --> J["Move to next MemoryBlock in memory_pool (circularly)"];
    J --> C;
    C -- No --> K{"Reached end of memory_pool (wrapped around)?"};
    K -- Yes --> L[Allocation Failed];
    K -- No --> J;
    L --> M[Return -1];
    H --> I[End];
    M --> I;
```

### Class Diagram

```mermaid
classDiagram
    class MemoryBlock {
        -start_address: int
        -size: int
        -allocated: bool
        -process_id: str
        +allocate(process_id: str)
        +deallocate()
    }
    class MemoryManager {
        -memory_pool: list[MemoryBlock]
        -allocation_strategy: AllocationStrategy
        -coalescing_manager: CoalescingManager
        -resizing_manager: ResizingManager
        +allocate(process_id: str, size: int)
        +deallocate(process_id: str)
        +get_memory_map(): list[str]
        +resize_allocation(process_id:str, new_size:int)
    }
    class AllocationStrategy {
        <<interface>>
        +find_available_block(memory_pool, size): int
    }
    class NextFitStrategy {
        -next_fit_pointer: int
        +find_available_block(memory_pool, size): int
    }
    class BlockOperations {
        +split_block(block, size, process_id)
        +merge_blocks(block1, block2)
    }
    class CoalescingManager {
        +coalesce(memory_pool)
    }
    class ResizingManager{
        -allocation_strategy : AllocationStrategy
        +resize_allocation(memory_pool,process_id,new_size)
    }

    MemoryManager "1" *-- "*" MemoryBlock : manages
    MemoryManager "1" -- "1" AllocationStrategy: uses
    MemoryManager "1" -- "1" CoalescingManager : uses
    MemoryManager "1"-- "1" ResizingManager : uses
    NextFitStrategy --|> AllocationStrategy : implements
    ResizingManager "1" -- "1" AllocationStrategy : uses
```

## Project Structure

The project follows a well-organized structure to enhance code clarity and maintainability. The `memory_management` package contains sub-packages for core components (`memory_block.py`, `memory_manager.py`), allocation strategies (`next_fit.py`), and utility modules (`block_operations.py`, `coalescing_manager.py`). This modular structure separates concerns, making it easier to understand and modify individual parts of the system. 

```
.
├── LICENSE
├── main.py
├── README.md
└── src
    ├── core
    │   ├── __init__.py
    │   ├── memory_block.py
    │   ├── memory_manager.py
    ├── strategies
    │   ├── allocation_strategy.py
    │   ├── base_strategy.py
    │   ├── __init__.py
    └── utils
        ├── block_operations.py
        ├── coalescing_manager.py
        ├── __init__.py
        └── resizing_manager.py
```

## Getting Started

To get started with the simulation, clone the repository using `git clone <repository_url>`. Then, navigate to the project directory (`cd memory_simulation`) and run the simulation using `python main.py`. You can customize the simulation logic and parameters within the `main.py` file.

## Usage Example (in `main.py`)

The following example demonstrates how to use the `MemoryManager` and `NextFitStrategy` in your `main.py` file:

```python
from memory_management.core.memory_manager import MemoryManager
from memory_management.strategies.next_fit import NextFitStrategy

memory_manager = MemoryManager(total_size=100, allocation_strategy=NextFitStrategy())
print(memory_manager.get_memory_map())  # Print initial memory map

pid1 = memory_manager.allocate(1, 30)
# ... allocate, deallocate, resize as needed ...

print(memory_manager.get_memory_map()) # Print the final memory map
```