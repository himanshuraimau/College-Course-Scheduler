#!/usr/bin/env python3
"""
Main entry point for the Crestwood College Course Scheduling System.
"""
import os
import sys

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []
    try:
        import pandas
    except ImportError:
        missing_deps.append("pandas")
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    try:
        import matplotlib
    except ImportError:
        missing_deps.append("matplotlib")
    try:
        import seaborn
    except ImportError:
        missing_deps.append("seaborn")
    try:
        import pulp
    except ImportError:
        missing_deps.append("pulp")
    
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
        print("Please install all required dependencies using:")
        print("pip install -r requirements.txt")
        return False
    
    print("All required dependencies are installed.")
    return True

def main():
    """Main function to orchestrate the scheduling process"""
    print("===== Crestwood College Course Scheduling System =====\n")
    
    # Check dependencies first
    if not check_dependencies():
        return
    
    # Set up the Python path for imports
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Try to import and run directly from the modular structure
    try:
        print("Running scheduler using modular structure...")
        from src.scheduling.main import main as scheduler_main
        scheduler_main()
    except ImportError as e:
        print(f"Error importing from modular structure: {e}")
        print("Falling back to original structure...")
        
        try:
            # Fall back to the original scheduler.py if the modular structure fails
            from src.scheduling.scheduler import main as original_scheduler_main
            original_scheduler_main()
        except ImportError as e2:
            print(f"Critical error: {e2}")
            print("Please make sure either the modular structure or the original scheduler.py file exists.")
            return 1
    
    print("\nScheduling process completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
