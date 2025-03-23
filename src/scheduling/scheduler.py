import pandas as pd
import json
import numpy as np
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import pulp  # Add this import for the linear programming solver

# Define file paths
BASE_DIR = '/home/himanshu/Downloads/test'
STUDENT_REQUESTS_FILE = os.path.join(BASE_DIR, 'dataset.xlsx - Student requests.csv')
COURSE_LIST_FILE = os.path.join(BASE_DIR, 'dataset.xlsx - Course list.csv')
LECTURER_DETAILS_FILE = os.path.join(BASE_DIR, 'dataset.xlsx - Lecturer Details.csv')
ROOMS_DATA_FILE = os.path.join(BASE_DIR, 'dataset.xlsx - Rooms data.csv')
RULES_FILE = os.path.join(BASE_DIR, 'dataset.xlsx - RULES.csv')

# Create output directories
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
DATA_DIR = os.path.join(OUTPUT_DIR, 'data')
REPORT_DIR = os.path.join(OUTPUT_DIR, 'reports')
VISUALIZATION_DIR = os.path.join(OUTPUT_DIR, 'visualizations')

# Create directories if they don't exist
for directory in [OUTPUT_DIR, DATA_DIR, REPORT_DIR, VISUALIZATION_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Update output file paths
OUTPUT_JSON_FILE = os.path.join(DATA_DIR, 'cleaned_data.json')
ANALYSIS_REPORT_FILE = os.path.join(REPORT_DIR, 'analysis_report.md')

def load_student_requests(file_path):
    """Load and clean student request data"""
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded {len(df)} student requests")
        
        # Clean and normalize column names
        df.columns = [col.strip() for col in df.columns]
        
        # Convert student IDs to strings
        df['student ID'] = df['student ID'].astype(str)
        
        # Normalize priority values
        priority_map = {'Required': 'required', 'Requested': 'requested', 'Recommended': 'recommended'}
        df['Priority'] = df['Type'].map(priority_map)
        
        return df
    except Exception as e:
        print(f"Error loading student requests: {e}")
        return pd.DataFrame()

def extract_course_info_from_requests(df):
    """Extract unique course information from student requests"""
    if df.empty:
        return []
    
    unique_courses = df.drop_duplicates(subset=['Course code', 'Title']).copy()
    courses = []
    
    for _, row in unique_courses.iterrows():
        # Extract available blocks (placeholder - would come from course list file)
        available_blocks = ["1A", "1B", "2A", "2B", "3", "4A", "4B"]
        
        course = {
            "code": row['Course code'],
            "title": row['Title'],
            "length": row['Length'],
            "priority": row['Priority'],
            "available_blocks": available_blocks,
            "unavailable_blocks": [],
            "min_size": 5,   # Default minimum size
            "target_size": 20,  # Default target size
            "max_size": 40,  # Default maximum size
            "num_sections": 1,  # Default number of sections
            "credits": row['Credits'],
            "department": row['Department(s)']
        }
        courses.append(course)
    
    return courses

def structure_student_requests(df):
    """Create structured student data from request data frame"""
    if df.empty:
        return []
    
    students = defaultdict(lambda: {"year": "", "requests": {"required": [], "requested": [], "recommended": []}})
    
    for _, row in df.iterrows():
        student_id = row['student ID']
        students[student_id]["year"] = row['College Year']
        
        request = {
            "code": row['Course code'],
            "title": row['Title'],
            "length": row['Length'],
            "term": row['Request start term']
        }
        
        priority = row['Priority'].lower()
        students[student_id]["requests"][priority].append(request)
    
    # Convert to list format for JSON
    result = []
    for student_id, data in students.items():
        student_data = {
            "id": student_id,
            "year": data["year"],
            "requests": data["requests"]
        }
        result.append(student_data)
    
    return result

def create_mock_lecturer_data(courses):
    """Create mock lecturer data based on courses"""
    lecturers = []
    lecturer_id_base = 1000
    
    # Group courses by department to assign to lecturers
    dept_courses = defaultdict(list)
    for course in courses:
        dept = course.get("department", "General")
        dept_courses[dept].append(course)
    
    for dept, dept_course_list in dept_courses.items():
        # Create 1-3 lecturers per department
        num_lecturers = min(len(dept_course_list), 3)
        num_lecturers = max(num_lecturers, 1)
        
        for i in range(num_lecturers):
            lecturer_id = str(lecturer_id_base + i)
            lecturer_courses = []
            
            # Assign courses to this lecturer
            for j, course in enumerate(dept_course_list):
                if j % num_lecturers == i:  # Distribute courses evenly among lecturers
                    lecturer_courses.append({
                        "code": course["code"],
                        "title": course["title"],
                        "length": course["length"],
                        "section": 1
                    })
            
            lecturers.append({
                "id": lecturer_id,
                "name": f"Professor {dept}_{i+1}",
                "department": dept,
                "courses": lecturer_courses
            })
        
        lecturer_id_base += 10  # Increment for next department
    
    return lecturers

def create_mock_rooms_data():
    """Create mock room data"""
    rooms = []
    room_numbers = list(range(101, 130))
    
    for room_num in room_numbers:
        capacity = np.random.choice([20, 25, 30, 35, 40])
        room_type = np.random.choice(["Standard", "Lab", "Studio", "Lecture Hall"], 
                                     p=[0.7, 0.1, 0.1, 0.1])
        
        rooms.append({
            "room_number": str(room_num),
            "capacity": capacity,
            "type": room_type,
            "building": "Main Building"
        })
    
    return rooms

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

def generate_visualizations(structured_data, analysis_data):
    """Generate visualizations for the data"""
    # Course demand by priority
    if analysis_data['course_demand']:
        plt.figure(figsize=(12, 8))
        top_courses = list(analysis_data['course_demand'].keys())[:15]  # Top 15 courses
        
        required = [analysis_data['course_demand'][course]['required'] for course in top_courses]
        requested = [analysis_data['course_demand'][course]['requested'] for course in top_courses]
        recommended = [analysis_data['course_demand'][course]['recommended'] for course in top_courses]
        
        x = np.arange(len(top_courses))
        width = 0.25
        
        plt.bar(x - width, required, width, label='Required')
        plt.bar(x, requested, width, label='Requested')
        plt.bar(x + width, recommended, width, label='Recommended')
        
        plt.xticks(x, top_courses, rotation=90)
        plt.xlabel('Course Code')
        plt.ylabel('Number of Requests')
        plt.title('Course Demand by Priority Type')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALIZATION_DIR, 'course_demand.png'))
        plt.close()
    
    # Student year distribution
    if structured_data['students']:
        years = [student['year'] for student in structured_data['students']]
        year_counts = Counter(years)
        
        plt.figure(figsize=(10, 6))
        plt.bar(year_counts.keys(), year_counts.values())
        plt.xlabel('College Year')
        plt.ylabel('Number of Students')
        plt.title('Student Distribution by Year')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALIZATION_DIR, 'student_years.png'))
        plt.close()

