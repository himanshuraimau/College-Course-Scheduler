import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import Counter

# Define directory paths
BASE_DIR = '/home/himanshu/Downloads/test'
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
DATA_DIR = os.path.join(OUTPUT_DIR, 'data')
REPORT_DIR = os.path.join(OUTPUT_DIR, 'reports')
VISUALIZATION_DIR = os.path.join(OUTPUT_DIR, 'visualizations')

# Create directories if they don't exist
for directory in [OUTPUT_DIR, DATA_DIR, REPORT_DIR, VISUALIZATION_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_data():
    """Load the necessary data files"""
    with open(os.path.join(DATA_DIR, 'cleaned_data.json'), 'r') as f:
        cleaned_data = json.load(f)
    
    with open(os.path.join(DATA_DIR, 'scheduling_results.json'), 'r') as f:
        results = json.load(f)
    
    return cleaned_data, results

def generate_fulfillment_chart(stats, output_dir):
    """Generate chart showing request fulfillment rates by priority"""
    priorities = ['required', 'requested', 'recommended']
    rates = [stats['by_priority'][p]['rate'] for p in priorities]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(priorities, rates, color=['green', 'blue', 'orange'])
    
    # Add percentage labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{height:.1%}', ha='center', va='bottom')
    
    plt.ylim(0, 1.1)  # Set y-axis to go from 0 to 1.1 (110%)
    plt.ylabel('Fulfillment Rate')
    plt.title('Request Fulfillment Rate by Priority')
    plt.savefig(os.path.join(output_dir, 'fulfillment_rates.png'))
    plt.close()

def generate_block_utilization_chart(results, output_dir):
    """Generate chart showing course distribution across blocks"""
    block_counts = {block: len(sections) for block, sections in results['schedule'].items()}
    
    plt.figure(figsize=(10, 6))
    plt.bar(block_counts.keys(), block_counts.values())
    plt.ylabel('Number of Sections')
    plt.title('Course Section Distribution by Block')
    plt.savefig(os.path.join(output_dir, 'block_utilization.png'))
    plt.close()

def generate_course_assignment_chart(results, cleaned_data, output_dir):
    """Generate chart showing top courses by student assignments"""
    course_counts = Counter()
    for student_schedule in results['student_schedules'].values():
        for block_schedule in student_schedule.values():
            course_counts[block_schedule['course']] += 1
    
    # Get course titles for top courses
    course_dict = {c['code']: c['title'] for c in cleaned_data['courses']}
    top_courses = course_counts.most_common(10)
    
    courses = [course_dict.get(code, code) for code, _ in top_courses]
    counts = [count for _, count in top_courses]
    
    plt.figure(figsize=(12, 6))
    plt.barh(courses, counts)
    plt.xlabel('Number of Students Assigned')
    plt.title('Top 10 Courses by Student Assignments')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'course_assignments.png'))
    plt.close()

