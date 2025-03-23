"""
Scheduling algorithm module for the Crestwood College Course Scheduling System.
This module imports and runs the main scheduling logic from scheduler_algorithm.py.
"""
import os
import sys

# Add the root directory to path to import scheduler_algorithm.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the main function from scheduler_algorithm.py
from src.scheduling.scheduler_algorithm import main as scheduler_algorithm_main

if __name__ == "__main__":
    # Run the main scheduling algorithm
    scheduler_algorithm_main()