def write_analysis_report(structured_data, validation_results, analysis_results):
    """Write analysis report to markdown file"""
    with open(ANALYSIS_REPORT_FILE, 'w') as f:
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

# Add this helper function to convert numpy types to native Python types
def convert_numpy_types(obj):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(i) for i in obj]
    else:
        return obj

def create_course_schedule(structured_data):
    """
    Create a course schedule based on student requests and constraints
    using PuLP linear programming solver
    """
    print("Creating course schedule...")
    
    # Extract data
    courses = structured_data['courses']
    students = structured_data['students']
    lecturers = structured_data['lecturers']
    rooms = structured_data['rooms']
    blocks = structured_data['blocks']
    
    # Create problem instance
    prob = pulp.LpProblem("CourseScheduling", pulp.LpMaximize)
    
    # Decision variables
    # x[student_id, course_code, block] = 1 if student is assigned to course in block
    x = {}
    for student in students:
        student_id = student['id']
        # Collect all course requests for the student
        requested_courses = []
        for priority in ['required', 'requested', 'recommended']:
            for course_req in student['requests'][priority]:
                requested_courses.append(course_req['code'])
        
        for course_code in requested_courses:
            for block in blocks:
                x[(student_id, course_code, block)] = pulp.LpVariable(
                    f"x_{student_id}_{course_code}_{block}", 
                    cat='Binary'
                )
    
    # y[course_code, block, room_id] = 1 if course is scheduled in block at room
    y = {}
    for course in courses:
        course_code = course['code']
        for block in blocks:
            for room in rooms:
                room_id = room['room_number']
                y[(course_code, block, room_id)] = pulp.LpVariable(
                    f"y_{course_code}_{block}_{room_id}",
                    cat='Binary'
                )
    
    # Objective function: maximize fulfilled requests with priority weights
    priority_weights = {'required': 10, 'requested': 5, 'recommended': 1}
    objective = 0
    
    for student in students:
        student_id = student['id']
        for priority in ['required', 'requested', 'recommended']:
            weight = priority_weights[priority]
            for course_req in student['requests'][priority]:
                course_code = course_req['code']
                # Sum over all blocks where this course could be scheduled for this student
                for block in blocks:
                    objective += weight * x[(student_id, course_code, block)]
    
    prob += objective
    
    # Constraints
    
    # 1. Student can't be in two places at once
    for student in students:
        student_id = student['id']
        for block in blocks:
            prob += pulp.lpSum(x[(student_id, course_code, block)] 
                              for course_code in [req['code'] 
                                               for priority in ['required', 'requested', 'recommended'] 
                                               for req in student['requests'][priority]]
                              if (student_id, course_code, block) in x) <= 1
    
    # 2. Course can only be scheduled in one room per block
    for course in courses:
        course_code = course['code']
        for block in blocks:
            prob += pulp.lpSum(y[(course_code, block, room['room_number'])] for room in rooms) <= 1
    
    # 3. Room can only have one course per block
    for room in rooms:
        room_id = room['room_number']
        for block in blocks:
            prob += pulp.lpSum(y[(course_code, block, room_id)] for course_code in [c['code'] for c in courses]) <= 1
    
    # 4. Student can only be assigned to a course if it's scheduled
    for student in students:
        student_id = student['id']
        student_courses = []
        for priority in ['required', 'requested', 'recommended']:
            student_courses.extend([req['code'] for req in student['requests'][priority]])
            
        for course_code in student_courses:
            for block in blocks:
                prob += x[(student_id, course_code, block)] <= pulp.lpSum(
                    y[(course_code, block, room['room_number'])] for room in rooms
                )
    
    # 5. Respect room capacity
    for course in courses:
        course_code = course['code']
        for block in blocks:
            for room in rooms:
                room_id = room['room_number']
                room_capacity = room['capacity']
                # Number of students assigned to this course in this block
                student_count = pulp.lpSum(x[(student_id, course_code, block)] 
                                         for student in students 
                                         for priority in ['required', 'requested', 'recommended']
                                         for req in student['requests'][priority] if req['code'] == course_code
                                         if (student_id, course_code, block) in x)
                
                # If course is scheduled in this room, enforce capacity
                prob += student_count <= room_capacity * y[(course_code, block, room_id)]
    
    # 6. Respect course minimum and maximum size
    for course in courses:
        course_code = course['code']
        min_size = course['min_size']
        max_size = course['max_size']
        
        for block in blocks:
            # Is this course scheduled in any room in this block?
            is_scheduled = pulp.lpSum(y[(course_code, block, room['room_number'])] for room in rooms)
            
            # Number of students in this course in this block
            student_count = pulp.lpSum(x[(student_id, course_code, block)] 
                                     for student in students 
                                     if (student_id, course_code, block) in x)
            
            # If course is scheduled, enforce min and max size
            prob += student_count >= min_size * is_scheduled
            prob += student_count <= max_size * is_scheduled
    
    # Solve the problem
    print("Solving the scheduling problem...")
    solver = pulp.PULP_CBC_CMD(msg=True, timeLimit=300)  # Limit solve time to 5 minutes
    prob.solve(solver)
    
    if pulp.LpStatus[prob.status] != 'Optimal':
        print(f"Warning: Could not find optimal solution. Status: {pulp.LpStatus[prob.status]}")
    
    # Extract the schedule from the solution
    schedule = {
        'course_blocks': defaultdict(list),  # course_code -> list of blocks
        'course_rooms': defaultdict(dict),   # course_code -> {block: room_id}
        'student_schedules': defaultdict(dict),  # student_id -> {block: course_code}
        'room_schedules': defaultdict(dict),     # room_id -> {block: course_code}
        'lecturer_schedules': defaultdict(dict)  # lecturer_id -> {block: course_code}
    }
    
    # Extract scheduled courses
    for course in courses:
        course_code = course['code']
        for block in blocks:
            for room in rooms:
                room_id = room['room_number']
                if (course_code, block, room_id) in y and pulp.value(y[(course_code, block, room_id)]) > 0.5:
                    schedule['course_blocks'][course_code].append(block)
                    schedule['course_rooms'][course_code][block] = room_id
                    schedule['room_schedules'][room_id][block] = course_code
    
    # Extract student assignments
    for student in students:
        student_id = student['id']
        for priority in ['required', 'requested', 'recommended']:
            for course_req in student['requests'][priority]:
                course_code = course_req['code']
                for block in blocks:
                    if (student_id, course_code, block) in x and pulp.value(x[(student_id, course_code, block)]) > 0.5:
                        schedule['student_schedules'][student_id][block] = course_code
    
    # Assign lecturers based on their course assignments
    for lecturer in lecturers:
        lecturer_id = lecturer['id']
        lecturer_courses = [course['code'] for course in lecturer['courses']]
        
        for course_code in lecturer_courses:
            if course_code in schedule['course_blocks']:
                for block in schedule['course_blocks'][course_code]:
                    schedule['lecturer_schedules'][lecturer_id][block] = course_code
    
    return schedule

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

