# Installation and Setup

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

1. Clone the repository or extract the project files to your desired location

2. Install the required dependencies:

```bash
cd College-Course-Schedular
pip install -r requirements.txt
```

The requirements file includes:
- pandas==1.5.3
- matplotlib==3.7.1
- seaborn==0.12.2
- numpy==1.24.3
- pulp==2.7.0

## Input Data Files

Ensure the following input files are available in the project root directory:
- `dataset.xlsx - Student requests.csv`
- `dataset.xlsx - Course list.csv`
- `dataset.xlsx - Lecturer Details.csv`
- `dataset.xlsx - Rooms data.csv`
- `dataset.xlsx - RULES.csv`

## Running the Scheduler

To run the scheduler, execute:

```bash
cd College-Course-Schedular
python src/run.py
```

This will:
1. Load and clean the data
2. Analyze student requests and course demand
3. Generate a schedule that maximizes fulfilled requests
4. Create reports and visualizations of the results

## Output Files

The scheduler will generate the following outputs:

1. Cleaned data (in `/output/data/`):
   - `cleaned_data.json` - Structured clean data
   - `schedule.json` - Final schedule data

2. Reports (in `/output/data/reports/`):
   - `analysis_report.md` - Analysis of the data
   - `schedule_report.md` - Schedule statistics and views

3. Visualizations (in `/output/data/visualizations/`):
   - `course_demand.png` - Course demand analysis
   - `student_years.png` - Student year distribution
   - `request_resolution.png` - Request resolution statistics
   - `priority_resolution.png` - Resolution by priority
   - `course_resolution_rates.png` - Course resolution rates

