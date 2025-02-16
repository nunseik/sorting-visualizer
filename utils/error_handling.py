from typing import Optional, Type, Callable
from functools import wraps
import traceback
import logging
from PyQt6.QtWidgets import QMessageBox

# Setup logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def show_error_dialog(title: str, message: str, parent=None) -> None:
    """Display an error message dialog to the user."""
    QMessageBox.critical(parent, title, message)

def handle_errors(error_title: str, show_dialog: bool = True) -> Callable:
    """
    Decorator for handling exceptions in GUI operations.
    
    Args:
        error_title (str): Title for the error dialog
        show_dialog (bool): Whether to show error dialog to user
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log the error
                logger.error(f"Error in {func.__name__}: {str(e)}")
                logger.error(traceback.format_exc())
                
                # Show error dialog if requested
                if show_dialog:
                    error_message = f"An error occurred: {str(e)}"
                    # Try to get parent widget for modal dialog
                    parent = args[0] if args and hasattr(args[0], 'parent') else None
                    show_error_dialog(error_title, error_message, parent)
                
                # Re-raise the exception if it's a program-ending error
                if isinstance(e, (SystemExit, KeyboardInterrupt)):
                    raise
                
        return wrapper
    return decorator

class SortingVisualizerError(Exception):
    """Base exception class for sorting visualizer errors."""
    pass

class AlgorithmError(SortingVisualizerError):
    """Exception raised for errors in sorting algorithms."""
    pass

class VisualizationError(SortingVisualizerError):
    """Exception raised for errors in visualization operations."""
    pass

class CustomAlgorithmError(SortingVisualizerError):
    """Exception raised for errors in custom algorithm handling."""
    pass