import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class MarketPulseDataProcessor:
    def __init__(self):
        self.processed_data = {}
        self.marketing_combined = None
        self.final_dataset = None
    
    def clean_marketing_data(self, df, channel_name):
        """Clean and standardize marketing data"""
        df_clean = df.copy()
        
        # Standardize column names (lowercase, remove spaces)
        df_clean.columns = df_clean.columns.str.lower().str.replace(' ', '_')
        
        # Handle date column - try common date column names
        date_cols = [col for col in df_clean.columns if 'date' in col.lower()]
        if date_cols:
            date_col = date_cols[0]
            df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
            df_clean = df_clean.rename(columns={date_col: 'date'})
        
        # Add channel identifier
        df_clean['channel'] = channel_name
        
        # Handle missing values in numeric columns
        numeric_cols = ['impressions', 'impression', 'clicks', 'spend', 'attributed_revenue']
        for col in numeric_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
        
        # Standardize column names
        column_mapping = {
            'impression': 'impressions',
            'attributed_revenue': 'revenue'
        }
        df_clean = df_clean.rename(columns=column_mapping)
        
        # Remove rows with invalid dates
        df_clean = df_clean.dropna(subset=['date'])
        
        return df_clean
    
    def clean_business_data(self, df):
        """Clean and standardize business data"""
        df_clean = df.copy()
        
        # Standardize column names
        df_clean.columns = df_clean.columns.str.lower().str.replace(' ', '_')
        
        # Handle date column
        date_cols = [col for col in df_clean.columns if 'date' in col.lower()]
        if date_cols:
            date_col = date_cols[0]
            df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
            df_clean = df_clean.rename(columns={date_col: 'date'})
        
        # Handle missing values in numeric columns
        numeric_cols = ['orders', 'new_orders', 'new_customers', 'total_revenue', 'gross_profit', 'cogs']
        for col in numeric_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
        
        # Remove rows with invalid dates
        df_clean = df_clean.dropna(subset=['date'])
        
        return df_clean
    
    def combine_marketing_data(self, facebook_df, google_df, tiktok_df):
        """Combine all marketing data sources"""
        # Clean each dataset
        facebook_clean = self.clean_marketing_data(facebook_df, 'Facebook')
        google_clean = self.clean_marketing_data(google_df, 'Google')
        tiktok_clean = self.clean_marketing_data(tiktok_df, 'TikTok')
        
        # Combine all marketing data
        marketing_combined = pd.concat([facebook_clean, google_clean, tiktok_clean], 
                                     ignore_index=True, sort=False)
        
        # Fill missing columns with 0
        required_cols = ['impressions', 'clicks', 'spend', 'revenue']
        for col in required_cols:
            if col not in marketing_combined.columns:
                marketing_combined[col] = 0
        
        self.marketing_combined = marketing_combined
        return marketing_combined
    
    def create_derived_metrics(self, df):
        """Create calculated marketing metrics"""
        df_metrics = df.copy()
        
        # Avoid division by zero
        df_metrics['ctr'] = np.where(df_metrics['impressions'] > 0, 
                                   df_metrics['clicks'] / df_metrics['impressions'], 0)
        
        df_metrics['cpc'] = np.where(df_metrics['clicks'] > 0, 
                                   df_metrics['spend'] / df_metrics['clicks'], 0)
        
        df_metrics['roas'] = np.where(df_metrics['spend'] > 0, 
                                    df_metrics['revenue'] / df_metrics['spend'], 0)
        
        df_metrics['cpm'] = np.where(df_metrics['impressions'] > 0, 
                                   (df_metrics['spend'] / df_metrics['impressions']) * 1000, 0)
        
        return df_metrics
    
    def aggregate_daily_marketing(self, marketing_df):
        """Aggregate marketing data by date and channel"""
        daily_marketing = marketing_df.groupby(['date', 'channel']).agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'spend': 'sum',
            'revenue': 'sum',
            'ctr': 'mean',
            'cpc': 'mean',
            'roas': 'mean',
            'cpm': 'mean'
        }).reset_index()
        
        # Also create total daily aggregates
        daily_total = marketing_df.groupby('date').agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'spend': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        # Recalculate metrics for totals
        daily_total = self.create_derived_metrics(daily_total)
        daily_total['channel'] = 'Total'
        
        # Combine channel-specific and total data
        daily_combined = pd.concat([daily_marketing, daily_total], ignore_index=True)
        
        return daily_combined
    
    def merge_marketing_business(self, marketing_daily, business_df):
        """Merge daily marketing data with business data"""
        business_clean = self.clean_business_data(business_df)
        
        # Merge on date
        merged_df = marketing_daily.merge(business_clean, on='date', how='outer')
        
        # Fill missing values
        merged_df = merged_df.fillna(0)
        
        # Sort by date and channel
        merged_df = merged_df.sort_values(['date', 'channel']).reset_index(drop=True)
        
        self.final_dataset = merged_df
        return merged_df
    
    def process_all_data(self, facebook_df, google_df, tiktok_df, business_df):
        """Main processing pipeline"""
        try:
            # Step 1: Combine and clean marketing data
            marketing_combined = self.combine_marketing_data(facebook_df, google_df, tiktok_df)
            
            # Step 2: Create derived metrics
            marketing_with_metrics = self.create_derived_metrics(marketing_combined)
            
            # Step 3: Aggregate daily data
            daily_marketing = self.aggregate_daily_marketing(marketing_with_metrics)
            
            # Step 4: Merge with business data
            final_data = self.merge_marketing_business(daily_marketing, business_df)
            
            return {
                'success': True,
                'marketing_raw': marketing_combined,
                'marketing_daily': daily_marketing,
                'final_dataset': final_data,
                'date_range': f"{final_data['date'].min().date()} to {final_data['date'].max().date()}",
                'total_days': len(final_data['date'].unique())
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'marketing_raw': None,
                'marketing_daily': None,
                'final_dataset': None
            }