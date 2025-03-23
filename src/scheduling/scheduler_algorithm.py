import json
import random
from collections import defaultdict
import os

# Create output directory paths
BASE_DIR = '/home/himanshu/Downloads/test'
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
DATA_DIR = os.path.join(OUTPUT_DIR, 'data')

# Create directories if they don't exist
for directory in [OUTPUT_DIR, DATA_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

class CourseScheduler:
    def __init__(self, data_file):
        """Initialize scheduler with cleaned data"""
        with open(data_file, 'r') as f:
            self.data = json.load(f)
        
        self.blocks = self.data['blocks']
        self.courses = {c['code']: c for c in self.data['courses']}
        self.students = self.data['students']
        self.lecturers = self.data['lecturers']
        self.rooms = self.data['rooms']
        
        # Will store the final schedule
        self.schedule = {block: [] for block in self.blocks}
        
        # Track course sections and assignments
        self.course_sections = {}
        self.student_assignments = defaultdict(dict)
        self.lecturer_assignments = defaultdict(list)

    def create_course_sections(self):
        """Create sections for each course based on demand and constraints"""
        # Calculate demand for each course
        course_demand = defaultdict(int)
        for student in self.students:
            for priority in ['required', 'requested', 'recommended']:
                for request in student['requests'].get(priority, []):
                    course_demand[request['code']] += 1
        
        # Create sections based on demand and course constraints
        for code, course in self.courses.items():
            if code not in course_demand:
                continue
            
            target_size = course.get('target_size', 20)
            max_size = course.get('max_size', 40)
            demand = course_demand[code]
            
            # Calculate number of sections needed
            needed_sections = max(1, (demand + target_size - 1) // target_size)
            actual_sections = course.get('num_sections', 1)
            num_sections = min(needed_sections, actual_sections)
            
            # Create section objects
            sections = []
            for i in range(num_sections):
                section = {
                    'course_code': code,
                    'section_num': i + 1,
                    'students': [],
                    'lecturer_id': None,
                    'room': None,
                    'block': None,
                    'max_size': max_size,
                    'target_size': target_size
                }
                sections.append(section)
            
            self.course_sections[code] = sections
    
    def assign_lecturers_to_sections(self):
        """Assign lecturers to course sections"""
        # Create a mapping of courses to qualified lecturers
        qualified_lecturers = defaultdict(list)
        for lecturer in self.lecturers:
            for course in lecturer['courses']:
                qualified_lecturers[course['code']].append(lecturer['id'])
        
        # Assign lecturers to sections
        for code, sections in self.course_sections.items():
            if code not in qualified_lecturers or not qualified_lecturers[code]:
                print(f"Warning: No qualified lecturers for course {code}")
                continue
            
            # Distribute sections among qualified lecturers
            lecturers = qualified_lecturers[code]
            for i, section in enumerate(sections):
                lecturer_id = lecturers[i % len(lecturers)]
                section['lecturer_id'] = lecturer_id

    def assign_rooms(self):
        """Assign rooms to course sections based on capacity"""
        # Sort rooms by capacity
        sorted_rooms = sorted(self.rooms, key=lambda r: r['capacity'])
        room_assignments = {room['room_number']: {} for room in self.rooms}
        
        # Assign rooms by block, starting with largest sections
        all_sections = []
        for sections in self.course_sections.values():
            all_sections.extend(sections)
        
        # Sort sections by expected size (descending)
        all_sections.sort(key=lambda s: len(s['students']), reverse=True)
        
        for section in all_sections:
            if not section['block']:
                continue
                
            block = section['block']
            section_size = len(section['students'])
            
            # Find suitable room
            assigned = False
            for room in sorted_rooms:
                room_id = room['room_number']
                if room['capacity'] >= section_size and block not in room_assignments[room_id]:
                    room_assignments[room_id][block] = section
                    section['room'] = room_id
                    assigned = True
                    break
            
            if not assigned:
                print(f"Warning: Could not find suitable room for {section['course_code']} section {section['section_num']} in block {block}")

    def schedule_required_courses(self):
        """Schedule all required courses first"""
        for student in self.students:
            student_id = student['id']
            
            # Process required courses
            for request in student['requests'].get('required', []):
                course_code = request['code']
                if course_code not in self.course_sections:
                    continue
                
                self._assign_student_to_course(student_id, course_code)

    def schedule_requested_courses(self):
        """Schedule requested courses after required courses"""
        for student in self.students:
            student_id = student['id']
            
            # Process requested courses
            for request in student['requests'].get('requested', []):
                course_code = request['code']
                if course_code not in self.course_sections:
                    continue
                
                self._assign_student_to_course(student_id, course_code)

    def schedule_recommended_courses(self):
        """Schedule recommended courses last"""
        for student in self.students:
            student_id = student['id']
            
            # Process recommended courses
            for request in student['requests'].get('recommended', []):
                course_code = request['code']
                if course_code not in self.course_sections:
                    continue
                
                self._assign_student_to_course(student_id, course_code)

    def _assign_student_to_course(self, student_id, course_code):
        """Assign a student to a section of the requested course"""
        # Skip if student already assigned to this course
        if course_code in self.student_assignments[student_id]:
            return
        
        sections = self.course_sections.get(course_code, [])
        if not sections:
            return
        
        # Find student's current block assignments
        student_blocks = set()
        for assigned_course, assigned_section in self.student_assignments[student_id].items():
            if assigned_section['block']:
                student_blocks.add(assigned_section['block'])
        
        # Find sections that aren't full and don't conflict with student's schedule
        available_sections = []
        for section in sections:
            # Skip full sections
            if len(section['students']) >= section['max_size']:
                continue
            
            # If section is not yet scheduled, add it as an option
            if not section['block']:
                available_sections.append(section)
                continue
            
            # Skip sections in blocks where student already has a class
            if section['block'] in student_blocks:
                continue
            
            available_sections.append(section)
        
        if not available_sections:
            # No available section found
            return
        
        # Prefer sections that are already scheduled but not full
        scheduled_sections = [s for s in available_sections if s['block']]
        if scheduled_sections:
            # Choose the least filled section
            section = min(scheduled_sections, key=lambda s: len(s['students']))
        else:
            # Choose an unscheduled section
            section = available_sections[0]
            
            # Assign a block to this section if it's not scheduled yet
            if not section['block']:
                self._assign_block_to_section(section)
        
        # Assign the student to the selected section
        section['students'].append(student_id)
        self.student_assignments[student_id][course_code] = section

    def _assign_block_to_section(self, section):
        """Assign an appropriate block to a section"""
        course_code = section['course_code']
        course = self.courses.get(course_code)
        
        if not course:
            return
            
        # Get available blocks for this course
        available_blocks = course.get('available_blocks', self.blocks)
        
        # Check which blocks the lecturer is already assigned to
        lecturer_id = section['lecturer_id']
        lecturer_blocks = set()
        
        if lecturer_id:
            for assigned_section in self.lecturer_assignments.get(lecturer_id, []):
                if assigned_section['block']:
                    lecturer_blocks.add(assigned_section['block'])
        
        # Find blocks that don't conflict with lecturer's schedule
        valid_blocks = [block for block in available_blocks if block not in lecturer_blocks]
        
        if not valid_blocks:
            print(f"Warning: No valid blocks for {course_code} section {section['section_num']}")
            return
        
        # Assign a random valid block
        chosen_block = random.choice(valid_blocks)
        section['block'] = chosen_block
        
        # Update lecturer assignments
        if lecturer_id:
            self.lecturer_assignments[lecturer_id].append(section)
        
        # Add to schedule
        self.schedule[chosen_block].append(section)

    def run_scheduling(self):
        """Run the complete scheduling process"""
        print("Creating course sections...")
        self.create_course_sections()
        
        print("Assigning lecturers to sections...")
        self.assign_lecturers_to_sections()
        
        print("Scheduling required courses...")
        self.schedule_required_courses()
        
        print("Scheduling requested courses...")
        self.schedule_requested_courses()
        
        print("Scheduling recommended courses...")
        self.schedule_recommended_courses()
        
        print("Assigning rooms...")
        self.assign_rooms()
        
        return self.generate_schedule_results()

    def generate_schedule_results(self):
        """Generate final schedule results"""
        results = {
            "schedule": {},
            "student_schedules": {},
            "lecturer_schedules": {},
            "room_schedules": {},
            "statistics": {}
        }
        
        # Format block schedules
        for block, sections in self.schedule.items():
            block_data = []
            for section in sections:
                block_data.append({
                    "course": section['course_code'],
                    "section": section['section_num'],
                    "lecturer": section['lecturer_id'],
                    "room": section['room'],
                    "students": len(section['students'])
                })
            results["schedule"][block] = block_data
        
        # Format student schedules
        for student_id, courses in self.student_assignments.items():
            student_schedule = {}
            for course_code, section in courses.items():
                if section['block']:
                    student_schedule[section['block']] = {
                        "course": course_code,
                        "section": section['section_num'],
                        "lecturer": section['lecturer_id'],
                        "room": section['room']
                    }
            results["student_schedules"][student_id] = student_schedule
        
        # Calculate statistics
        total_requests = 0
        fulfilled_requests = 0
        
        # Count by priority
        request_counts = {"required": 0, "requested": 0, "recommended": 0}
        fulfilled_counts = {"required": 0, "requested": 0, "recommended": 0}
        
        for student in self.students:
            student_id = student['id']
            assigned_courses = set(self.student_assignments[student_id].keys())
            
            for priority in ["required", "requested", "recommended"]:
                for request in student['requests'].get(priority, []):
                    course_code = request['code']
                    request_counts[priority] += 1
                    total_requests += 1
                    
                    if course_code in assigned_courses:
                        fulfilled_counts[priority] += 1
                        fulfilled_requests += 1
        
        results["statistics"] = {
            "total_requests": total_requests,
            "fulfilled_requests": fulfilled_requests,
            "fulfillment_rate": fulfilled_requests / total_requests if total_requests else 0,
            "by_priority": {
                "required": {
                    "total": request_counts["required"],
                    "fulfilled": fulfilled_counts["required"],
                    "rate": fulfilled_counts["required"] / request_counts["required"] if request_counts["required"] else 0
                },
                "requested": {
                    "total": request_counts["requested"],
                    "fulfilled": fulfilled_counts["requested"],
                    "rate": fulfilled_counts["requested"] / request_counts["requested"] if request_counts["requested"] else 0
                },
                "recommended": {
                    "total": request_counts["recommended"],
                    "fulfilled": fulfilled_counts["recommended"],
                    "rate": fulfilled_counts["recommended"] / request_counts["recommended"] if request_counts["recommended"] else 0
                }
            }
        }
        
        return results

def main():
    """Run the scheduling algorithm"""
    print("Initializing course scheduler...")
    scheduler = CourseScheduler(os.path.join(BASE_DIR, 'output', 'data', 'cleaned_data.json'))
    
    print("Running scheduling algorithm...")
    results = scheduler.run_scheduling()
    
    # Save scheduling results
    output_file = os.path.join(BASE_DIR, 'output', 'data', 'scheduling_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary statistics
    stats = results["statistics"]
    print("\nScheduling completed!")
    print(f"Total requests: {stats['total_requests']}")
    print(f"Fulfilled requests: {stats['fulfilled_requests']}")
    print(f"Overall fulfillment rate: {stats['fulfillment_rate']:.2%}")
    print("\nFulfillment by priority:")
    print(f"Required: {stats['by_priority']['required']['rate']:.2%}")
    print(f"Requested: {stats['by_priority']['requested']['rate']:.2%}")
    print(f"Recommended: {stats['by_priority']['recommended']['rate']:.2%}")
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()
