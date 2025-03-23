# Scheduling Algorithm

The scheduling algorithm implemented in this project uses a Linear Programming (LP) approach to optimize course assignments based on student requests, room constraints, and course requirements.

## Constraint Satisfaction Problem

The course scheduling problem is formulated as a constraint satisfaction problem with the following components:

### Decision Variables

- **x[student_id, course_code, block]**: Binary variable indicating if a student is assigned to a course in a specific block
- **y[course_code, block, room_id]**: Binary variable indicating if a course is scheduled in a specific block and room

### Objective Function

The objective is to maximize the total weighted value of fulfilled student requests, where:
- Required courses have a weight of 10
- Requested courses have a weight of 5
- Recommended courses have a weight of 1

### Constraints

1. **Student Conflicts**: A student can't be in two places at once (maximum one course per block per student)
2. **Course Placement**: A course can only be scheduled in one room per block
3. **Room Capacity**: A room can only have one course per block
4. **Assignment Logic**: Students can only be assigned to courses that are actually scheduled
5. **Room Size**: The number of students assigned to a course cannot exceed the room capacity
6. **Course Size**: Each course must meet its minimum enrollment requirement and cannot exceed its maximum size

## Implementation Details

The algorithm is implemented using the PuLP linear programming library:

1. **Problem Definition**: We create a new LP problem with the objective to maximize fulfilled requests
2. **Variable Creation**: Decision variables are created for all possible student-course-block assignments
3. **Constraint Definition**: Constraints are added to ensure the solution is feasible
4. **Optimization**: The CBC solver is used to find the optimal solution
5. **Solution Extraction**: The results are extracted into a structured schedule

### Performance Considerations

- A time limit of 5 minutes (300 seconds) is set to ensure the algorithm completes in a reasonable time
- The algorithm prioritizes fulfilling required course requests over recommended ones
- The algorithm aims to minimize the number of unscheduled course requests

## Scheduling Results

The scheduling algorithm produces:
1. Student schedules showing which courses they are assigned to in each block
2. Lecturer schedules showing which courses they are teaching in each block
3. Room assignments for each course in each block
4. Course schedules showing when and where each course is scheduled

The algorithm successfully handles conflicts between requests and produces a comprehensive schedule that maximizes student satisfaction subject to the constraints.
