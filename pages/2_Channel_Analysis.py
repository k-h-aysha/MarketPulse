import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add path for imports
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

from src.analytics import MarketingAnalytics

st.set_page_config(page_title="Channel Analysis", page_icon="📈", layout="wide")

st.title("📈 Channel Deep Dive")
st.markdown("### Detailed Channel Performance Analysis")

# Check if data is loaded
if 'processed_data' not in st.session_state or not st.session_state.processed_data:
    st.warning("⚠️ No data loaded. Please run the main dashboard first.")
    st.stop()

processed_data = st.session_state.processed_data
analytics = MarketingAnalytics(processed_data['final_dataset'])

# Get channel performance
channel_performance = analytics.calculate_channel_performance()
daily_trends = analytics.calculate_daily_trends()

# Sidebar for channel selection
st.sidebar.header("📊 Channel Controls")
selected_channels = st.sidebar.multiselect(
    "Select Channels to Compare",
    channel_performance['channel'].tolist(),
    default=channel_performance['channel'].tolist()
)

# Filter data
filtered_channels = channel_performance[
    channel_performance['channel'].isin(selected_channels)
]

# Channel comparison
st.header("🔄 Channel Comparison")

if len(selected_channels) > 0:
    # Create subplots for different metrics
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Spend Comparison', 'ROAS Comparison', 
                       'CTR Comparison', 'CPC Comparison'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Spend
    fig.add_trace(go.Bar(
        x=filtered_channels['channel'],
        y=filtered_channels['spend'],
        name='Spend',
        marker_color='#1f77b4'
    ), row=1, col=1)
    
    # ROAS
    fig.add_trace(go.Bar(
        x=filtered_channels['channel'],
        y=filtered_channels['roas'],
        name='ROAS',
        marker_color='#ff7f0e'
    ), row=1, col=2)
    
    # CTR
    fig.add_trace(go.Bar(
        x=filtered_channels['channel'],
        y=filtered_channels['ctr'],
        name='CTR',
        marker_color='#2ca02c'
    ), row=2, col=1)
    
    # CPC
    fig.add_trace(go.Bar(
        x=filtered_channels['channel'],
        y=filtered_channels['cpc'],
        name='CPC',
        marker_color='#d62728'
    ), row=2, col=2)
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Efficiency Analysis
    st.header("⚡ Efficiency Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost efficiency
        fig = px.bar(
            filtered_channels,
            x='channel',
            y=['cpc', 'cpm'],
            title='Cost Efficiency: CPC vs CPM',
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Performance efficiency
        efficiency_data = filtered_channels.copy()
        efficiency_data['conversion_rate'] = (
            efficiency_data['clicks'] / efficiency_data['impressions'] * 100
        )
        
        fig = px.scatter(
            efficiency_data,
            x='cpc',
            y='roas',
            size='spend',
            color='channel',
            title='Cost vs Performance Efficiency',
            labels={'cpc': 'Cost Per Click ($)', 'roas': 'Return on Ad Spend'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed metrics table
    st.header("📊 Detailed Channel Metrics")
    st.dataframe(filtered_channels, use_container_width=True)

else:
    st.warning("Please select at least one channel to analyze.")