"""
Main module for Crestwood College course scheduling system.
This is the entry point that orchestrates the scheduling process.
"""
import os
import sys

# Fix the import paths for relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Set up error handling
try:
    from src.scheduling.utils.error_handler import setup_error_handling
    setup_error_handling()
except ImportError:
    print("Warning: Error handling module not found.")

# Import modules from the modular structure
try:
    from src.scheduling.config import setup_paths
    from src.scheduling.data import loader, processor
    from src.scheduling.analysis import validator, analyzer
    from src.scheduling.visualization import visualizer
    from src.scheduling.scheduling import optimizer
    from src.scheduling.reporting import reporter
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please make sure all required modules are installed and the project structure is correct.")
    sys.exit(1)

def main():
    """Main function to execute the scheduling plan"""
    print("Starting Crestwood College course scheduling process...")
    
    # Setup paths
    paths = setup_paths()
    
    # Step 1: Load and clean data
    print("Loading student request data...")
    student_requests_df = loader.load_student_requests(paths['STUDENT_REQUESTS_FILE'])
    
    # Step 2: Extract and structure course data from student requests
    print("Extracting course information...")
    courses = processor.extract_course_info_from_requests(student_requests_df)
    
    # Step 3: Structure student request data
    print("Structuring student request data...")
    students = processor.structure_student_requests(student_requests_df)
    
    # Step 4: Create mock data for missing information
    print("Creating mock lecturer data...")
    lecturers = processor.create_mock_lecturer_data(courses)
    
    print("Creating mock room data...")
    rooms = processor.create_mock_rooms_data()
    
    # Step 5: Create structured JSON
    structured_data = {
        "courses": courses,
        "students": students,
        "lecturers": lecturers,
        "rooms": rooms,
        "blocks": ["1A", "1B", "2A", "2B", "3", "4A", "4B"]
    }
    
    # Step 6: Validate data
    print("Validating data...")
    validation_results = validator.validate_data(structured_data)
    
    # Step 7: Analyze data
    print("Analyzing data...")
    analysis_results = analyzer.analyze_data(structured_data)
    
    # Step 8: Generate visualizations
    print("Generating visualizations...")
    visualizer.generate_data_visualizations(structured_data, analysis_results, paths['VISUALIZATION_DIR'])
    
    # Step 9: Write analysis report
    print("Writing analysis report...")
    reporter.write_analysis_report(structured_data, validation_results, analysis_results, paths['ANALYSIS_REPORT_FILE'])
    
    # Step 10: Save structured data to JSON file
    print(f"Saving structured data to {paths['OUTPUT_JSON_FILE']}...")
    processor.save_structured_data(structured_data, paths['OUTPUT_JSON_FILE'])
    
    print("Course scheduling preparation completed!")
    print(f"- Cleaned data saved to: {paths['OUTPUT_JSON_FILE']}")
    print(f"- Analysis report saved to: {paths['ANALYSIS_REPORT_FILE']}")
    print(f"- Visualizations saved to: {paths['VISUALIZATION_DIR']}")

    # Step 11: Create the course schedule
    print("Creating course schedule...")
    schedule = optimizer.create_course_schedule(structured_data)
    
    # Step 12: Analyze the schedule results
    print("Analyzing schedule results...")
    schedule_analysis = analyzer.analyze_schedule_results(structured_data, schedule)
    
    # Step 13: Generate schedule visualizations
    print("Generating schedule visualizations...")
    visualizer.generate_schedule_visualizations(structured_data, schedule, schedule_analysis, paths['VISUALIZATION_DIR'])
    
    # Step 14: Write schedule report
    print("Writing schedule report...")
    reporter.write_schedule_report(structured_data, schedule, schedule_analysis, paths['REPORT_DIR'])
    
    # Save the schedule to a JSON file
    schedule_json_file = os.path.join(paths['DATA_DIR'], 'schedule.json')
    print(f"Saving schedule to {schedule_json_file}...")
    processor.save_schedule_data(schedule, schedule_json_file)
    
    print("Course scheduling completed!")
    print(f"- Schedule data saved to: {schedule_json_file}")
    print(f"- Schedule report saved to: {os.path.join(paths['REPORT_DIR'], 'schedule_report.md')}")
    print(f"- Schedule visualizations saved to: {paths['VISUALIZATION_DIR']}")

if __name__ == "__main__":
    main()
