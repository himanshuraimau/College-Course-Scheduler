"""
Reporting functions for the scheduling system.
"""
import os

def write_analysis_report(structured_data, validation_results, analysis_results, report_file):
    """Write analysis report to markdown file"""
    with open(report_file, 'w') as f:
        f.write("# Crestwood College Course Scheduling Analysis Report\n\n")
        
        # Data summary
        f.write("## Data Summary\n\n")
        f.write(f"- Number of Students: {len(structured_data['students'])}\n")
        f.write(f"- Number of Courses: {len(structured_data['courses'])}\n")
        f.write(f"- Number of Lecturers: {len(structured_data['lecturers'])}\n")
        f.write(f"- Number of Rooms: {len(structured_data['rooms'])}\n\n")
        
        # Validation results
        f.write("## Data Validation\n\n")
        f.write(f"Valid data: {'Yes' if validation_results['valid'] else 'No'}\n\n")
        if validation_results['issues']:
            f.write("### Issues Found\n\n")
            for issue in validation_results['issues']:
                f.write(f"- {issue}\n")
            f.write("\n")
        
        # Analysis insights
        f.write("## Data Insights\n\n")
        for insight in analysis_results.get('insights', []):
            f.write(f"- {insight}\n")
        f.write("\n")
        
        # Course demand
        f.write("## Course Demand Analysis\n\n")
        f.write("### Top 10 Most Requested Courses\n\n")
        f.write("| Course Code | Course Title | Required | Requested | Recommended | Total |\n")
        f.write("|------------|--------------|----------|-----------|-------------|-------|\n")
        
        course_demand = analysis_results.get('course_demand', {})
        top_courses = list(course_demand.keys())[:10]
        
        for course_code in top_courses:
            demand = course_demand[course_code]
            course_info = next((c for c in structured_data['courses'] if c['code'] == course_code), None)
            title = course_info['title'] if course_info else "Unknown"
            f.write(f"| {course_code} | {title} | {demand['required']} | {demand['requested']} | {demand['recommended']} | {demand['total']} |\n")
        
        f.write("\n")
        
        # Potential conflicts
        f.write("## Potential Scheduling Conflicts\n\n")
        conflicts = analysis_results.get('potential_conflicts', [])
        if conflicts:
            for conflict in conflicts:
                f.write(f"- {conflict}\n")
        else:
            f.write("No major scheduling conflicts identified.\n")
        
        # Visualizations
        f.write("\n## Visualizations\n\n")
        f.write("### Course Demand by Priority\n\n")
        f.write("![Course Demand](../visualizations/course_demand.png)\n\n")
        f.write("### Student Distribution by Year\n\n")
        f.write("![Student Years](../visualizations/student_years.png)\n\n")

def write_schedule_report(structured_data, schedule, schedule_analysis, report_dir):
    """Write the schedule report to a markdown file"""
    report_file = os.path.join(report_dir, 'schedule_report.md')
    
    with open(report_file, 'w') as f:
        f.write("# Crestwood College Course Schedule Report\n\n")
        
        # Overall statistics
        f.write("## Overall Schedule Statistics\n\n")
        f.write(f"- Total Requests: {schedule_analysis['total_requests']}\n")
        f.write(f"- Resolved Requests: {schedule_analysis['resolved_requests']} ({schedule_analysis.get('resolved_percentage', 0):.1f}%)\n")
        f.write(f"- Unresolved Requests: {schedule_analysis['unresolved_requests']} ({schedule_analysis.get('unresolved_percentage', 0):.1f}%)\n\n")
        
        # Priority statistics
        f.write("## Resolution by Priority\n\n")
        f.write("| Priority | Total | Resolved | Resolution Rate |\n")
        f.write("|----------|-------|----------|----------------|\n")
        
        for priority in ['required', 'requested', 'recommended']:
            stats = schedule_analysis['priority_stats'][priority]
            percentage = stats.get('percentage', 0)
            f.write(f"| {priority.capitalize()} | {stats['total']} | {stats['resolved']} | {percentage:.1f}% |\n")
        
        f.write("\n")
        
        # Student view sample
        f.write("## Student Schedule View (Sample)\n\n")
        
        sample_students = list(schedule['student_schedules'].keys())[:5]  # First 5 students
        
        for student_id in sample_students:
            student_info = next((s for s in structured_data['students'] if s['id'] == student_id), None)
            if student_info:
                f.write(f"### Student {student_id} (Year {student_info['year']})\n\n")
                f.write("| Block | Course Code | Course Title |\n")
                f.write("|-------|-------------|-------------|\n")
                
                student_schedule = schedule['student_schedules'][student_id]
                for block in sorted(structured_data['blocks']):
                    course_code = student_schedule.get(block, "")
                    course_title = ""
                    if course_code:
                        course_info = next((c for c in structured_data['courses'] if c['code'] == course_code), None)
                        if course_info:
                            course_title = course_info['title']
                    
                    f.write(f"| {block} | {course_code} | {course_title} |\n")
                
                f.write("\n")
        
        # Teacher view sample
        f.write("## Lecturer Schedule View (Sample)\n\n")
        
        sample_lecturers = list(schedule['lecturer_schedules'].keys())[:5]  # First 5 lecturers
        
        for lecturer_id in sample_lecturers:
            lecturer_info = next((l for l in structured_data['lecturers'] if l['id'] == lecturer_id), None)
            if lecturer_info:
                f.write(f"### {lecturer_info['name']} (ID: {lecturer_id})\n\n")
                f.write("| Block | Course Code | Course Title | Room |\n")
                f.write("|-------|-------------|-------------|------|\n")
                
                lecturer_schedule = schedule['lecturer_schedules'][lecturer_id]
                for block in sorted(structured_data['blocks']):
                    course_code = lecturer_schedule.get(block, "")
                    course_title = ""
                    room_id = ""
                    
                    if course_code:
                        course_info = next((c for c in structured_data['courses'] if c['code'] == course_code), None)
                        if course_info:
                            course_title = course_info['title']
                        
                        room_id = schedule['course_rooms'].get(course_code, {}).get(block, "")
                    
                    f.write(f"| {block} | {course_code} | {course_title} | {room_id} |\n")
                
                f.write("\n")
        
        # Top courses by resolution rate
        f.write("## Top Courses by Resolution Rate\n\n")
        f.write("| Course Code | Total Requests | Resolved | Resolution Rate |\n")
        f.write("|-------------|----------------|----------|----------------|\n")
        
        top_courses = list(schedule_analysis['course_resolution_rates'].keys())[:10]  # Top 10
        
        for course_code in top_courses:
            stats = schedule_analysis['course_stats'][course_code]
            resolution_rate = schedule_analysis['course_resolution_rates'][course_code]
            
            # Get course title
            course_title = ""
            course_info = next((c for c in structured_data['courses'] if c['code'] == course_code), None)
            if course_info:
                course_title = course_info['title']
            
            f.write(f"| {course_code} ({course_title}) | {stats['total']} | {stats['resolved']} | {resolution_rate:.1f}% |\n")
        
        f.write("\n")
        
        # Visualizations
        f.write("## Schedule Visualizations\n\n")
        f.write("### Overall Request Resolution\n\n")
        f.write("![Request Resolution](../visualizations/request_resolution.png)\n\n")
        f.write("### Request Resolution by Priority\n\n")
        f.write("![Priority Resolution](../visualizations/priority_resolution.png)\n\n")
        f.write("### Course Request Resolution Rates\n\n")
        f.write("![Course Resolution Rates](../visualizations/course_resolution_rates.png)\n\n")
