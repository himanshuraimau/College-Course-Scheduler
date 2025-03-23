"""
Visualization functions for the scheduling system.
"""
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from collections import Counter

def generate_data_visualizations(structured_data, analysis_data, visualization_dir):
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
        plt.savefig(os.path.join(visualization_dir, 'course_demand.png'))
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
        plt.savefig(os.path.join(visualization_dir, 'student_years.png'))
        plt.close()

def generate_schedule_visualizations(structured_data, schedule, schedule_analysis, visualization_dir):
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
    plt.savefig(os.path.join(visualization_dir, 'request_resolution.png'))
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
    plt.savefig(os.path.join(visualization_dir, 'priority_resolution.png'))
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
    plt.savefig(os.path.join(visualization_dir, 'course_resolution_rates.png'))
    plt.close()
