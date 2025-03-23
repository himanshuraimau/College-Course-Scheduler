"""
Data loading functions for the scheduling system.
"""
import pandas as pd

def load_student_requests(file_path):
    """Load and clean student request data"""
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded {len(df)} student requests")
        
        # Clean and normalize column names
        df.columns = [col.strip() for col in df.columns]
        
        # Convert student IDs to strings
        df['student ID'] = df['student ID'].astype(str)
        
        # Normalize priority values
        priority_map = {'Required': 'required', 'Requested': 'requested', 'Recommended': 'recommended'}
        df['Priority'] = df['Type'].map(priority_map)
        
        return df
    except Exception as e:
        print(f"Error loading student requests: {e}")
        return pd.DataFrame()
