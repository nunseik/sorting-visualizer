from typing import List

class SortingAlgorithm:
    """Base class for sorting algorithms"""
    def __init__(self, name: str, function: callable, complexity: str):
        self.name = name
        self.function = function
        self.complexity = complexity

class AlgorithmRegistry:
    """Registry to manage all available sorting algorithms"""
    def __init__(self):
        self._algorithms = {}

    def register(self, name: str, function: callable, complexity: str) -> None:
        """Register a new sorting algorithm"""
        self._algorithms[name] = SortingAlgorithm(name, function, complexity)

    def get_algorithm(self, name: str) -> SortingAlgorithm:
        """Get a sorting algorithm by name"""
        return self._algorithms.get(name)

    def get_names(self) -> List[str]:
        """Get list of all registered algorithm names"""
        return list(self._algorithms.keys())

    def __getitem__(self, name: str) -> SortingAlgorithm:
        return self._algorithms[name]