import pandas as pd
import numpy as np
from typing import Dict, Tuple

class MarketingAnalytics:
    """Handles all marketing analytics and calculations"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    def calculate_channel_performance(self) -> pd.DataFrame:
        """Calculate performance metrics by channel"""
        # Filter out 'Total' rows for channel-specific analysis
        channel_data = self.data[self.data['channel'] != 'Total'].copy()
        
        channel_summary = channel_data.groupby('channel').agg({
            'spend': 'sum',
            'revenue': 'sum',
            'impressions': 'sum',
            'clicks': 'sum'
        }).reset_index()
        
        # Calculate derived metrics
        channel_summary['roas'] = np.where(
            channel_summary['spend'] > 0,
            channel_summary['revenue'] / channel_summary['spend'],
            0
        )
        
        channel_summary['ctr'] = np.where(
            channel_summary['impressions'] > 0,
            (channel_summary['clicks'] / channel_summary['impressions']) * 100,
            0
        )
        
        channel_summary['cpc'] = np.where(
            channel_summary['clicks'] > 0,
            channel_summary['spend'] / channel_summary['clicks'],
            0
        )
        
        channel_summary['cpm'] = np.where(
            channel_summary['impressions'] > 0,
            (channel_summary['spend'] / channel_summary['impressions']) * 1000,
            0
        )
        
        return channel_summary.sort_values('spend', ascending=False)
    
    def calculate_daily_trends(self) -> pd.DataFrame:
        """Calculate daily trend data"""
        daily_trends = self.data[self.data['channel'] == 'Total'].copy()
        daily_trends = daily_trends.sort_values('date').reset_index(drop=True)
        
        # Calculate rolling averages
        daily_trends['spend_7d_avg'] = daily_trends['spend'].rolling(window=7, min_periods=1).mean()
        daily_trends['roas_7d_avg'] = daily_trends['roas'].rolling(window=7, min_periods=1).mean()
        daily_trends['revenue_7d_avg'] = daily_trends['revenue'].rolling(window=7, min_periods=1).mean()
        
        return daily_trends
    
    def calculate_business_impact(self) -> Dict:
        """Calculate business impact metrics"""
        total_data = self.data[self.data['channel'] == 'Total'].copy()
        
        total_marketing_spend = total_data['spend'].sum()
        total_attributed_revenue = total_data['revenue'].sum()
        total_business_revenue = total_data['total_revenue'].sum()
        
        # Calculate attribution percentage
        attribution_rate = (total_attributed_revenue / total_business_revenue * 100) if total_business_revenue > 0 else 0
        
        # Calculate overall ROAS
        overall_roas = (total_attributed_revenue / total_marketing_spend) if total_marketing_spend > 0 else 0
        
        # Calculate efficiency metrics
        avg_daily_spend = total_marketing_spend / len(total_data) if len(total_data) > 0 else 0
        avg_daily_revenue = total_attributed_revenue / len(total_data) if len(total_data) > 0 else 0
        
        return {
            'total_marketing_spend': total_marketing_spend,
            'total_attributed_revenue': total_attributed_revenue,
            'total_business_revenue': total_business_revenue,
            'attribution_rate': attribution_rate,
            'overall_roas': overall_roas,
            'avg_daily_spend': avg_daily_spend,
            'avg_daily_revenue': avg_daily_revenue,
            'data_period_days': len(total_data)
        }
    
    def get_top_performers(self, metric='roas', n=3) -> pd.DataFrame:
        """Get top performing campaigns or channels"""
        channel_perf = self.calculate_channel_performance()
        return channel_perf.nlargest(n, metric)