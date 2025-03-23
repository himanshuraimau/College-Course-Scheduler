"""
Crestwood College course scheduling package.
Provides modular components for course scheduling optimization.
"""
import os
import sys

# Add parent directory to path to ensure imports work correctly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
