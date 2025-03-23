"""
Course scheduling optimization functions.
"""
import pulp
from collections import defaultdict
import sys

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
    
    # Debug info
    print(f"Scheduling {len(courses)} courses for {len(students)} students")
    print(f"Available blocks: {blocks}")
    print(f"Available rooms: {len(rooms)}")
    
    # Create problem instance
    prob = pulp.LpProblem("CourseScheduling", pulp.LpMaximize)
    
    # Track which courses are requested by students (to reduce variable count)
    requested_courses = set()
    for student in students:
        for priority in ['required', 'requested', 'recommended']:
            for course_req in student['requests'][priority]:
                requested_courses.add(course_req['code'])
    
    print(f"Total requested courses: {len(requested_courses)}")
    
    # Only create variables for courses that are actually requested
    relevant_courses = [course for course in courses if course['code'] in requested_courses]
    print(f"Relevant courses for scheduling: {len(relevant_courses)}")
    
    if not relevant_courses:
        print("ERROR: No relevant courses found. Check that course codes match between requests and course data.")
        return default_empty_schedule()
    
    # Decision variables
    # x[student_id, course_code, block] = 1 if student is assigned to course in block
    x = {}
    # Track created variables to avoid duplicates
    created_x_vars = set()
    
    for student in students:
        student_id = student['id']
        # Collect all course requests for this student
        requested_course_codes = set()
        for priority in ['required', 'requested', 'recommended']:
            for course_req in student['requests'][priority]:
                course_code = course_req['code']
                # Only create variables for valid course codes
                if course_code in requested_courses:
                    requested_course_codes.add(course_code)
        
        for course_code in requested_course_codes:
            for block in blocks:
                var_key = (student_id, course_code, block)
                if var_key not in created_x_vars:
                    x[var_key] = pulp.LpVariable(
                        f"x_{student_id}_{course_code}_{block}", 
                        cat='Binary'
                    )
                    created_x_vars.add(var_key)
    
    # y[course_code, block, room_id] = 1 if course is scheduled in block at room
    y = {}
    # Track created variables to avoid duplicates
    created_y_vars = set()
    
    for course in relevant_courses:
        course_code = course['code']
        for block in blocks:
            for room in rooms:
                room_id = room['room_number']
                var_key = (course_code, block, room_id)
                if var_key not in created_y_vars:
                    y[var_key] = pulp.LpVariable(
                        f"y_{course_code}_{block}_{room_id}",
                        cat='Binary'
                    )
                    created_y_vars.add(var_key)
    
    print(f"Created {len(x)} student assignment variables and {len(y)} course scheduling variables")
    
    # Objective function: maximize fulfilled requests with priority weights
    priority_weights = {'required': 10, 'requested': 5, 'recommended': 1}
    objective = 0
    
    for student in students:
        student_id = student['id']
        for priority in ['required', 'requested', 'recommended']:
            weight = priority_weights[priority]
            for course_req in student['requests'][priority]:
                course_code = course_req['code']
                # Only include requested courses with valid variables
                for block in blocks:
                    var_key = (student_id, course_code, block)
                    if var_key in x:
                        objective += weight * x[var_key]
    
    prob += objective
    print(f"Objective function created with {len(x)} terms")
    
    # Constraints
    constraint_count = 0
    
    # 1. Student can't be in two places at once
    for student in students:
        student_id = student['id']
        for block in blocks:
            # Get all course codes this student has requested and that have variables
            student_courses = []
            for priority in ['required', 'requested', 'recommended']:
                for course_req in student['requests'][priority]:
                    course_code = course_req['code']
                    if (student_id, course_code, block) in x:
                        student_courses.append(course_code)
            
            if student_courses:  # Only add constraint if student has requested courses
                prob += pulp.lpSum(x[(student_id, course_code, block)] 
                                for course_code in student_courses) <= 1
                constraint_count += 1
    
    # 2. Course can only be scheduled in one room per block
    for course in relevant_courses:
        course_code = course['code']
        for block in blocks:
            # Check if any rooms have variables for this course/block
            room_vars = [(course_code, block, room['room_number']) for room in rooms 
                       if (course_code, block, room['room_number']) in y]
            
            if room_vars:  # Only add constraint if variables exist
                prob += pulp.lpSum(y[var_key] for var_key in room_vars) <= 1
                constraint_count += 1
    
    # 3. Room can only have one course per block
    for room in rooms:
        room_id = room['room_number']
        for block in blocks:
            # Check if any courses have variables for this room/block
            course_vars = [(course['code'], block, room_id) for course in relevant_courses 
                         if (course['code'], block, room_id) in y]
            
            if course_vars:  # Only add constraint if variables exist
                prob += pulp.lpSum(y[var_key] for var_key in course_vars) <= 1
                constraint_count += 1
    
    # 4. Student can only be assigned to a course if it's scheduled
    for student in students:
        student_id = student['id']
        for priority in ['required', 'requested', 'recommended']:
            for course_req in student['requests'][priority]:
                course_code = course_req['code']
                for block in blocks:
                    var_key = (student_id, course_code, block)
                    if var_key in x:
                        # Find all room variables for this course/block
                        room_vars = [(course_code, block, room['room_number']) for room in rooms 
                                  if (course_code, block, room['room_number']) in y]
                        
                        if room_vars:  # Only add constraint if room variables exist
                            prob += x[var_key] <= pulp.lpSum(y[room_var] for room_var in room_vars)
                            constraint_count += 1
    
    # 5. Respect room capacity - RELAXED VERSION
    for course in relevant_courses:
        course_code = course['code']
        for block in blocks:
            for room in rooms:
                room_id = room['room_number']
                var_key = (course_code, block, room_id)
                
                if var_key in y:
                    # Count students who could be assigned to this course in this block
                    potential_students = []
                    for student in students:
                        student_id = student['id']
                        student_var_key = (student_id, course_code, block)
                        if student_var_key in x:
                            potential_students.append(student_id)
                    
                    # Only add constraint if there are potential students
                    if potential_students:
                        room_capacity = room['capacity']
                        # If room capacity is too small for class minimum size, allow some flexibility
                        effective_capacity = max(room_capacity, 5)  # Allow at least 5 students
                        
                        # Student count for this course/block
                        student_count = pulp.lpSum(x[(student_id, course_code, block)] 
                                              for student_id in potential_students)
                        
                        # If course scheduled in this room, respect capacity
                        prob += student_count <= effective_capacity * y[var_key]
                        constraint_count += 1
    
    # 6. Relaxed course minimum size constraint (allow smaller classes if needed)
    for course in relevant_courses:
        course_code = course['code']
        min_size = max(1, course['min_size'] - 3)  # Relax minimum by 3
        max_size = course['max_size'] + 5  # Allow slight overflow
        
        for block in blocks:
            # Check if course can be scheduled in any room for this block
            room_vars = [(course_code, block, room['room_number']) for room in rooms 
                       if (course_code, block, room['room_number']) in y]
            
            if room_vars:
                # Is this course scheduled in any room in this block?
                is_scheduled = pulp.lpSum(y[var_key] for var_key in room_vars)
                
                # Find all students who could take this course in this block
                potential_students = []
                for student in students:
                    student_id = student['id']
                    student_var_key = (student_id, course_code, block)
                    if student_var_key in x:
                        potential_students.append(student_id)
                
                if potential_students:
                    # Number of students in this course in this block
                    student_count = pulp.lpSum(x[(student_id, course_code, block)] 
                                          for student_id in potential_students)
                    
                    # Relaxed minimum size constraint - only enforce for courses with enough requests
                    if len(potential_students) >= min_size:
                        prob += student_count >= min_size * is_scheduled
                        constraint_count += 1
                    
                    # Maximum size constraint
                    prob += student_count <= max_size * is_scheduled
                    constraint_count += 1
    
    print(f"Created {constraint_count} constraints")
    
    # Solve the problem
    print("Solving the scheduling problem...")
    solver = pulp.PULP_CBC_CMD(msg=True, timeLimit=300)  # 5 minute time limit
    prob.solve(solver)
    
    status = pulp.LpStatus[prob.status]
    print(f"Solution status: {status}")
    
    if status != 'Optimal':
        print(f"Warning: Could not find optimal solution. Status: {status}")
    
    objective_value = pulp.value(prob.objective)
    print(f"Objective value: {objective_value}")
    
    if objective_value is None or objective_value < 1:
        print("WARNING: Optimization failed to find a solution with any fulfilled requests.")
        print("Trying a simpler model with fewer constraints...")
        return create_simplified_schedule(structured_data)
    
    # Extract the schedule from the solution
    schedule = {
        'course_blocks': defaultdict(list),  # course_code -> list of blocks
        'course_rooms': defaultdict(dict),   # course_code -> {block: room_id}
        'student_schedules': defaultdict(dict),  # student_id -> {block: course_code}
        'room_schedules': defaultdict(dict),     # room_id -> {block: course_code}
        'lecturer_schedules': defaultdict(dict)  # lecturer_id -> {block: course_code}
    }
    
    # Extract scheduled courses
    for course in relevant_courses:
        course_code = course['code']
        for block in blocks:
            for room in rooms:
                room_id = room['room_number']
                var_key = (course_code, block, room_id)
                if var_key in y and pulp.value(y[var_key]) > 0.5:
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
                    var_key = (student_id, course_code, block)
                    if var_key in x and pulp.value(x[var_key]) > 0.5:
                        schedule['student_schedules'][student_id][block] = course_code
    
    # Assign lecturers based on their course assignments
    for lecturer in lecturers:
        lecturer_id = lecturer['id']
        lecturer_courses = [course['code'] for course in lecturer['courses']]
        
        for course_code in lecturer_courses:
            if course_code in schedule['course_blocks']:
                for block in schedule['course_blocks'][course_code]:
                    schedule['lecturer_schedules'][lecturer_id][block] = course_code
    
    # Print summary
    print(f"Schedule created with {len(schedule['course_blocks'])} courses scheduled")
    print(f"Student schedules created for {len(schedule['student_schedules'])} students")
    print(f"Room schedules created for {len(schedule['room_schedules'])} rooms")
    print(f"Lecturer schedules created for {len(schedule['lecturer_schedules'])} lecturers")
    
    return schedule

