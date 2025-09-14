import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class MarketingAnalytics:
    """Enhanced marketing analytics with business intelligence capabilities"""
    
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
            (channel_summary['clicks'] / channel_summary['impressions']),
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
    
    # NEW BUSINESS INTELLIGENCE METHODS
    
    def get_performance_insights(self) -> List[Dict]:
        """Generate actionable business insights"""
        insights = []
        channel_perf = self.calculate_channel_performance()
        business_metrics = self.calculate_business_impact()
        
        # Best performing channel insight
        if not channel_perf.empty:
            top_channel = channel_perf.iloc[0]
            insights.append({
                'type': 'Top Performer',
                'priority': 'High',
                'insight': f"{top_channel['channel']} delivers the highest ROAS at {top_channel['roas']:.2f}x with ${top_channel['spend']:,.0f} spend",
                'recommendation': f"Consider scaling {top_channel['channel']} budget by 15-20% to maximize returns",
                'impact': f"Potential revenue increase: ${top_channel['spend'] * 0.2 * top_channel['roas']:,.0f}"
            })
        
        # Underperforming channels
        low_roas_channels = channel_perf[channel_perf['roas'] < 2.0]
        if not low_roas_channels.empty:
            underperforming = ', '.join(low_roas_channels['channel'].tolist())
            potential_savings = low_roas_channels['spend'].sum() * 0.15
            insights.append({
                'type': 'Optimization Opportunity',
                'priority': 'High',
                'insight': f"{underperforming} showing ROAS below 2.0x benchmark",
                'recommendation': 'Review targeting, creative assets, or consider reducing spend by 15%',
                'impact': f"Potential cost savings: ${potential_savings:,.0f}"
            })
        
        # High CTR, Low Conversion insight
        high_ctr_low_roas = channel_perf[(channel_perf['ctr'] > channel_perf['ctr'].median()) & 
                                        (channel_perf['roas'] < channel_perf['roas'].median())]
        if not high_ctr_low_roas.empty:
            channel_name = high_ctr_low_roas.iloc[0]['channel']
            insights.append({
                'type': 'Conversion Optimization',
                'priority': 'Medium',
                'insight': f"{channel_name} has good engagement (CTR: {high_ctr_low_roas.iloc[0]['ctr']*100:.2f}%) but low conversion",
                'recommendation': 'Optimize landing pages, improve offer relevance, or adjust attribution windows',
                'impact': 'Could improve ROAS by 25-40% with better conversion rates'
            })
        
        # Attribution rate insight
        if business_metrics['attribution_rate'] < 15:
            insights.append({
                'type': 'Attribution Gap',
                'priority': 'Medium',
                'insight': f"Marketing attribution rate is {business_metrics['attribution_rate']:.1f}% - potentially missing conversions",
                'recommendation': 'Implement view-through conversions, extend attribution windows, or improve tracking',
                'impact': 'Better attribution could reveal 20-30% more marketing value'
            })
        
        # Budget concentration risk
        if not channel_perf.empty:
            top_channel_share = channel_perf.iloc[0]['spend'] / channel_perf['spend'].sum()
            if top_channel_share > 0.6:
                insights.append({
                    'type': 'Portfolio Risk',
                    'priority': 'Medium',
                    'insight': f"Marketing spend heavily concentrated in {channel_perf.iloc[0]['channel']} ({top_channel_share*100:.0f}%)",
                    'recommendation': 'Diversify marketing mix to reduce platform dependency and discover new growth channels',
                    'impact': 'Risk mitigation and potential new revenue streams'
                })
        
        return insights[:5]  # Return top 5 insights
    
    def calculate_efficiency_benchmarks(self) -> Dict:
        """Calculate efficiency scores and benchmarks"""
        channel_perf = self.calculate_channel_performance()
        
        if channel_perf.empty:
            return {}
        
        # Industry benchmarks (these would typically come from external data)
        benchmarks = {
            'roas_benchmark': 3.0,
            'ctr_benchmark': 0.02,  # 2%
            'cpc_benchmark': 2.0
        }
        
        # Calculate efficiency scores
        results = {}
        for _, row in channel_perf.iterrows():
            channel = row['channel']
            
            # Composite efficiency score (0-100)
            roas_score = min(100, (row['roas'] / benchmarks['roas_benchmark']) * 100)
            ctr_score = min(100, (row['ctr'] / benchmarks['ctr_benchmark']) * 100)
            cpc_score = min(100, (benchmarks['cpc_benchmark'] / max(row['cpc'], 0.1)) * 100)
            
            efficiency_score = (roas_score * 0.5 + ctr_score * 0.3 + cpc_score * 0.2)
            
            results[channel] = {
                'efficiency_score': efficiency_score,
                'roas_vs_benchmark': row['roas'] / benchmarks['roas_benchmark'],
                'ctr_vs_benchmark': row['ctr'] / benchmarks['ctr_benchmark'],
                'cpc_vs_benchmark': benchmarks['cpc_benchmark'] / max(row['cpc'], 0.1),
                'performance_grade': self._get_performance_grade(efficiency_score)
            }
        
        return results
    
    def _get_performance_grade(self, score: float) -> str:
        """Convert efficiency score to letter grade"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B+'
        elif score >= 60:
            return 'B'
        elif score >= 50:
            return 'C'
        else:
            return 'D'
    
    def calculate_seasonal_patterns(self) -> Dict:
        """Identify seasonal patterns in performance"""
        daily_data = self.data[self.data['channel'] == 'Total'].copy()
        
        if len(daily_data) < 30:  # Need at least a month of data
            return {}
        
        daily_data['day_of_week'] = daily_data['date'].dt.day_name()
        daily_data['week_number'] = daily_data['date'].dt.isocalendar().week
        
        # Day of week analysis
        dow_performance = daily_data.groupby('day_of_week').agg({
            'spend': 'mean',
            'revenue': 'mean',
            'roas': 'mean'
        }).reset_index()
        
        # Find best and worst performing days
        best_day = dow_performance.loc[dow_performance['roas'].idxmax()]
        worst_day = dow_performance.loc[dow_performance['roas'].idxmin()]
        
        return {
            'best_day': {
                'day': best_day['day_of_week'],
                'avg_roas': best_day['roas'],
                'avg_spend': best_day['spend']
            },
            'worst_day': {
                'day': worst_day['day_of_week'],
                'avg_roas': worst_day['roas'], 
                'avg_spend': worst_day['spend']
            },
            'dow_performance': dow_performance
        }
    
    def calculate_budget_optimization_opportunities(self) -> Dict:
        """Calculate budget reallocation opportunities"""
        channel_perf = self.calculate_channel_performance()
        
        if len(channel_perf) < 2:
            return {}
        
        opportunities = {}
        
        # Sort by ROAS efficiency
        sorted_channels = channel_perf.sort_values('roas', ascending=False)
        
        top_performer = sorted_channels.iloc[0]
        bottom_performer = sorted_channels.iloc[-1]
        
        # Calculate reallocation impact
        reallocation_amount = bottom_performer['spend'] * 0.2  # Move 20% of worst performer
        projected_revenue_gain = reallocation_amount * top_performer['roas']
        projected_revenue_loss = reallocation_amount * bottom_performer['roas']
        net_gain = projected_revenue_gain - projected_revenue_loss
        
        opportunities['reallocation'] = {
            'from_channel': bottom_performer['channel'],
            'to_channel': top_performer['channel'],
            'amount': reallocation_amount,
            'projected_net_gain': net_gain,
            'roi_improvement': (net_gain / reallocation_amount) if reallocation_amount > 0 else 0
        }
        
        # Scale-up opportunities (channels with ROAS > 3.0)
        scale_up_channels = channel_perf[channel_perf['roas'] > 3.0]
        opportunities['scale_up'] = scale_up_channels[['channel', 'roas', 'spend']].to_dict('records')
        
        # Optimization needed (channels with ROAS < 2.0)
        optimize_channels = channel_perf[channel_perf['roas'] < 2.0]
        opportunities['optimize'] = optimize_channels[['channel', 'roas', 'spend']].to_dict('records')
        
        return opportunities
    
    def generate_executive_summary(self) -> Dict:
        """Generate executive summary with key metrics and recommendations"""
        business_metrics = self.calculate_business_impact()
        channel_perf = self.calculate_channel_performance()
        insights = self.get_performance_insights()
        
        # Performance status
        overall_roas = business_metrics['overall_roas']
        performance_status = 'Excellent' if overall_roas > 4 else 'Good' if overall_roas > 2.5 else 'Needs Improvement'
        
        # Top 3 recommendations
        high_priority_insights = [i for i in insights if i['priority'] == 'High']
        top_recommendations = [i['recommendation'] for i in high_priority_insights[:3]]
        
        return {
            'performance_status': performance_status,
            'overall_roas': overall_roas,
            'attribution_rate': business_metrics['attribution_rate'],
            'total_spend': business_metrics['total_marketing_spend'],
            'total_revenue': business_metrics['total_attributed_revenue'],
            'top_channel': channel_perf.iloc[0]['channel'] if not channel_perf.empty else 'N/A',
            'top_recommendations': top_recommendations,
            'key_insights': insights[:3]
        }