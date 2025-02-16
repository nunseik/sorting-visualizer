import random
import inspect
from typing import List, Optional, Generator, Tuple

from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QGridLayout, 
    QLabel, 
    QComboBox, 
    QSpinBox, 
    QPushButton, 
    QMessageBox
)
from PyQt6.QtCore import QTimer

# Using relative imports
from .visualization import SortingVisualization
from .custom_widgets import CustomAlgorithmWidget
from ..algorithms.base import AlgorithmRegistry, SortingAlgorithm
from .complexity_analyzer import analyze_sorting_algorithm


class MainWindow(QMainWindow):
    """Main window for the sorting algorithm visualizer application"""
    
    def __init__(self, algorithm_registry: AlgorithmRegistry):
        super().__init__()
        self.algorithm_registry = algorithm_registry
        
        # Setup window properties
        self.setWindowTitle("Dual Sorting Algorithm Visualizer")
        self.setGeometry(100, 100, 1600, 900)
        
        # Initialize state
        self.current_data: List[int] = []
        self.sorting_generators: List[Optional[Generator]] = [None, None]
        self.is_sorting: List[bool] = [False, False]
        
        # Initialize timers
        self.timers: List[QTimer] = [QTimer(), QTimer()]
        self.timers[0].timeout.connect(lambda: self.update_sort(0))
        self.timers[1].timeout.connect(lambda: self.update_sort(1))
        
        # Setup UI components
        self.setup_ui()
        
    def setup_ui(self) -> None:
        """Initialize and setup all UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create visualizations
        vis_layout = QHBoxLayout()
        self.visualizations: List[SortingVisualization] = []
        for _ in range(2):
            vis = SortingVisualization()
            self.visualizations.append(vis)
            vis_layout.addWidget(vis)
        
        # Setup controls
        control_panel = self.setup_control_panel()
        custom_panel = CustomAlgorithmWidget()
        custom_panel.add_button.clicked.connect(self.add_custom_algorithm)
        self.custom_widget = custom_panel
        
        # Add widgets to main layout
        main_layout.addWidget(control_panel)
        main_layout.addWidget(custom_panel)
        main_layout.addLayout(vis_layout)
        
        self.generate_new_arrays()
    
    def setup_control_panel(self) -> QWidget:
        """Create and setup the control panel widget"""
        panel = QWidget()
        layout = QGridLayout(panel)
        
        # Initialize control lists
        self.algo_combos: List[QComboBox] = []
        self.size_spins: List[QSpinBox] = []
        self.speed_spins: List[QSpinBox] = []
        self.start_btns: List[QPushButton] = []
        self.stop_btns: List[QPushButton] = []
        
        # Create controls for both visualizations
        for i in range(2):
            # Algorithm selection
            algo_combo = QComboBox()
            algo_combo.addItems(self.algorithm_registry.get_names())
            layout.addWidget(QLabel(f"Algorithm {i+1}:"), 0, i*4)
            layout.addWidget(algo_combo, 0, i*4 + 1)
            self.algo_combos.append(algo_combo)
            
            # Size control
            size_spin = QSpinBox()
            size_spin.setRange(5, 100)
            size_spin.setValue(30)
            layout.addWidget(QLabel("Array Size:"), 1, i*4)
            layout.addWidget(size_spin, 1, i*4 + 1)
            self.size_spins.append(size_spin)
            
            # Speed control
            speed_spin = QSpinBox()
            speed_spin.setRange(1, 1000)
            speed_spin.setValue(50)
            layout.addWidget(QLabel("Speed (ms):"), 2, i*4)
            layout.addWidget(speed_spin, 2, i*4 + 1)
            self.speed_spins.append(speed_spin)
            
            # Buttons
            start_btn = QPushButton("Start Sorting")
            start_btn.clicked.connect(lambda checked, idx=i: self.start_sorting(idx))
            layout.addWidget(start_btn, 3, i*4)
            self.start_btns.append(start_btn)
            
            stop_btn = QPushButton("Stop")
            stop_btn.clicked.connect(lambda checked, idx=i: self.stop_sorting(idx))
            stop_btn.setEnabled(False)
            layout.addWidget(stop_btn, 3, i*4 + 1)
            self.stop_btns.append(stop_btn)
        
        # Common controls
        self.generate_btn = QPushButton("Generate New Arrays")
        self.generate_btn.clicked.connect(self.generate_new_arrays)
        layout.addWidget(self.generate_btn, 4, 0, 1, 8)
        
        return panel
    
    def generate_new_arrays(self) -> None:
        """Generate new random arrays for both visualizations"""
        try:
            # Stop any ongoing sorting
            for i in range(2):
                if self.is_sorting[i]:
                    self.stop_sorting(i)
            
            # Generate same array for both visualizations
            size = self.size_spins[0].value()
            self.current_data = [random.randint(1, 100) for _ in range(size)]
            
            # Plot initial state for both visualizations
            for i in range(2):
                algorithm = self.algorithm_registry[self.algo_combos[i].currentText()]
                self.visualizations[i].plot_array(
                    self.current_data.copy(), 
                    0, 
                    algorithm.name,
                    algorithm.complexity
                )
            
        except Exception as e:
            self.show_error("Generation Error", str(e))
    
    def start_sorting(self, idx: int) -> None:
        """Start the sorting visualization for the specified index"""
        try:
            if self.is_sorting[idx]:
                return
                
            self.is_sorting[idx] = True
            self.start_btns[idx].setEnabled(False)
            self.stop_btns[idx].setEnabled(True)
            self.generate_btn.setEnabled(False)
            self.algo_combos[idx].setEnabled(False)
            self.size_spins[idx].setEnabled(False)
            
            algorithm = self.algorithm_registry[self.algo_combos[idx].currentText()]
            self.sorting_generators[idx] = algorithm.function(self.current_data.copy())
            
            # Start the timer for this visualization
            self.timers[idx].start(self.speed_spins[idx].value())
            
        except Exception as e:
            self.show_error("Start Error", str(e))
            self.stop_sorting(idx)
    
    def update_sort(self, idx: int) -> None:
        """Update the sorting visualization for the specified index"""
        try:
            if not self.is_sorting[idx]:
                return
                
            try:
                # Get next state from generator
                generator = self.sorting_generators[idx]
                if generator is not None:
                    arr, steps = next(generator)
                    algorithm = self.algorithm_registry[self.algo_combos[idx].currentText()]
                    self.visualizations[idx].plot_array(
                        arr, 
                        steps,
                        algorithm.name,
                        algorithm.complexity
                    )
            except StopIteration:
                self.stop_sorting(idx)
                
        except Exception as e:
            self.show_error("Update Error", str(e))
            self.stop_sorting(idx)
    
    def stop_sorting(self, idx: int) -> None:
        """Stop the sorting visualization for the specified index"""
        try:
            self.is_sorting[idx] = False
            self.timers[idx].stop()
            self.sorting_generators[idx] = None
            
            self.start_btns[idx].setEnabled(True)
            self.stop_btns[idx].setEnabled(False)
            self.algo_combos[idx].setEnabled(True)
            self.size_spins[idx].setEnabled(True)
            
            # Only enable generate button if both visualizations are stopped
            if not any(self.is_sorting):
                self.generate_btn.setEnabled(True)
            
        except Exception as e:
            self.show_error("Stop Error", str(e))
    
    def add_custom_algorithm(self) -> None:
        """Add a new custom sorting algorithm with complexity analysis"""
        try:
            # Check if name is provided
            custom_name = self.custom_widget.get_name()
            if not custom_name:
                self.show_error("Input Error", "Please enter a name for your algorithm")
                return
                
            code = self.custom_widget.get_code()
            
            # Analyze the complexity before executing the code
            complexity = analyze_sorting_algorithm(code)
            if complexity == "Invalid code":
                self.show_error("Analysis Error", "The provided code is invalid")
                return
            elif complexity.startswith("Analysis error"):
                complexity = "Unknown complexity"
            
            # Execute the code
            local_namespace = {}
            exec(code, local_namespace)
            
            # Find the first function defined in the code
            func = None
            for _, obj in local_namespace.items():
                if inspect.isfunction(obj):
                    func = obj
                    break
            
            if func is None:
                self.show_error("Input Error", "No function found in the code")
                return
                
            # Add the algorithm to registry with analyzed complexity
            algorithm_name = f"Custom: {custom_name}"
            self.algorithm_registry.register(
                algorithm_name,
                func,
                complexity  # Use the analyzed complexity instead of "Custom Implementation"
            )
            
            # Update combo boxes
            for combo in self.algo_combos:
                combo.addItem(algorithm_name)
            
            # Clear the name field
            self.custom_widget.clear_name()
            
            # Show success message with complexity information
            QMessageBox.information(
                self, 
                "Success", 
                f"Algorithm '{custom_name}' has been added!\nEstimated Time Complexity: {complexity}"
            )
            
        except Exception as e:
            self.show_error("Custom Algorithm Error", str(e))
            
    def show_error(self, title: str, message: str) -> None:
        """Show an error message dialog"""
        QMessageBox.critical(self, title, message)
    
    def closeEvent(self, event) -> None:
        """Handle the window close event"""
        try:
            # Stop all sorting operations
            for i in range(2):
                self.stop_sorting(i)
            
            # Clean up matplotlib resources
            for visualization in self.visualizations:
                visualization.cleanup()
                
            event.accept()
        except Exception as e:
            print(f"Error during close: {str(e)}")
            event.accept()