#!/usr/bin/env python3
"""
Dependency installer for the Crestwood College Scheduling System.
"""
import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies from requirements.txt"""
    print("Installing dependencies...")
    
    try:
        # Try using pip directly
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies using pip.")
        print("Please manually install the requirements using:")
        print("pip install -r requirements.txt")
        return 1
    
    print("\nDependencies installed successfully!")
    print("You can now run the scheduling system with: python run.py")
    return 0

if __name__ == "__main__":
    sys.exit(install_dependencies())
