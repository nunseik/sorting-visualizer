#!/usr/bin/env python3
"""
Main entry point for the Sorting Algorithm Visualizer application.
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports
from sorting_visualizer.algorithms import AlgorithmRegistry, initialize_algorithms
from sorting_visualizer.ui import MainWindow
from sorting_visualizer.utils import handle_errors

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@handle_errors("Application Error", show_dialog=True)
def main():
    """Initialize and run the application."""
    # Setup exception handling
    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        logger.critical('Uncaught exception:', exc_info=(exctype, value, traceback))
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    
    try:
        # Initialize QApplication
        app = QApplication(sys.argv)
        
        # Setup algorithm registry
        logger.info("Initializing algorithm registry...")
        registry = AlgorithmRegistry()
        initialize_algorithms(registry)
        
        # Create and show main window
        logger.info("Creating main window...")
        window = MainWindow(registry)
        window.show()
        
        # Start event loop
        logger.info("Starting application...")
        sys.exit(app.exec())
        
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()