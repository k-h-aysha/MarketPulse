import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class ChartsDisplay:
    """Handles all chart visualizations"""
    
    @staticmethod
    def daily_spend_trend(daily_data):
        """Daily spend trend chart"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data['spend'],
            mode='lines+markers',
            name='Daily Spend',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data['spend_7d_avg'],
            mode='lines',
            name='7-Day Average',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Daily Marketing Spend Trend",
            xaxis_title="Date",
            yaxis_title="Spend ($)",
            hovermode='x unified',
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def roas_performance_chart(daily_data):
        """ROAS performance over time"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data['roas'],
            mode='lines+markers',
            name='Daily ROAS',
            line=dict(color='#2ca02c', width=2),
            marker=dict(size=6)
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data['roas_7d_avg'],
            mode='lines',
            name='7-Day Avg ROAS',
            line=dict(color='#d62728', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Return on Ad Spend (ROAS) Performance",
            xaxis_title="Date",
            yaxis_title="ROAS",
            hovermode='x unified',
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def channel_comparison_bar(channel_data):
        """Channel comparison bar chart"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Spend',
            x=channel_data['channel'],
            y=channel_data['spend'],
            yaxis='y',
            marker_color='#1f77b4'
        ))
        
        fig.add_trace(go.Scatter(
            name='ROAS',
            x=channel_data['channel'],
            y=channel_data['roas'],
            yaxis='y2',
            mode='lines+markers',
            marker_color='#ff7f0e',
            line=dict(width=3)
        ))
        
        fig.update_layout(
            title="Channel Performance: Spend vs ROAS",
            xaxis_title="Channel",
            yaxis=dict(title="Spend ($)", side="left"),
            yaxis2=dict(title="ROAS", side="right", overlaying="y"),
            hovermode='x unified',
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def funnel_metrics_chart(channel_data):
        """Marketing funnel metrics"""
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Impressions by Channel', 'Clicks by Channel', 
                          'CTR by Channel', 'CPC by Channel'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Impressions
        fig.add_trace(go.Bar(
            x=channel_data['channel'],
            y=channel_data['impressions'],
            name='Impressions',
            marker_color='#1f77b4'
        ), row=1, col=1)
        
        # Clicks
        fig.add_trace(go.Bar(
            x=channel_data['channel'],
            y=channel_data['clicks'],
            name='Clicks',
            marker_color='#ff7f0e'
        ), row=1, col=2)
        
        # CTR
        fig.add_trace(go.Bar(
            x=channel_data['channel'],
            y=channel_data['ctr'],
            name='CTR (%)',
            marker_color='#2ca02c'
        ), row=2, col=1)
        
        # CPC
        fig.add_trace(go.Bar(
            x=channel_data['channel'],
            y=channel_data['cpc'],
            name='CPC ($)',
            marker_color='#d62728'
        ), row=2, col=2)
        
        fig.update_layout(
            title_text="Marketing Funnel Metrics by Channel",
            showlegend=False,
            height=600
        )
        
        return fig
    
    @staticmethod
    def revenue_attribution_pie(business_metrics):
        """Revenue attribution pie chart"""
        attributed = business_metrics['total_attributed_revenue']
        non_attributed = business_metrics['total_business_revenue'] - attributed
        
        fig = go.Figure(data=[go.Pie(
            labels=['Marketing Attributed', 'Other Sources'],
            values=[attributed, non_attributed],
            hole=0.3,
            marker_colors=['#1f77b4', '#ff7f0e']
        )])
        
        fig.update_layout(
            title="Revenue Attribution",
            annotations=[dict(text=f"{business_metrics['attribution_rate']:.1f}%", 
                             x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        return fig
    
    @staticmethod
    def spend_vs_revenue_scatter(daily_data):
        """Spend vs Revenue correlation scatter plot"""
        fig = px.scatter(
            daily_data,
            x='spend',
            y='revenue',
            title='Daily Spend vs Attributed Revenue',
            labels={'spend': 'Daily Spend ($)', 'revenue': 'Daily Revenue ($)'},
            trendline='ols',
            hover_data=['date']
        )
        
        fig.update_layout(
            xaxis_title="Daily Marketing Spend ($)",
            yaxis_title="Daily Attributed Revenue ($)"
        )
        
        return fig