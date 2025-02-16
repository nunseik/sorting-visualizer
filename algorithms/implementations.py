from typing import List, Generator, Tuple

def bubble_sort(arr: List[int]) -> Generator[Tuple[List[int], int], None, None]:
    """Implementation of bubble sort algorithm"""
    n = len(arr)
    arr = arr.copy()
    steps = 0
    yield arr.copy(), steps
    
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                steps += 1
                arr[j], arr[j+1] = arr[j+1], arr[j]
                yield arr.copy(), steps
    yield arr, steps

def insertion_sort(arr: List[int]) -> Generator[Tuple[List[int], int], None, None]:
    """Implementation of insertion sort algorithm"""
    arr = arr.copy()
    steps = 0
    yield arr.copy(), steps
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        steps += 1
        arr[j+1] = key
        yield arr.copy(), steps
    yield arr, steps

def selection_sort(arr: List[int]) -> Generator[Tuple[List[int], int], None, None]:
    """Implementation of selection sort algorithm"""
    arr = arr.copy()
    steps = 0
    yield arr.copy(), steps
    
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            steps += 1
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr.copy(), steps
    yield arr, steps

def quick_sort(arr: List[int]) -> Generator[Tuple[List[int], int], None, None]:
    """Implementation of quick sort algorithm with visualization"""
    arr = arr.copy()
    steps = 0
    yield arr.copy(), steps
    
    def partition(low: int, high: int) -> Generator[Tuple[List[int], int], None, int]:
        nonlocal steps
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps += 1
                yield arr.copy(), steps
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps += 1
        yield arr.copy(), steps
        return i + 1
    
    def quick_sort_helper(low: int, high: int):
        if low < high:
            # Find pivot element
            pivot_idx = yield from partition(low, high)
            
            # Sort elements before and after partition
            yield from quick_sort_helper(low, pivot_idx - 1)
            yield from quick_sort_helper(pivot_idx + 1, high)
    
    # Start the recursive sorting process
    yield from quick_sort_helper(0, len(arr) - 1)
    yield arr, steps

def merge_sort(arr: List[int]) -> Generator[Tuple[List[int], int], None, None]:
    """Implementation of merge sort algorithm with visualization"""
    arr = arr.copy()
    steps = 0
    yield arr.copy(), steps
    
    def merge(left: int, mid: int, right: int):
        nonlocal steps
        
        # Create temporary arrays
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            k += 1
            steps += 1
            yield arr.copy(), steps
        
        # Check for remaining elements
        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
            steps += 1
            yield arr.copy(), steps
            
        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1
            steps += 1
            yield arr.copy(), steps
    
    def merge_sort_helper(left: int, right: int):
        if left < right:
            mid = (left + right) // 2
            
            # Sort first and second halves
            yield from merge_sort_helper(left, mid)
            yield from merge_sort_helper(mid + 1, right)
            
            # Merge the sorted halves
            yield from merge(left, mid, right)
    
    # Start the recursive sorting process
    yield from merge_sort_helper(0, len(arr) - 1)
    yield arr, steps

def heap_sort(arr: List[int]) -> Generator[Tuple[List[int], int], None, None]:
    """Implementation of heap sort algorithm with visualization"""
    arr = arr.copy()
    steps = 0
    yield arr.copy(), steps
    
    def heapify(n: int, i: int):
        nonlocal steps
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
            
        if right < n and arr[right] > arr[largest]:
            largest = right
            
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            steps += 1
            yield arr.copy(), steps
            yield from heapify(n, largest)
    
    # Build max heap
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)
        
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        steps += 1
        yield arr.copy(), steps
        yield from heapify(i, 0)
    
    yield arr, steps

# Add new algorithms to the registry in initialize_algorithms function
def initialize_algorithms(registry):
    """Register all sorting algorithms"""
    algorithms = [
        ("Bubble Sort", bubble_sort, "O(n²)"),
        ("Insertion Sort", insertion_sort, "O(n²) worst/avg, O(n) best"),
        ("Selection Sort", selection_sort, "O(n²)"),
        ("Quick Sort", quick_sort, "O(n²) worst, O(n log n) avg"),
        ("Merge Sort", merge_sort, "O(n log n)"),
        ("Heap Sort", heap_sort, "O(n log n)")
    ]
    
    for name, func, complexity in algorithms:
        registry.register(name, func, complexity)