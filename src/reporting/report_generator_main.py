"""
Report generation module for the Crestwood College Course Scheduling System.
This module imports and runs the main reporting logic from report_generator.py.
"""
import os
import sys

# Add the root directory to path to import report_generator.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the main function from report_generator.py
from src.reporting.report_generator import main as report_generator_main

if __name__ == "__main__":
    # Run the main report generation function
    report_generator_main()
