import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class SortingVisualization(QWidget):
    """Widget for visualizing sorting algorithms"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create figure and canvas
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def plot_array(self, arr, steps, algorithm_name, complexity):
        """Update the visualization with new array state"""
        try:
            self.ax.clear()
            self.ax.bar(range(len(arr)), arr, color='skyblue')
            self.ax.set_title(f"{algorithm_name}\nSteps: {steps}")
            self.ax.set_xlabel("Index")
            self.ax.set_ylabel("Value")
            self.ax.text(0.02, 0.98, f"Time Complexity: {complexity}", 
                        transform=self.ax.transAxes, verticalalignment='top')
            self.canvas.draw()
        except Exception as e:
            raise Exception(f"Plot Error: {str(e)}")

    def cleanup(self):
        """Clean up matplotlib resources"""
        plt.close(self.figure)