# Scheduling Algorithm Details

## Algorithm Overview

The Crestwood College Course Scheduling System employs a multi-phase constraint satisfaction algorithm to generate optimal course schedules. The algorithm prioritizes required courses over requested and recommended ones while ensuring all scheduling constraints are met.

## Key Components

### Course Section Creation

Before scheduling students, the algorithm creates appropriate course sections based on demand:

1. Calculate demand for each course
2. Determine the needed number of sections based on demand and target section size
3. Create section objects with appropriate attributes

```python
needed_sections = max(1, (demand + target_size - 1) // target_size)
actual_sections = course.get('num_sections', 1)
num_sections = min(needed_sections, actual_sections)
```

### Lecturer Assignment

The algorithm assigns lecturers to sections based on qualifications:

1. Create a mapping of courses to qualified lecturers
2. Distribute sections among qualified lecturers
3. Ensure no lecturer is assigned to multiple sections in the same block

### Priority-Based Scheduling

The core scheduling process follows a strict priority order:

1. **Required Courses**: Schedule all required courses first
2. **Requested Courses**: Schedule requested courses next
3. **Recommended Courses**: Schedule recommended courses last if space allows

This ensures that higher-priority requests are fulfilled first.

### Student Assignment Logic

For each student and course request:

1. Skip if student is already assigned to the course
2. Find available sections (not full and don't conflict with existing schedule)
3. Prefer sections that are already scheduled but not full
4. If no scheduled sections are available, choose an unscheduled section
5. If choosing an unscheduled section, assign an appropriate block
6. Add the student to the selected section

```python
# Find student's current block assignments
student_blocks = set()
for assigned_course, assigned_section in self.student_assignments[student_id].items():
    if assigned_section['block']:
        student_blocks.add(assigned_section['block'])

# Find sections that aren't full and don't conflict
available_sections = []
for section in sections:
    if len(section['students']) >= section['max_size']:
        continue
    
    if not section['block']:
        available_sections.append(section)
        continue
    
    if section['block'] in student_blocks:
        continue
    
    available_sections.append(section)
```

### Block Assignment

When assigning a block to a section:

1. Get available blocks for the course
2. Check which blocks the lecturer is already assigned to
3. Find blocks that don't conflict with lecturer's schedule
4. Choose a valid block randomly
5. Update lecturer assignments and schedule

### Room Assignment

The algorithm assigns rooms to sections based on size requirements:

1. Sort rooms by capacity
2. Sort sections by student count (descending)
3. For each section, find the smallest suitable room that isn't already assigned in that block
4. Assign the room to the section

## Constraint Handling

The algorithm enforces the following constraints:

1. **Block constraints**: Courses are only scheduled in their available blocks
2. **Lecturer constraints**: No lecturer teaches multiple sections in the same block
3. **Student constraints**: No student is scheduled for multiple courses in the same block
4. **Capacity constraints**: Sections don't exceed maximum capacity
5. **Balancing**: Students are distributed evenly across sections when possible

## Optimization Techniques

1. **Demand-based section creation**: Creates an appropriate number of sections based on actual demand
2. **Least-filled section preference**: When multiple sections are available, chooses the section with fewer students
3. **Block availability constraints**: Considers course-specific block restrictions during scheduling
4. **Room-section matching**: Matches section sizes with appropriate room capacities

## Algorithm Performance

The algorithm's time complexity is primarily determined by:
- Number of students
- Number of course requests per student
- Number of courses
- Number of sections per course
- Number of blocks

In the worst case, the time complexity is approximately O(S × R × C × B), where:
- S is the number of students
- R is the average number of requests per student
- C is the number of courses
- B is the number of blocks

However, various optimizations and early termination conditions improve real-world performance.
