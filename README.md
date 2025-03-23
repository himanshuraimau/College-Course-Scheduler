# Crestwood College Course Scheduler

This project implements a course scheduling system for Crestwood College that:
1. Cleans and structures the raw data from various sources
2. Analyzes course demands and student requests
3. Creates an optimal schedule that maximizes fulfilled student requests
4. Generates reports and visualizations on the scheduling results

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Ensure the input data files are in the correct location:
   - `/home/himanshu/Downloads/test/dataset.xlsx - Student requests.csv`
   - `/home/himanshu/Downloads/test/dataset.xlsx - Course list.csv`
   - `/home/himanshu/Downloads/test/dataset.xlsx - Lecturer Details.csv`
   - `/home/himanshu/Downloads/test/dataset.xlsx - Rooms data.csv`
   - `/home/himanshu/Downloads/test/dataset.xlsx - RULES.csv`

## Running the Scheduler

Execute the main script:
```
python src/run.py
```

## Output Files

After running the scheduler, the following output will be generated:

1. Cleaned data:
   - `/output/data/cleaned_data.json` - Structured JSON data
   - `/output/data/schedule.json` - Final schedule data

2. Reports:
   - `/output/reports/analysis_report.md` - Data analysis from Milestone 1
   - `/output/reports/schedule_report.md` - Schedule statistics from Milestone 2

3. Visualizations:
   - `/output/visualizations/course_demand.png` - Course demand analysis
   - `/output/visualizations/student_years.png` - Student year distribution
   - `/output/visualizations/request_resolution.png` - Request resolution rates
   - `/output/visualizations/priority_resolution.png` - Priority-wise resolution 
   - `/output/visualizations/course_resolution_rates.png` - Course resolution rates

## Project Structure

The project follows a modular architecture:

```
src/
├── run.py                    # Entry point script
└── scheduling/               # Main package
    ├── main.py               # Main orchestration logic
    ├── config.py             # Configuration settings
    ├── data/                 # Data handling
    │   ├── loader.py         # Data loading functions
    │   └── processor.py      # Data processing functions
    ├── analysis/             # Analysis modules
    │   ├── validator.py      # Data validation
    │   └── analyzer.py       # Data analysis
    ├── visualization/        # Visualization
    │   └── visualizer.py     # Visualization functions
    ├── scheduling/           # Core scheduling
    │   └── optimizer.py      # Scheduling optimization
    └── reporting/            # Report generation
        └── reporter.py       # Reporting functions
```

## Algorithm Details

The scheduler uses a constraint-based optimization approach with PuLP to:
- Maximize fulfilled student requests with priority weighting
- Ensure no student is scheduled for multiple courses in the same block
- Respect room capacities and course size constraints
- Assign lecturers to their courses without conflicts

## Documentation

Comprehensive documentation is available in the `docs` directory:
- [Installation Guide](./docs/installation.md)
- [Project Structure](./docs/project_structure.md)
- [Algorithm Details](./docs/algorithm.md)
- [Module Reference](./docs/modules.md)
- [API Reference](./docs/api.md)
- [Developer Guide](./docs/developer_guide.md)
