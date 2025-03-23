# Developer Guide

This guide provides information for developers who want to extend or modify the Crestwood College scheduling system.

## Code Organization

The project follows a modular design pattern to separate concerns and improve maintainability:

- **Configuration**: Centralized config in `config.py`
- **Data Management**: Data loading and processing in the `data` module
- **Analysis**: Data validation and analysis in the `analysis` module
- **Visualization**: Visualization generation in the `visualization` module
- **Scheduling Algorithm**: Core scheduling logic in the `scheduling` module
- **Reporting**: Report generation in the `reporting` module

## Adding New Features

### Extending the Data Loader

To support additional data sources:

1. Add new loading functions in `data/loader.py`
2. Update the `config.py` file with the new file paths
3. Integrate the new data in `main.py`

### Modifying the Scheduling Algorithm

To adjust the scheduling algorithm:

1. Modify the constraint definitions in `scheduling/optimizer.py`
2. Adjust weights in the objective function
3. Update the schedule extraction code if needed

### Adding New Visualizations

To create new visualizations:

1. Add new functions to `visualization/visualizer.py`
2. Call these functions from `main.py`
3. Update report templates to include the new visualizations

## Testing

Currently, the project does not have formal tests. To add tests:

1. Create a `tests` directory
2. Add test files for each module
3. Implement unit tests using the `unittest` or `pytest` framework

Example test structure:
```
/tests/
├── __init__.py
├── test_data_loader.py
├── test_data_processor.py
├── test_validator.py
├── test_analyzer.py
├── test_optimizer.py
```

## Contributing Guidelines

When contributing to this project:

1. Follow the modular design pattern
2. Add documentation for new functions and modules
3. Maintain PEP 8 style compliance
4. Test your changes thoroughly before submitting
5. Update relevant documentation

## Common Tasks

### Adding a New Constraint to the Scheduler

To add a new constraint to the scheduling algorithm:

```python
# Example: Add constraint that limits the number of consecutive blocks for students
for student in students:
    student_id = student['id']
    for i in range(len(blocks) - 1):
        block1 = blocks[i]
        block2 = blocks[i+1]
        # Sum of courses in consecutive blocks should be ≤ 1 (no consecutive classes)
        prob += pulp.lpSum(x[(student_id, course_code, block1)] + 
                          x[(student_id, course_code, block2)]
                          for course_code in student_courses) <= 1
```

### Implementing Different Scheduling Priorities

To modify the priority weighting system:

```python
# Modify priority weights in optimizer.py
priority_weights = {
    'required': 15,    # Increased from 10
    'requested': 5,
    'recommended': 1
}
```

### Adding New Report Formats

To add a new report format:

1. Create a new function in `reporting/reporter.py`
2. Call this function from `main.py`

```python
def write_json_report(structured_data, schedule, schedule_analysis, output_file):
    """Write schedule report in JSON format"""
    report_data = {
        "statistics": {
            "total_requests": schedule_analysis['total_requests'],
            "resolved_requests": schedule_analysis['resolved_requests'],
            "resolution_rate": schedule_analysis.get('resolved_percentage', 0)
        },
        "priority_stats": schedule_analysis['priority_stats'],
        # Add more fields as needed
    }
    
    with open(output_file, 'w') as f:
        json.dump(report_data, f, indent=2)
```
