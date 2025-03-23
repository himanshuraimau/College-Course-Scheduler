# Crestwood College Course Scheduling System Overview

## Purpose

The Crestwood College Course Scheduling System automates the process of creating course schedules based on student preferences, teacher availability, classroom constraints, and block scheduling rules. The system aims to maximize student satisfaction by fulfilling as many course requests as possible while adhering to all scheduling constraints.

## System Architecture

The system follows a three-phase architecture:

1. **Data Preprocessing Phase**
   - Data cleaning and normalization
   - Conversion of raw data to structured JSON format
   - Data validation and analysis
   - Generation of insights and visualizations

2. **Scheduling Algorithm Phase**
   - Creation of course sections based on demand
   - Assignment of lecturers to course sections
   - Priority-based scheduling (Required → Requested → Recommended)
   - Block assignment with constraint satisfaction
   - Room allocation based on section size

3. **Reporting Phase**
   - Generation of comprehensive scheduling statistics
   - Visual representation of results (charts and graphs)
   - Creation of detailed reports
   - Analysis of scheduling effectiveness

## Key Components

### Data Processor (`scheduler.py`)
Handles data cleaning, normalization, and analysis. Converts raw CSV data into a structured JSON format suitable for the scheduling algorithm.

### Scheduler Algorithm (`scheduler_algorithm.py`)
Core scheduling engine that implements constraint satisfaction algorithms to produce optimal course schedules.

### Report Generator (`report_generator.py`)
Creates comprehensive reports and visualizations based on scheduling results.

### Main Runner (`run.py`)
Orchestrates the entire scheduling process by running each component in sequence.

## System Flow

1. Raw data is loaded from CSV files
2. Data is cleaned, normalized, and analyzed
3. Insights and potential conflicts are identified
4. Course sections are created based on demand
5. Lecturers are assigned to sections
6. Students are scheduled for required courses
7. Students are scheduled for requested courses
8. Students are scheduled for recommended courses
9. Rooms are assigned to course sections
10. Results are compiled and statistics are generated
11. Reports and visualizations are created

## Constraints and Rules

The system adheres to the following constraints:
- 7 block scheduling system: "1A", "1B", "2A", "2B", "3", "4A", "4B"
- No lecturer can teach multiple sections in the same block
- No student can be scheduled for multiple courses in the same block
- Courses can only be scheduled in their available blocks
- Section sizes must respect minimum, target, and maximum capacities
- Priority order: Required > Requested > Recommended
