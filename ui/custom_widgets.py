from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QTextEdit, QPushButton, QLineEdit)
from .complexity_analyzer import analyze_sorting_algorithm

class CustomAlgorithmWidget(QWidget):
    """Widget for adding custom sorting algorithms"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        input_layout = QVBoxLayout()
        
        # Name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Algorithm Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter algorithm name")
        name_layout.addWidget(self.name_input)
        input_layout.addLayout(name_layout)
        
        # Code input
        self.code_input = QTextEdit()
        self.code_input.setText(self.get_template())
        input_layout.addWidget(self.code_input)
        
        # Complexity display
        complexity_layout = QHBoxLayout()
        complexity_layout.addWidget(QLabel("Estimated Time Complexity:"))
        self.complexity_label = QLabel("O(?)")
        complexity_layout.addWidget(self.complexity_label)
        input_layout.addLayout(complexity_layout)
        
        layout.addLayout(input_layout)
        
        button_layout = QVBoxLayout()
        # Analyze button
        self.analyze_button = QPushButton("Analyze Complexity")
        self.analyze_button.clicked.connect(self.analyze_complexity)
        button_layout.addWidget(self.analyze_button)
        
        # Add button
        self.add_button = QPushButton("Add Custom Algorithm")
        button_layout.addWidget(self.add_button)
        
        layout.addLayout(button_layout)

    def analyze_complexity(self):
        """Analyze the current code and update complexity label"""
        code = self.get_code()
        complexity = analyze_sorting_algorithm(code)
        self.complexity_label.setText(complexity)

    def get_template(self):
        return """# Template for custom sorting algorithm:

def your_sort_name(arr):
    # Create a copy of the input array
    arr = arr.copy()
    steps = 0
    
    # Yield initial state
    yield arr.copy(), steps
    
    # Your sorting logic here
    # Example (bubble sort):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                # Increment steps when making changes
                steps += 1
                # Swap elements
                arr[j], arr[j+1] = arr[j+1], arr[j]
                # Yield current state after each change
                yield arr.copy(), steps
    
    # Yield final state
    yield arr, steps"""

    def get_name(self):
        """Get the entered algorithm name"""
        return self.name_input.text().strip()

    def get_code(self):
        """Get the entered code"""
        return self.code_input.toPlainText()

    def clear_name(self):
        """Clear the name input"""
        self.name_input.clear()