def generate_schedule_visualizations(structured_data, schedule, schedule_analysis):
    """Generate visualizations for the schedule results"""
    
    # 1. Priority fulfillment pie chart
    plt.figure(figsize=(10, 8))
    labels = ['Resolved', 'Unresolved']
    sizes = [
        schedule_analysis['resolved_requests'],
        schedule_analysis['unresolved_requests']
    ]
    explode = (0.1, 0)  # explode the 1st slice
    
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Request Resolution Status')
    plt.savefig(os.path.join(VISUALIZATION_DIR, 'request_resolution.png'))
    plt.close()
    
    # 2. Priority-wise resolution bar chart
    plt.figure(figsize=(10, 6))
    priorities = ['Required', 'Requested', 'Recommended']
    resolved = [
        schedule_analysis['priority_stats']['required']['resolved'],
        schedule_analysis['priority_stats']['requested']['resolved'],
        schedule_analysis['priority_stats']['recommended']['resolved']
    ]
    unresolved = [
        schedule_analysis['priority_stats']['required']['total'] - schedule_analysis['priority_stats']['required']['resolved'],
        schedule_analysis['priority_stats']['requested']['total'] - schedule_analysis['priority_stats']['requested']['resolved'],
        schedule_analysis['priority_stats']['recommended']['total'] - schedule_analysis['priority_stats']['recommended']['resolved']
    ]
    
    x = np.arange(len(priorities))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, resolved, width, label='Resolved')
    rects2 = ax.bar(x + width/2, unresolved, width, label='Unresolved')
    
    ax.set_xlabel('Priority')
    ax.set_ylabel('Number of Requests')
    ax.set_title('Request Resolution by Priority')
    ax.set_xticks(x)
    ax.set_xticklabels(priorities)
    ax.legend()
    
    # Add resolution percentage labels on bars
    for i, priority in enumerate(['required', 'requested', 'recommended']):
        if schedule_analysis['priority_stats'][priority]['total'] > 0:
            percentage = schedule_analysis['priority_stats'][priority]['percentage']
            ax.annotate(f'{percentage:.1f}%',
                       xy=(x[i] - width/2, resolved[i]),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(VISUALIZATION_DIR, 'priority_resolution.png'))
    plt.close()
    
    # 3. Course resolution heatmap
    # Get top 20 courses by request volume
    course_stats = schedule_analysis['course_stats']
    top_courses = sorted(course_stats.keys(), key=lambda k: course_stats[k]['total'], reverse=True)[:20]
    
    # Create a dictionary for the heatmap
    heatmap_data = {
        'Course Code': [],
        'Total Requests': [],
        'Resolved Requests': [],
        'Resolution Rate (%)': []
    }
    
    for course_code in top_courses:
        stats = course_stats[course_code]
        if stats['total'] > 0:
            resolution_rate = (stats['resolved'] / stats['total']) * 100
        else:
            resolution_rate = 0
            
        heatmap_data['Course Code'].append(course_code)
        heatmap_data['Total Requests'].append(stats['total'])
        heatmap_data['Resolved Requests'].append(stats['resolved'])
        heatmap_data['Resolution Rate (%)'].append(resolution_rate)
    
    # Convert to DataFrame for seaborn
    df = pd.DataFrame(heatmap_data)
    
    # Pivot the dataframe for the heatmap
    pivot_df = df.pivot_table(
        index='Course Code',
        values=['Total Requests', 'Resolved Requests', 'Resolution Rate (%)']
    )
    
    # Create the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_df, annot=True, cmap="YlGnBu", fmt=".1f")
    plt.title('Course Request Resolution Rates')
    plt.tight_layout()
    plt.savefig(os.path.join(VISUALIZATION_DIR, 'course_resolution_rates.png'))
    plt.close()

