# Crestwood College Course Scheduling - Implementation Plan

## 1. Understanding the Data and Requirements

### Available Data Sources
- Course list data: Information about courses, their capacity, available blocks, etc.
- Lecturer Details: Which teacher teaches which course
- Student requests: Course preferences from students (Required, Requested, Recommended)
- RULES: Constraints for the scheduling system

### Key Scheduling Rules
1. The college has 7 blocks: "1A", "1B", "2A", "2B", "3", "4A", "4B"
2. Block scheduling system with longer time periods (60-120 minutes)
3. No teacher can teach multiple sections in the same block
4. No student can be scheduled for multiple courses in the same block
5. Request priority: Required > Requested > Recommended
6. Students from different years can be in the same section
7. Section sizes must respect minimum, target, and maximum capacities
8. Sections must be balanced with students distributed evenly
9. Courses can only be scheduled in their available blocks
10. Course length determines if it runs for entire year (2) or half year (1)

## 2. Data Preprocessing and Cleaning

### Course List Data
- Clean course codes, titles, and other fields
- Normalize available blocks data into a consistent format
- Validate section capacity constraints (min ≤ target ≤ max)
- Verify course credits match course length

### Lecturer Data
- Normalize lecturer IDs and names
- Ensure each course has at least one assigned lecturer
- Identify courses without lecturers
- Validate lecturer availability across multiple sections

### Student Requests
- Clean and normalize student IDs
- Structure requests by priority (Required, Requested, Recommended)
- Group requests by student and year level
- Identify impossible or conflicting requests

## 3. Data Structure Design

### JSON Structure
Design a comprehensive data structure that includes:

```json
{
  "courses": [
    {
      "code": "ARTBND",
      "title": "Band - High",
      "length": 2,
      "priority": "Core course",
      "available_blocks": ["1A", "1B", "2A", "2B", "3", "4A", "4B"],
      "unavailable_blocks": [],
      "min_size": 7,
      "target_size": 25,
      "max_size": 40,
      "num_sections": 1,
      "credits": 1
    },
    // More courses
  ],
  "lecturers": [
    {
      "id": "5361519",
      "courses": [
        {
          "code": "ARTBND",
          "title": "Band - High",
          "length": 2,
          "section": 1
        }
      ]
    },
    // More lecturers
  ],
  "students": [
    {
      "id": "5407488",
      "year": "2nd Year",
      "requests": {
        "required": [
          {"code": "BIB10", "title": "Bible 10", "length": 2, "term": "First term"}
        ],
        "requested": [
          {"code": "ENG10H", "title": "English 10 Honors", "length": 2, "term": "First term"},
          // More requested courses
        ],
        "recommended": [
          {"code": "SCICHEM10H", "title": "Chemistry Honors", "length": 2, "term": "First term"},
          // More recommended courses
        ]
      }
    },
    // More students
  ],
  "blocks": ["1A", "1B", "2A", "2B", "3", "4A", "4B"]
}
```

## 4. Data Validation and Analysis

### Validation Checks
1. Ensure all course codes mentioned in student requests exist in course list
2. Verify lecturer availability for all sections
3. Check if available blocks for each course match with the master block list
4. Validate section capacities and counts

### Data Analysis
1. Identify most requested courses (potential bottlenecks)
2. Check if demand for any course exceeds capacity
3. Analyze block availability constraints
4. Identify potential scheduling conflicts

## 5. Scheduling Algorithm Design

### Approach
1. **Priority-based scheduling**: Process requests in order of priority
2. **Constraint satisfaction**: Ensure all rules are met while maximizing fulfilled requests
3. **Optimization**: Balance section sizes and maximize student satisfaction

### Algorithm Steps
1. Start with Required courses for all students
2. Process Requested courses based on demand and constraints
3. Handle Recommended courses if space allows
4. Iteratively resolve conflicts and optimize assignments

### Conflict Resolution
- When a student has conflicting course requests in the same block
- When a teacher is assigned to multiple sections in the same block
- When section capacity limits are reached

## 6. Implementation Plan

### Phase 1: Data Preprocessing
- Write scripts to clean and normalize all data sources
- Convert to structured JSON format
- Validate data integrity and completeness

### Phase 2: Analysis and Validation
- Run analytical queries on the data
- Generate reports on potential issues
- Document insights and challenges

### Phase 3: Algorithm Implementation
- Develop the core scheduling algorithm
- Implement constraint checking
- Build conflict resolution mechanisms

### Phase 4: Output Generation and Visualization
- Generate student schedules
- Create teacher assignment reports
- Visualize room and block utilization

## 7. Evaluation Metrics

- **Request Fulfillment Rate**: Percentage of student requests satisfied
- **Priority Satisfaction**: Weighted score based on fulfilling Required, Requested, and Recommended courses
- **Section Balance**: How evenly distributed students are across sections
- **Resource Utilization**: How efficiently blocks, rooms, and teachers are utilized

## 8. Challenges and Considerations

1. **Scalability**: The algorithm needs to handle a large number of students and courses
2. **Optimization trade-offs**: Balancing student preferences vs. resource constraints
3. **Edge cases**: Handling unique scenarios like courses with very specific block requirements
4. **Performance**: Ensuring the scheduling process completes in reasonable time

## Next Steps
1. Begin data cleaning and preprocessing
2. Create normalized JSON structures
3. Run initial validation and analysis
4. Document findings and adjust approach as needed
