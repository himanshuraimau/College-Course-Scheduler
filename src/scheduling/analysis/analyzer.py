"""
Data analysis functions for the scheduling system.
"""
from collections import defaultdict

def analyze_data(structured_data):
    """Analyze the structured data for insights"""
    analysis = {
        "course_demand": {},
        "block_constraints": {},
        "potential_conflicts": [],
        "insights": []
    }
    
    # Count course demand by priority
    course_demand = defaultdict(lambda: {"required": 0, "requested": 0, "recommended": 0, "total": 0})
    for student in structured_data['students']:
        for priority in ['required', 'requested', 'recommended']:
            for request in student['requests'].get(priority, []):
                course_code = request['code']
                course_demand[course_code][priority] += 1
                course_demand[course_code]['total'] += 1
    
    # Sort by total demand
    sorted_demand = {k: v for k, v in sorted(
        course_demand.items(), 
        key=lambda item: item[1]['total'], 
        reverse=True
    )}
    analysis['course_demand'] = sorted_demand
    
    # Top 10 most requested courses
    top_courses = list(sorted_demand.keys())[:10]
    analysis['insights'].append(f"Top 10 most requested courses: {', '.join(top_courses)}")
    
    # Count requests by priority
    priority_counts = {
        "required": sum(course['required'] for course in course_demand.values()),
        "requested": sum(course['requested'] for course in course_demand.values()),
        "recommended": sum(course['recommended'] for course in course_demand.values())
    }
    analysis['insights'].append(
        f"Request priorities: {priority_counts['required']} required, "
        f"{priority_counts['requested']} requested, {priority_counts['recommended']} recommended"
    )
    
    # Analyze potential scheduling bottlenecks
    for course_code, demand in sorted_demand.items():
        # Find the corresponding course in structured data
        course_info = next((c for c in structured_data['courses'] if c['code'] == course_code), None)
        if course_info:
            max_capacity = course_info['max_size'] * course_info.get('num_sections', 1)
            if demand['total'] > max_capacity:
                analysis['potential_conflicts'].append(
                    f"Course {course_code} has demand of {demand['total']} but capacity of only {max_capacity}"
                )
    
    # Analyze student course load
    course_counts = [sum(len(student['requests'][p]) for p in ['required', 'requested', 'recommended']) 
                     for student in structured_data['students']]
    avg_courses = sum(course_counts) / len(course_counts) if course_counts else 0
    analysis['insights'].append(f"Average courses requested per student: {avg_courses:.2f}")
    
    return analysis

def analyze_schedule_results(structured_data, schedule):
    """Analyze the results of the scheduling algorithm"""
    results = {
        'total_requests': 0,
        'resolved_requests': 0,
        'unresolved_requests': 0,
        'priority_stats': {
            'required': {'total': 0, 'resolved': 0},
            'requested': {'total': 0, 'resolved': 0},
            'recommended': {'total': 0, 'resolved': 0}
        },
        'course_stats': defaultdict(lambda: {'total': 0, 'resolved': 0, 'unresolved': 0})
    }
    
    # Count requests and resolutions
    for student in structured_data['students']:
        student_id = student['id']
        student_schedule = schedule['student_schedules'].get(student_id, {})
        
        for priority in ['required', 'requested', 'recommended']:
            for req in student['requests'][priority]:
                course_code = req['code']
                results['total_requests'] += 1
                results['priority_stats'][priority]['total'] += 1
                results['course_stats'][course_code]['total'] += 1
                
                # Check if this course is in the student's schedule
                is_scheduled = False
                for block, scheduled_course in student_schedule.items():
                    if scheduled_course == course_code:
                        is_scheduled = True
                        break
                
                if is_scheduled:
                    results['resolved_requests'] += 1
                    results['priority_stats'][priority]['resolved'] += 1
                    results['course_stats'][course_code]['resolved'] += 1
                else:
                    results['unresolved_requests'] += 1
                    results['course_stats'][course_code]['unresolved'] += 1
    
    # Calculate percentages
    if results['total_requests'] > 0:
        results['resolved_percentage'] = (results['resolved_requests'] / results['total_requests']) * 100
        results['unresolved_percentage'] = (results['unresolved_requests'] / results['total_requests']) * 100
    
    for priority in ['required', 'requested', 'recommended']:
        if results['priority_stats'][priority]['total'] > 0:
            results['priority_stats'][priority]['percentage'] = (
                results['priority_stats'][priority]['resolved'] / 
                results['priority_stats'][priority]['total']
            ) * 100
    
    # Sort courses by resolution rate
    course_resolution_rates = {}
    for course_code, stats in results['course_stats'].items():
        if stats['total'] > 0:
            course_resolution_rates[course_code] = (stats['resolved'] / stats['total']) * 100
    
    results['course_resolution_rates'] = {
        k: v for k, v in sorted(
            course_resolution_rates.items(), 
            key=lambda item: item[1], 
            reverse=True
        )
    }
    
    return results
