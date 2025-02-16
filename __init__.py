"""
Sorting Algorithm Visualizer Package
A tool for visualizing and comparing different sorting algorithms in real-time.
"""

from .algorithms import AlgorithmRegistry, initialize_algorithms
from .ui import MainWindow

__version__ = '1.0.0'
__all__ = ['AlgorithmRegistry', 'initialize_algorithms', 'MainWindow']