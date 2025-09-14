import pandas as pd
import os
import streamlit as st

class DataLoader:
    """Handles all data loading operations"""
    
    def __init__(self, data_folder='data'):
        self.data_folder = data_folder
        
    def load_csv_files(self):
        """Load all CSV files from data folder"""
        data_files = {
            'facebook': None,
            'google': None,
            'tiktok': None,
            'business': None
        }
        
        if not os.path.exists(self.data_folder):
            return data_files, f"Data folder '{self.data_folder}' not found"
            
        try:
            for file in os.listdir(self.data_folder):
                if file.lower().endswith('.csv'):
                    file_path = os.path.join(self.data_folder, file)
                    
                    if 'facebook' in file.lower():
                        data_files['facebook'] = pd.read_csv(file_path)
                    elif 'google' in file.lower():
                        data_files['google'] = pd.read_csv(file_path)
                    elif 'tiktok' in file.lower():
                        data_files['tiktok'] = pd.read_csv(file_path)
                    elif 'business' in file.lower():
                        data_files['business'] = pd.read_csv(file_path)
                        
        except Exception as e:
            return data_files, f"Error loading files: {str(e)}"
            
        return data_files, None
    
    def validate_data_files(self, data_files):
        """Check if all required files are loaded"""
        required_files = ['facebook', 'google', 'tiktok', 'business']
        missing_files = []
        
        for file_key in required_files:
            if file_key not in data_files or data_files[file_key] is None:
                missing_files.append(f"{file_key}.csv")
                
        if missing_files:
            return False, f"Missing files: {', '.join(missing_files)}"
        
        return True, "All files loaded successfully"