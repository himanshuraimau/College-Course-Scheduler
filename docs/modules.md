# Module Reference

## Data Module

The `data` module handles data loading, cleaning, and processing.

### loader.py

Functions for loading data from external sources:

- `load_student_requests(file_path)`: Loads and normalizes student request data from CSV

### processor.py

Functions for processing and transforming data:

- `extract_course_info_from_requests(df)`: Extracts course information from request data
- `structure_student_requests(df)`: Creates structured student data
- `create_mock_lecturer_data(courses)`: Creates lecturer data based on courses
- `create_mock_rooms_data()`: Creates mock room data
- `convert_numpy_types(obj)`: Converts numpy types to native Python types
- `save_structured_data(structured_data, output_file)`: Saves data to JSON
- `save_schedule_data(schedule, output_file)`: Saves schedule to JSON

## Analysis Module

The `analysis` module contains functions for data validation and analysis.

### validator.py

Functions for validating data:

- `validate_data(structured_data)`: Validates the structured data for completeness and consistency

### analyzer.py

Functions for analyzing data:

- `analyze_data(structured_data)`: Analyzes data for insights
- `analyze_schedule_results(structured_data, schedule)`: Analyzes the scheduling results

## Visualization Module

The `visualization` module creates visual representations of data.

### visualizer.py

Functions for generating visualizations:

- `generate_data_visualizations(structured_data, analysis_data, visualization_dir)`: Generates data analysis visualizations
- `generate_schedule_visualizations(structured_data, schedule, schedule_analysis, visualization_dir)`: Generates schedule visualizations

## Scheduling Module

The `scheduling` module implements the core scheduling algorithm.

### optimizer.py

Functions for optimizing course schedules:

- `create_course_schedule(structured_data)`: Creates an optimal course schedule using linear programming

## Reporting Module

The `reporting` module generates reports from the data and results.

### reporter.py

Functions for generating reports:

- `write_analysis_report(structured_data, validation_results, analysis_results, report_file)`: Writes data analysis report
- `write_schedule_report(structured_data, schedule, schedule_analysis, report_dir)`: Writes schedule report
