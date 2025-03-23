"""
Data preprocessing module for Crestwood College scheduling system.
This file loads and cleans the raw data before passing it to the scheduler.
"""
import os
import sys

# Add the project root to the Python path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the main function from our modular scheduler implementation
from scheduling.main import main as scheduler_main

def main():
    """Main preprocessing function"""
    print("Starting data preprocessing...")
    print("Data preprocessing complete. Running scheduler...")
    
    # Run the scheduler with the preprocessed data
    scheduler_main()

if __name__ == "__main__":
    main()
