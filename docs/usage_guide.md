# Usage Guide

This guide explains how to use the Crestwood College Course Scheduling System.

## Basic Usage

### Running the Complete System

To run the entire scheduling process:

```bash
python run.py
```

This executes all three phases:
1. Data preprocessing and analysis
2. Scheduling algorithm
3. Report generation

### Running Individual Components

You can also run each component separately:

```bash
# Data preprocessing only
python scheduler.py

# Scheduling algorithm only (requires cleaned_data.json)
python scheduler_algorithm.py

# Report generation only (requires cleaned_data.json and scheduling_results.json)
python report_generator.py
```

## Input Data Preparation

### Student Requests

Prepare student course requests in a CSV file with the following columns:
- `College Year`: Student's year level
- `Request start term`: When the course should start
- `Title`: Course title
- `Type`: Request type (Required, Requested, Recommended)
- `student ID`: Unique student identifier
- `Course ID`: Course identifier
- `Length`: Course duration (1 = half year, 2 = full year)
- `Course code`: Unique course code
- `Priority`: Priority level
- `Department(s)`: Academic department(s)
- `Credits`: Course credit value

### Customizing Input/Output Paths

To customize file paths, modify the constants at the top of each script:

```python
# In scheduler.py
BASE_DIR = '/your/custom/path'
STUDENT_REQUESTS_FILE = os.path.join(BASE_DIR, 'your-student-requests.csv')
# ...other file paths...
```

## Interpreting Results

### Analysis Report

The `analysis_report.md` file contains:
- Data summary and statistics
- Validation results and issues
- Key insights from the data
- Course demand analysis
- Potential scheduling conflicts

### Scheduling Results

The `scheduling_results.json` file contains the complete scheduling solution:
- Block schedules (which courses are in which blocks)
- Student schedules (individual schedules for each student)
- Statistics on request fulfillment

### Final Report

The `final_report.md` file offers a comprehensive overview of the scheduling results:
- Executive summary
- Fulfillment rate analysis
- Block utilization
- Course assignment statistics
- Challenges and solutions
- Recommendations for future terms

### Visualizations

The system generates several visualizations in the `visualizations` directory:
- Course demand by priority
- Student distribution by year
- Request fulfillment rates
- Block utilization
- Course assignments

## Customization Options

### Adjusting Scheduling Priorities

To modify how the algorithm prioritizes different factors:

1. **Change the order of scheduling phases** in `scheduler_algorithm.py`:
```python
def run_scheduling(self):
    # Change the order of these calls to affect prioritization
    self.schedule_required_courses()
    self.schedule_requested_courses()
    self.schedule_recommended_courses()
```

2. **Modify section creation logic** to change how sections are sized:
```python
# Modify these calculations in scheduler_algorithm.py
needed_sections = max(1, (demand + target_size - 1) // target_size)
```

### Adding Custom Constraints

To add custom scheduling constraints:
1. Add validation logic in `_assign_student_to_course` or `_assign_block_to_section` methods
2. Implement additional checks before making assignments

## Troubleshooting

### Common Issues

1. **Data Loading Errors**
   - Ensure CSV files are properly formatted
   - Check file paths in the constants at the top of each script
   - Verify CSV column names match the expected names

2. **JSON Serialization Errors**
   - These are often caused by NumPy data types that can't be serialized
   - The `convert_numpy_types` function should handle this, but check for any missed conversions

3. **Visualization Errors**
   - Ensure matplotlib and seaborn are properly installed
   - Check that the visualization directory exists and is writable
