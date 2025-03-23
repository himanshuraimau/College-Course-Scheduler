"""
Data validation functions for the scheduling system.
"""

def validate_data(structured_data):
    """Validate the structured data"""
    validation_results = {
        "valid": True,
        "issues": []
    }
    
    # Validate course data
    course_codes = set(course['code'] for course in structured_data['courses'])
    for student in structured_data['students']:
        for priority in ['required', 'requested', 'recommended']:
            for request in student['requests'].get(priority, []):
                if request['code'] not in course_codes and request['code']:
                    validation_results['issues'].append(
                        f"Student {student['id']} requested unknown course code: {request['code']}")
                    validation_results['valid'] = False
    
    # Check for missing data
    if not structured_data['courses']:
        validation_results['issues'].append("No course data available")
        validation_results['valid'] = False
        
    if not structured_data['students']:
        validation_results['issues'].append("No student data available")
        validation_results['valid'] = False
        
    if not structured_data['lecturers']:
        validation_results['issues'].append("No lecturer data available")
        validation_results['valid'] = False
    
    return validation_results
