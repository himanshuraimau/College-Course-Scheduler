# Data Format Documentation

## Input Data Formats

### Student Requests (`dataset.xlsx - Student requests.csv`)

CSV file containing student course requests with the following columns:
- `College Year`: Student's year (e.g., "1st Year", "2nd Year")
- `Request start term`: When the course should start (e.g., "First term", "Second Term")
- `Title`: Course title
- `Type`: Request type (Required, Requested, Recommended)
- `student ID`: Unique student identifier
- `Course ID`: Course identifier
- `Length`: Course duration (1 = half year, 2 = full year)
- `Course code`: Unique course code
- `Priority`: Priority level of the course
- `Department(s)`: Academic department(s)
- `Credits`: Course credit value

### Course List (`dataset.xlsx - Course list.csv`)

CSV file containing course information (specific format may vary).

### Lecturer Details (`dataset.xlsx - Lecturer Details.csv`)

CSV file containing lecturer information (specific format may vary).

### Rooms Data (`dataset.xlsx - Rooms data.csv`)

CSV file containing room information (specific format may vary).

### Rules (`dataset.xlsx - RULES.csv`)

CSV file containing scheduling rules with columns:
- `S. No.`: Rule number
- `RULES`: Description of the rule

## Intermediate Data Formats

### Cleaned Data (JSON)

The preprocessed data is stored in a structured JSON format:

```json
{
  "courses": [
    {
      "code": "COURSE_CODE",
      "title": "Course Title",
      "length": 2,
      "priority": "Core course",
      "available_blocks": ["1A", "1B", "2A", "2B", "3", "4A", "4B"],
      "unavailable_blocks": [],
      "min_size": 5,
      "target_size": 20,
      "max_size": 40,
      "num_sections": 1,
      "credits": 1,
      "department": "Department Name"
    }
  ],
  "students": [
    {
      "id": "STUDENT_ID",
      "year": "Year Level",
      "requests": {
        "required": [
          {"code": "COURSE_CODE", "title": "Course Title", "length": 2, "term": "First term"}
        ],
        "requested": [...],
        "recommended": [...]
      }
    }
  ],
  "lecturers": [
    {
      "id": "LECTURER_ID",
      "name": "Professor Name",
      "department": "Department Name",
      "courses": [
        {"code": "COURSE_CODE", "title": "Course Title", "length": 2, "section": 1}
      ]
    }
  ],
  "rooms": [
    {
      "room_number": "101",
      "capacity": 30,
      "type": "Standard",
      "building": "Main Building"
    }
  ],
  "blocks": ["1A", "1B", "2A", "2B", "3", "4A", "4B"]
}
```

## Output Data Formats

### Scheduling Results (JSON)

```json
{
  "schedule": {
    "1A": [
      {
        "course": "COURSE_CODE",
        "section": 1,
        "lecturer": "LECTURER_ID",
        "room": "ROOM_NUMBER",
        "students": 25
      }
    ],
    "1B": [...],
    "2A": [...],
    "2B": [...],
    "3": [...],
    "4A": [...],
    "4B": [...]
  },
  "student_schedules": {
    "STUDENT_ID": {
      "1A": {
        "course": "COURSE_CODE",
        "section": 1,
        "lecturer": "LECTURER_ID",
        "room": "ROOM_NUMBER"
      },
      "2B": {...}
    }
  },
  "lecturer_schedules": {...},
  "room_schedules": {...},
  "statistics": {
    "total_requests": 1000,
    "fulfilled_requests": 850,
    "fulfillment_rate": 0.85,
    "by_priority": {
      "required": {
        "total": 300,
        "fulfilled": 295,
        "rate": 0.98
      },
      "requested": {
        "total": 500,
        "fulfilled": 425,
        "rate": 0.85
      },
      "recommended": {
        "total": 200,
        "fulfilled": 130,
        "rate": 0.65
      }
    }
  }
}
```

### Analysis Report (Markdown)

A Markdown file containing:
- Data summary
- Validation results
- Data insights
- Course demand analysis
- Potential scheduling conflicts
- Visualizations

### Final Report (Markdown)

A Markdown file containing:
- Executive summary
- Request fulfillment rates
- Block utilization
- Top courses
- Scheduling challenges and solutions
- Recommendations
- Conclusion
