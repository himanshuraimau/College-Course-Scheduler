"""
Data processing functions for the scheduling system.
"""
import json
import numpy as np
from collections import defaultdict

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

def save_structured_data(structured_data, output_file):
    """Save structured data to JSON file"""
    with open(output_file, 'w') as f:
        # Convert numpy types before serialization
        structured_data_converted = convert_numpy_types(structured_data)
        json.dump(structured_data_converted, f, indent=2)

def save_schedule_data(schedule, output_file):
    """Save schedule data to JSON file"""
    with open(output_file, 'w') as f:
        # Convert defaultdict to regular dict for JSON serialization
        serializable_schedule = {
            'course_blocks': {k: v for k, v in schedule['course_blocks'].items()},
            'course_rooms': {k: {str(bk): v for bk, v in v.items()} for k, v in schedule['course_rooms'].items()},
            'student_schedules': {k: {str(bk): v for bk, v in v.items()} for k, v in schedule['student_schedules'].items()},
            'room_schedules': {k: {str(bk): v for bk, v in v.items()} for k, v in schedule['room_schedules'].items()},
            'lecturer_schedules': {k: {str(bk): v for bk, v in v.items()} for k, v in schedule['lecturer_schedules'].items()}
        }
        json.dump(serializable_schedule, f, indent=2)