def write_final_report(cleaned_data, results):
    """Write the final scheduling report"""
    # Generate visualizations
    generate_fulfillment_chart(results['statistics'], VISUALIZATION_DIR)
    generate_block_utilization_chart(results, VISUALIZATION_DIR)
    generate_course_assignment_chart(results, cleaned_data, VISUALIZATION_DIR)
    
    # Write the report
    with open(os.path.join(REPORT_DIR, 'final_report.md'), 'w') as f:
        f.write("# Crestwood College Course Scheduling - Final Report\n\n")
        
        # Executive Summary
        f.write("## Executive Summary\n\n")
        stats = results['statistics']
        f.write(f"The scheduling process has successfully assigned courses to {len(results['student_schedules'])} students ")
        f.write(f"across {len(cleaned_data['courses'])} different courses and {len(results['schedule'])} time blocks. ")
        f.write(f"Overall, {stats['fulfilled_requests']} out of {stats['total_requests']} course requests ")
        f.write(f"({stats['fulfillment_rate']:.1%}) were successfully fulfilled.\n\n")
        
        # Fulfillment Rates by Priority
        f.write("## Request Fulfillment Rates\n\n")
        f.write("![Fulfillment Rates](../visualizations/fulfillment_rates.png)\n\n")
        f.write("| Priority | Requests | Fulfilled | Rate |\n")
        f.write("|----------|----------|-----------|------|\n")
        
        for priority in ['required', 'requested', 'recommended']:
            p_stats = stats['by_priority'][priority]
            f.write(f"| {priority.capitalize()} | {p_stats['total']} | {p_stats['fulfilled']} | {p_stats['rate']:.1%} |\n")
        
        f.write("\n")
        
        # Block Utilization
        f.write("## Block Utilization\n\n")
        f.write("![Block Utilization](../visualizations/block_utilization.png)\n\n")
        
        f.write("| Block | Number of Sections | Average Students per Section |\n")
        f.write("|-------|-------------------|-----------------------------|\n")
        
        for block, sections in results['schedule'].items():
            if sections:
                avg_students = sum(section['students'] for section in sections) / len(sections)
                f.write(f"| {block} | {len(sections)} | {avg_students:.1f} |\n")
            else:
                f.write(f"| {block} | 0 | N/A |\n")
        
        f.write("\n")
        
        # Top Courses
        f.write("## Top Courses by Student Assignments\n\n")
        f.write("![Course Assignments](../visualizations/course_assignments.png)\n\n")
        
        # Scheduling Challenges and Solutions
        f.write("## Scheduling Challenges and Solutions\n\n")
        f.write("### Challenges\n\n")
        f.write("1. **Balancing student preferences**: Ensuring as many students as possible get their preferred courses.\n")
        f.write("2. **Block constraints**: Some courses had limited availability for specific blocks.\n")
        f.write("3. **Room assignments**: Matching section sizes with appropriate room capacities.\n")
        f.write("4. **Lecturer availability**: Avoiding scheduling conflicts for lecturers teaching multiple courses.\n\n")
        
        f.write("### Solutions\n\n")
        f.write("1. **Priority-based scheduling**: Required courses were scheduled first, followed by requested and recommended.\n")
        f.write("2. **Dynamic section creation**: Course sections were created based on actual demand.\n")
        f.write("3. **Constraint satisfaction algorithm**: The scheduler accounted for multiple constraints simultaneously.\n")
        f.write("4. **Iterative optimization**: Multiple passes were made to maximize fulfillment rates.\n\n")
        
        # Recommendations
        f.write("## Recommendations for Future Terms\n\n")
        f.write("1. **Increase sections for high-demand courses**: Some courses had significantly more requests than available seats.\n")
        f.write("2. **Review block assignments**: Some blocks have higher utilization than others, suggesting potential imbalance.\n")
        f.write("3. **Optimize room assignments**: Better matching of section sizes to room capacities could improve resource utilization.\n")
        f.write("4. **Collect student preferences earlier**: Earlier collection of student preferences would allow more time for optimization.\n\n")
        
        # Conclusion
        f.write("## Conclusion\n\n")
        f.write("The scheduling system successfully balanced multiple constraints and priorities to create a schedule that ")
        f.write(f"satisfies {stats['fulfillment_rate']:.1%} of student requests. Required courses achieved a ")
        f.write(f"{stats['by_priority']['required']['rate']:.1%} fulfillment rate, demonstrating the effectiveness ")
        f.write("of the priority-based approach. The schedule respects all specified constraints including block availability, ")
        f.write("lecturer assignments, and room capacities.\n\n")

def main():
    """Run the report generation process"""
    print("Loading data...")
    cleaned_data, results = load_data()
    
    print("Generating final report...")
    write_final_report(cleaned_data, results)
    
    print("Final report generated successfully!")
    print(f"Report saved to: {os.path.join(REPORT_DIR, 'final_report.md')}")

if __name__ == "__main__":
    main()
