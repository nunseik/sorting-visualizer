# Sorting Algorithm Visualizer

An interactive Python application that provides real-time visualization of sorting algorithms. This tool allows users to compare different sorting algorithms side by side and even implement and test their own custom sorting algorithms.

## Features

### Core Features
- Dual visualization windows for side-by-side algorithm comparison
- Real-time visualization of sorting process
- Customizable array size and sorting speed
- Built-in time complexity analysis for custom algorithms
- Persistent storage of custom algorithms across sessions

### Supported Algorithms
- Built-in implementations of common sorting algorithms
- Support for custom algorithm implementation
- Automatic time complexity analysis for custom implementations

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Dependencies
```
PyQt6
matplotlib
```

### Installation Steps
1. Clone the repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
```
sorting_visualizer/
├── algorithms/
│   ├── __init__.py
│   ├── base.py
│   └── implementations.py
├── ui/
│   ├── __init__.py
│   ├── complexity_analyzer.py
│   ├── custom_widgets.py
│   ├── main_window.py
│   └── visualization.py
├── utils/
│   ├── __init__.py
│   └── error_handling.py
├── __init__.py
├── main.py
└── setup.py
```

## Usage

### Basic Operation
1. Select sorting algorithms for each visualization window
2. Adjust array size and sorting speed as needed
3. Click "Generate New Arrays" to create new random data
4. Click "Start Sorting" to begin visualization

### Implementing Custom Algorithms
1. Click on the custom algorithm input section
2. Enter a name for your algorithm
3. Implement your sorting algorithm following the template:
```python
def your_sort_name(arr):
    # Create a copy of the input array
    arr = arr.copy()
    steps = 0
    
    # Yield initial state
    yield arr.copy(), steps
    
    # Your sorting logic here
    # Remember to:
    # 1. Increment steps when making changes
    # 2. Yield current state after each change
    
    # Yield final state
    yield arr, steps
```
4. Click "Add Custom Algorithm" to save and register your implementation

The application will automatically analyze your algorithm's time complexity and store it for future sessions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a new branch for your feature
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Make your changes
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:
1. Check the existing issues on GitHub
2. Create a new issue if needed
3. Provide as much detail as possible about your problem
