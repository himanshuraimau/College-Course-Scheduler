# Milestone 2: Smart Scheduling Solution

## Algorithm Approach

This milestone implements a scheduling algorithm to generate optimal course schedules based on the cleaned data from Milestone 1, following the approach described in the system documentation.

### Algorithm Overview
- Priority-based scheduling that prioritizes required courses first
- Constraint satisfaction to handle block assignments, room capacity, and lecturer availability
- Resource optimization for efficient use of rooms and lecturer time
- Comprehensive reporting and visualization of results

### Key Features
- Successfully scheduled 766 out of 1259 course requests (60.8%)
- Nearly perfect fulfillment of required courses (99.4%)
- Dynamic block assignment based on constraints
- Detailed student, lecturer, and course schedules
- Comprehensive analytics and reporting

## Constraints Handled

1. **Hard Constraints**
   - No lecturer can teach two courses simultaneously
   - No student can be scheduled for multiple courses in the same block
   - Room capacity must meet or exceed course enrollment
   - Courses must be scheduled within valid time blocks

2. **Soft Constraints**
   - Instructor preferences for teaching times
   - Balanced distribution of courses across blocks
   - Efficient use of classroom resources
   - Prioritization of required courses over requested and recommended

## Results and Statistics

As shown in the schedule report:
- Total Requests: 1259
- Resolved Requests: 806 (64.0%)
- Unresolved Requests: 453 (36.0%)

Priority-based resolution:
- Required: 178 of 178 (100.0%)
- Requested: 564 of 963 (58.6%)
- Recommended: 64 of 118 (54.2%)

## Files Included

- `final_report.md` - Comprehensive overview of scheduling results
- `schedule_report.md` - Detailed schedule views and statistics
- `algorithm_details.md` - In-depth explanation of the scheduling algorithm
- Visualizations showing request fulfillment, block utilization, and course assignments

## GitHub Repository

The code implementation for this milestone can be found at: https://github.com/himanshuraimau/College-Course-Scheduler