def create_simplified_schedule(structured_data):
    """Create a simplified schedule when the full optimization fails"""
    print("Creating simplified schedule with direct assignments...")
    
    # Extract data
    courses = structured_data['courses']
    students = structured_data['students']
    lecturers = structured_data['lecturers']
    rooms = structured_data['rooms']
    blocks = structured_data['blocks']
    
    # Default schedule structure
    schedule = {
        'course_blocks': defaultdict(list),  # course_code -> list of blocks
        'course_rooms': defaultdict(dict),   # course_code -> {block: room_id}
        'student_schedules': defaultdict(dict),  # student_id -> {block: course_code}
        'room_schedules': defaultdict(dict),     # room_id -> {block: course_code}
        'lecturer_schedules': defaultdict(dict)  # lecturer_id -> {block: course_code}
    }
    
    # Count course requests to prioritize popular courses
    course_counts = defaultdict(int)
    for student in students:
        for priority in ['required', 'requested', 'recommended']:
            for course_req in student['requests'][priority]:
                course_counts[course_req['code']] += 1
    
    # Sort courses by popularity
    sorted_courses = sorted(
        [(code, count) for code, count in course_counts.items()],
        key=lambda x: x[1], 
        reverse=True
    )
    
    # Assign blocks to courses
    block_usage = {block: [] for block in blocks}  # block -> [course_codes]
    room_assignments = {}  # (course_code, block) -> room_id
    
    # Assign popular courses to blocks first
    for course_code, _ in sorted_courses:
        course_info = next((c for c in courses if c['code'] == course_code), None)
        if course_info is None:
            continue
            
        # Find least used block
        block_loads = [(block, len(courses)) for block, courses in block_usage.items()]
        block_loads.sort(key=lambda x: x[1])  # Sort by usage
        
        # Assign to first available block
        for block, _ in block_loads:
            # Find suitable room
            for room in rooms:
                room_id = room['room_number']
                room_taken = False
                
                # Check if room is already assigned in this block
                for existing_course in block_usage[block]:
                    if (existing_course, block) in room_assignments and \
                       room_assignments[(existing_course, block)] == room_id:
                        room_taken = True
                        break
                        
                if not room_taken and room['capacity'] >= course_info['min_size']:
                    # Assign course to this block and room
                    block_usage[block].append(course_code)
                    room_assignments[(course_code, block)] = room_id
                    
                    # Update schedule
                    schedule['course_blocks'][course_code].append(block)
                    schedule['course_rooms'][course_code][block] = room_id
                    schedule['room_schedules'][room_id][block] = course_code
                    break
                    
            # If course was assigned to this block, stop looking for blocks
            if course_code in block_usage[block]:
                break
    
    # Assign students to courses
    for student in students:
        student_id = student['id']
        assigned_blocks = set()
        
        # Process requests in priority order
        for priority in ['required', 'requested', 'recommended']:
            for course_req in student['requests'][priority]:
                course_code = course_req['code']
                
                # Check if course was scheduled
                if course_code in schedule['course_blocks']:
                    # Try to assign to any available block for this course
                    for block in schedule['course_blocks'][course_code]:
                        # Only assign if student doesn't already have a course in this block
                        if block not in assigned_blocks:
                            schedule['student_schedules'][student_id][block] = course_code
                            assigned_blocks.add(block)
                            break
    
    # Assign lecturers to their courses
    for lecturer in lecturers:
        lecturer_id = lecturer['id']
        lecturer_courses = [course['code'] for course in lecturer['courses']]
        
        for course_code in lecturer_courses:
            if course_code in schedule['course_blocks']:
                for block in schedule['course_blocks'][course_code]:
                    schedule['lecturer_schedules'][lecturer_id][block] = course_code
    
    # Print summary
    print(f"Simplified schedule created with {len(schedule['course_blocks'])} courses scheduled")
    print(f"Student schedules created for {len(schedule['student_schedules'])} students")
    
    return schedule

def default_empty_schedule():
    """Return an empty schedule structure when optimization fails"""
    return {
        'course_blocks': defaultdict(list),
        'course_rooms': defaultdict(dict),
        'student_schedules': defaultdict(dict),
        'room_schedules': defaultdict(dict),
        'lecturer_schedules': defaultdict(dict)
    }
