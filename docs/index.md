# Crestwood College Course Scheduler Documentation

Welcome to the documentation for the Crestwood College Course Scheduling System. This system is designed to automate the process of scheduling courses based on student requests, lecturer availability, and room constraints.

## Overview

The scheduling system performs the following tasks:
1. Data cleaning and structuring from various input sources
2. Analysis of student requests and course demand
3. Optimization of the course schedule to maximize fulfilled requests
4. Generation of reports and visualizations for analysis

## Table of Contents

- [Project Structure](./project_structure.md)
- [Installation & Setup](./installation.md)
- [Algorithm Details](./algorithm.md)
- [Module Reference](./modules.md)
- [API Reference](./api.md)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scheduler
python src/run.py
```

The results will be available in the `/output` directory, including:
- Cleaned data in JSON format
- Analysis reports
- Schedule reports
- Visualizations
