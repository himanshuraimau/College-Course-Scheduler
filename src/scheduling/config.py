"""
Configuration settings for the scheduling system.
"""
import os

def setup_paths():
    """Set up and return all file paths needed by the application"""
    BASE_DIR = '/home/himanshu/Downloads/test'
    
    # Input files
    STUDENT_REQUESTS_FILE = os.path.join(BASE_DIR, 'dataset.xlsx - Student requests.csv')
    COURSE_LIST_FILE = os.path.join(BASE_DIR, 'dataset.xlsx - Course list.csv')
    LECTURER_DETAILS_FILE = os.path.join(BASE_DIR, 'dataset.xlsx - Lecturer Details.csv')
    ROOMS_DATA_FILE = os.path.join(BASE_DIR, 'dataset.xlsx - Rooms data.csv')
    RULES_FILE = os.path.join(BASE_DIR, 'dataset.xlsx - RULES.csv')
    
    # Output directories
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
    DATA_DIR = os.path.join(OUTPUT_DIR, 'data')
    REPORT_DIR = os.path.join(OUTPUT_DIR, 'reports')
    VISUALIZATION_DIR = os.path.join(OUTPUT_DIR, 'visualizations')
    
    # Create directories if they don't exist
    for directory in [OUTPUT_DIR, DATA_DIR, REPORT_DIR, VISUALIZATION_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Output files
    OUTPUT_JSON_FILE = os.path.join(DATA_DIR, 'cleaned_data.json')
    ANALYSIS_REPORT_FILE = os.path.join(REPORT_DIR, 'analysis_report.md')
    
    return {
        'BASE_DIR': BASE_DIR,
        'STUDENT_REQUESTS_FILE': STUDENT_REQUESTS_FILE,
        'COURSE_LIST_FILE': COURSE_LIST_FILE,
        'LECTURER_DETAILS_FILE': LECTURER_DETAILS_FILE,
        'ROOMS_DATA_FILE': ROOMS_DATA_FILE,
        'RULES_FILE': RULES_FILE,
        'OUTPUT_DIR': OUTPUT_DIR,
        'DATA_DIR': DATA_DIR,
        'REPORT_DIR': REPORT_DIR,
        'VISUALIZATION_DIR': VISUALIZATION_DIR,
        'OUTPUT_JSON_FILE': OUTPUT_JSON_FILE,
        'ANALYSIS_REPORT_FILE': ANALYSIS_REPORT_FILE,
    }
