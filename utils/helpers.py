import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class Helpers:
    """Utility functions for the dashboard"""
    
    @staticmethod
    def format_currency(value):
        """Format number as currency"""
        if pd.isna(value) or value == 0:
            return "$0"
        return f"${value:,.0f}"
    
    @staticmethod
    def format_percentage(value):
        """Format number as percentage"""
        if pd.isna(value):
            return "0.0%"
        return f"{value:.1f}%"
    
    @staticmethod
    def format_number(value, decimals=0):
        """Format number with commas"""
        if pd.isna(value):
            return "0"
        if decimals == 0:
            return f"{value:,.0f}"
        return f"{value:,.{decimals}f}"
    
    @staticmethod
    def get_date_range_options(df):
        """Get date range options from dataframe"""
        if 'date' not in df.columns:
            return None
        
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        
        return {
            'min_date': min_date,
            'max_date': max_date,
            'default_start': min_date,
            'default_end': max_date
        }
    
    @staticmethod
    def filter_data_by_date(df, start_date, end_date):
        """Filter dataframe by date range"""
        if 'date' not in df.columns:
            return df
        
        return df[
            (df['date'].dt.date >= start_date) & 
            (df['date'].dt.date <= end_date)
        ].copy()
    
    @staticmethod
    def validate_data_completeness(df, required_columns):
        """Validate that dataframe has required columns"""
        missing_columns = []
        for col in required_columns:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            return False, f"Missing columns: {', '.join(missing_columns)}"
        
        return True, "All required columns present"
    
    @staticmethod
    def show_data_info(df, title="Data Information"):
        """Show basic data information"""
        st.info(f"""
        **{title}**
        - Rows: {len(df):,}
        - Columns: {len(df.columns)}
        - Date Range: {df['date'].min().date()} to {df['date'].max().date()}
        - Memory Usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB
        """)