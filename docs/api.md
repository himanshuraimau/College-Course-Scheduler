# API Reference

This document provides details on the core functions and their parameters for developers working with the codebase.

## Configuration API

### config.setup_paths()

Sets up and returns file paths needed by the application.

**Returns:**
- Dictionary containing all necessary file and directory paths

## Data API

### loader.load_student_requests(file_path)

Loads and cleans student request data from CSV file.

**Parameters:**
- `file_path` (str): Path to the CSV file

**Returns:**
- Pandas DataFrame containing cleaned student requests

### processor.extract_course_info_from_requests(df)

Extracts unique course information from student requests.

**Parameters:**
- `df` (DataFrame): The student requests dataframe

**Returns:**
- List of dictionaries containing course information

### processor.structure_student_requests(df)

Creates structured student data from request data frame.

**Parameters:**
- `df` (DataFrame): The student requests dataframe

**Returns:**
- List of dictionaries containing student information and requests

### processor.save_structured_data(structured_data, output_file)

Saves structured data to JSON file.

**Parameters:**
- `structured_data` (dict): The data to save
- `output_file` (str): Path to the output file

### processor.save_schedule_data(schedule, output_file)

Saves schedule data to JSON file.

**Parameters:**
- `schedule` (dict): The schedule data to save
- `output_file` (str): Path to the output file

## Analysis API

### validator.validate_data(structured_data)

Validates the structured data.

**Parameters:**
- `structured_data` (dict): The structured data to validate

**Returns:**
- Dictionary containing validation results and issues

### analyzer.analyze_data(structured_data)

Analyzes the structured data for insights.

**Parameters:**
- `structured_data` (dict): The structured data to analyze

**Returns:**
- Dictionary containing analysis results

### analyzer.analyze_schedule_results(structured_data, schedule)

Analyzes the results of the scheduling algorithm.

**Parameters:**
- `structured_data` (dict): The structured data
- `schedule` (dict): The schedule to analyze

**Returns:**
- Dictionary containing schedule analysis results

## Scheduling API

### optimizer.create_course_schedule(structured_data)

Creates an optimal course schedule using linear programming.

**Parameters:**
- `structured_data` (dict): The structured data to use for scheduling

**Returns:**
- Dictionary containing the optimized schedule

## Visualization API

### visualizer.generate_data_visualizations(structured_data, analysis_data, visualization_dir)

Generates visualizations for the data.

**Parameters:**
- `structured_data` (dict): The structured data
- `analysis_data` (dict): The analysis results
- `visualization_dir` (str): Directory to save visualizations

### visualizer.generate_schedule_visualizations(structured_data, schedule, schedule_analysis, visualization_dir)

Generates visualizations for the schedule results.

**Parameters:**
- `structured_data` (dict): The structured data
- `schedule` (dict): The generated schedule
- `schedule_analysis` (dict): The schedule analysis results
- `visualization_dir` (str): Directory to save visualizations

## Reporting API

### reporter.write_analysis_report(structured_data, validation_results, analysis_results, report_file)

Writes analysis report to markdown file.

**Parameters:**
- `structured_data` (dict): The structured data
- `validation_results` (dict): The validation results
- `analysis_results` (dict): The analysis results
- `report_file` (str): Path to the output report file

### reporter.write_schedule_report(structured_data, schedule, schedule_analysis, report_dir)

Writes schedule report to markdown file.

**Parameters:**
- `structured_data` (dict): The structured data
- `schedule` (dict): The generated schedule
- `schedule_analysis` (dict): The schedule analysis results 
- `report_dir` (str): Directory to save the report