def write_schedule_report(structured_data, schedule, schedule_analysis):
    """Write the schedule report to a markdown file"""
    report_file = os.path.join(REPORT_DIR, 'schedule_report.md')
    
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

# Update the main function to include the new scheduling functionality
def main():
    """Main function to execute the scheduling plan"""
    print("Starting Crestwood College course scheduling process...")
    
    # Step 1: Load and clean data
    print("Loading student request data...")
    student_requests_df = load_student_requests(STUDENT_REQUESTS_FILE)
    
    # Step 2: Extract and structure course data from student requests
    print("Extracting course information...")
    courses = extract_course_info_from_requests(student_requests_df)
    
    # Step 3: Structure student request data
    print("Structuring student request data...")
    students = structure_student_requests(student_requests_df)
    
    # Step 4: Create mock data for missing information
    print("Creating mock lecturer data...")
    lecturers = create_mock_lecturer_data(courses)
    
    print("Creating mock room data...")
    rooms = create_mock_rooms_data()
    
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
    validation_results = validate_data(structured_data)
    
    # Step 7: Analyze data
    print("Analyzing data...")
    analysis_results = analyze_data(structured_data)
    
    # Step 8: Generate visualizations
    print("Generating visualizations...")
    generate_visualizations(structured_data, analysis_results)
    
    # Step 9: Write analysis report
    print("Writing analysis report...")
    write_analysis_report(structured_data, validation_results, analysis_results)
    
    # Step 10: Save structured data to JSON file
    print(f"Saving structured data to {OUTPUT_JSON_FILE}...")
    with open(OUTPUT_JSON_FILE, 'w') as f:
        # Convert numpy types before serialization
        structured_data_converted = convert_numpy_types(structured_data)
        json.dump(structured_data_converted, f, indent=2)
    
    print("Course scheduling preparation completed!")
    print(f"- Cleaned data saved to: {OUTPUT_JSON_FILE}")
    print(f"- Analysis report saved to: {ANALYSIS_REPORT_FILE}")
    print(f"- Visualizations saved to: {VISUALIZATION_DIR}")

    # Step 11: Create the course schedule
    print("Creating course schedule...")
    schedule = create_course_schedule(structured_data)
    
    # Step 12: Analyze the schedule results
    print("Analyzing schedule results...")
    schedule_analysis = analyze_schedule_results(structured_data, schedule)
    
    # Step 13: Generate schedule visualizations
    print("Generating schedule visualizations...")
    generate_schedule_visualizations(structured_data, schedule, schedule_analysis)
    
    # Step 14: Write schedule report
    print("Writing schedule report...")
    write_schedule_report(structured_data, schedule, schedule_analysis)
    
    # Save the schedule to a JSON file
    print(f"Saving schedule to {os.path.join(DATA_DIR, 'schedule.json')}...")
    with open(os.path.join(DATA_DIR, 'schedule.json'), 'w') as f:
        # Convert defaultdict to regular dict for JSON serialization
        serializable_schedule = {
            'course_blocks': {k: v for k, v in schedule['course_blocks'].items()},
            'course_rooms': {k: {str(bk): v for bk, v in v.items()} for k, v in schedule['course_rooms'].items()},
            'student_schedules': {k: {str(bk): v for bk, v in v.items()} for k, v in schedule['student_schedules'].items()},
            'room_schedules': {k: {str(bk): v for bk, v in v.items()} for k, v in schedule['room_schedules'].items()},
            'lecturer_schedules': {k: {str(bk): v for bk, v in v.items()} for k, v in schedule['lecturer_schedules'].items()}
        }
        json.dump(serializable_schedule, f, indent=2)
    
    print("Course scheduling completed!")
    print(f"- Schedule data saved to: {os.path.join(DATA_DIR, 'schedule.json')}")
    print(f"- Schedule report saved to: {os.path.join(REPORT_DIR, 'schedule_report.md')}")
    print(f"- Schedule visualizations saved to: {VISUALIZATION_DIR}")

if __name__ == "__main__":
    main()
