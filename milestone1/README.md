# Milestone 1: Data Cleaning and Validation

## Approach

This milestone focuses on converting raw, unstructured data from Crestwood College into a structured JSON format and implementing validation checks to identify inconsistencies or missing data.

### Data Cleaning Process
1. Initial data extraction from CSV files (`dataset.xlsx - Student requests.csv`, course lists, lecturer details, rooms)
2. Data normalization and standardization (student IDs, course codes, etc.)
3. Structured conversion to JSON format (`cleaned_data.json`)
4. Data analysis and insights generation

### Validation Methodology
- Type checking for all data fields (student years, course credits, room capacities)
- Consistency validation between related entities
- Completeness checks for required fields
- Course demand analysis and conflict identification

## Key Findings

Based on the analysis report:
- Processed data for 156 students, 75 courses, 31 lecturers, and 29 rooms
- Identified request priorities: 178 required, 963 requested, 118 recommended courses
- Average of 8.07 course requests per student
- Identified top requested courses (LANSP2, BIB11, BIB10, etc.)
- Found potential scheduling conflicts in courses exceeding capacity

## Assumptions

- Course codes follow established patterns specific to Crestwood College
- The seven-block scheduling system is fixed and cannot be modified
- Priority levels (Required, Requested, Recommended) must be strictly adhered to
- Room capacities and constraints are accurately reflected in the source data

## Files Included

- `analysis_report.md` - Comprehensive report of data analysis and validation
- `cleaned_data.json` - Structured and normalized data extracted from sources
- Generated visualizations showing course demand and student distribution

## GitHub Repository

The code implementation for this milestone can be found at: https://github.com/himanshuraimau/College-Course-Scheduler
