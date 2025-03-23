# Project Structure

The project follows a modular architecture to separate concerns and make the codebase more maintainable.

## Directory Structure

```
/College-Course-Schedular
├── dataset.xlsx - Student requests.csv
├── dataset.xlsx - Course list.csv
├── dataset.xlsx - Lecturer Details.csv
├── dataset.xlsx - Rooms data.csv
├── dataset.xlsx - RULES.csv
├── requirements.txt
├── README.md
├── src/
│   ├── run.py                    # Entry point script
│   └── scheduling/               # Main package
│       ├── __init__.py
│       ├── main.py               # Main orchestration logic
│       ├── config.py             # Configuration settings
│       ├── data/                 # Data handling
│       │   ├── __init__.py
│       │   ├── loader.py         # Data loading functions
│       │   └── processor.py      # Data processing functions
│       ├── analysis/             # Analysis modules
│       │   ├── __init__.py
│       │   ├── validator.py      # Data validation
│       │   └── analyzer.py       # Data analysis
│       ├── visualization/        # Visualization
│       │   ├── __init__.py
│       │   └── visualizer.py     # Visualization functions
│       ├── scheduling/           # Core scheduling
│       │   ├── __init__.py
│       │   └── optimizer.py      # Scheduling optimization
│       └── reporting/            # Report generation
│           ├── __init__.py
│           └── reporter.py       # Reporting functions
└── output/                       # Generated outputs
    ├── data/                     # Processed data files
    ├── reports/                  # Generated reports
    └── visualizations/           # Generated visualizations
```

## Key Components

- **Data Handling**: Responsible for loading, cleaning, and processing the input data
- **Analysis**: Performs data validation and analysis to generate insights
- **Visualization**: Creates visual representations of the data and results
- **Scheduling**: Implements the core scheduling algorithm using constraint optimization
- **Reporting**: Generates reports and documentation of the results
