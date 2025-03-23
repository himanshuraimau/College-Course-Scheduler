"""
Error handling utilities for the scheduling system.
"""
import sys
import traceback

def log_error(error_type, error_message, traceback_info=None):
    """Log an error with appropriate formatting"""
    print(f"\nERROR: {error_type}")
    print(f"Message: {error_message}")
    if traceback_info:
        print("\nTraceback:")
        print(traceback_info)

def handle_exception(exc_type, exc_value, exc_traceback):
    """Custom exception handler for uncaught exceptions"""
    # Log the error
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    log_error(exc_type.__name__, str(exc_value), error_msg)
    
    # Display user-friendly message for specific errors
    if exc_type.__name__ == "ModuleNotFoundError" and "pulp" in str(exc_value):
        print("\n======================================================")
        print("PuLP module not found. This is required for scheduling.")
        print("Please install it using: pip install pulp==2.7.0")
        print("or run: python install_deps.py")
        print("======================================================")
    
    elif exc_type.__name__ == "ImportError":
        print("\n======================================================")
        print("Import error detected. This might be due to:")
        print("1. Missing dependencies")
        print("2. Path issues in the codebase")
        print("3. Incorrect module structure")
        print("\nTry running: python install_deps.py")
        print("======================================================")

def setup_error_handling():
    """Set up custom error handling"""
    sys.excepthook = handle_exception
