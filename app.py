import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import our custom modules
from src.data_loader import DataLoader
from src.data_processor import MarketPulseDataProcessor
from src.analytics import MarketingAnalytics
from components.metrics import MetricsDisplay
from components.charts import ChartsDisplay
from components.tables import TablesDisplay
from utils.helpers import Helpers

# Page configuration
st.set_page_config(
    page_title="MarketPulse Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.processed_data = None

@st.cache_data
def load_and_process_data():
    """Load and process all data using modular components"""
    
    # Step 1: Load data
    loader = DataLoader()
    data_files, load_error = loader.load_csv_files()
    
    if load_error:
        return None, load_error
    
    # Step 2: Validate data
    is_valid, validation_message = loader.validate_data_files(data_files)
    if not is_valid:
        return None, validation_message
    
    # Step 3: Process data
    processor = MarketPulseDataProcessor()
    result = processor.process_all_data(
        data_files['facebook'],
        data_files['google'],
        data_files['tiktok'],
        data_files['business']
    )
    
    if not result['success']:
        return None, result['error']
    
    return result, None

def main():
    """Main dashboard application"""
    
    # Header
    st.title("📊 MarketPulse Dashboard")
    st.markdown("### Marketing Intelligence & Business Performance Analytics")
    
    # Sidebar Controls
    st.sidebar.header("🎯 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Load and process data
    with st.spinner("🔄 Loading and processing data..."):
        processed_data, error = load_and_process_data()
        if processed_data and not error:
        # Store in session state for other pages
            st.session_state.processed_data = processed_data
    
    if error:
        st.error(f"❌ Error: {error}")
        st.info("📋 Please ensure all CSV files are in the `data/` folder:")
        st.code("- Facebook.csv\n- Google.csv\n- TikTok.csv\n- Business.csv")
        return
    
    if not processed_data:
        st.error("❌ Failed to load and process data")
        return
    
    # Store in session state
    st.session_state.data_loaded = True
    st.session_state.processed_data = processed_data
    
    # Initialize analytics
    analytics = MarketingAnalytics(processed_data['final_dataset'])
    
    # Calculate key metrics
    business_metrics = analytics.calculate_business_impact()
    channel_performance = analytics.calculate_channel_performance()
    daily_trends = analytics.calculate_daily_trends()
    
    # Sidebar date filter
    st.sidebar.subheader("📅 Date Range Filter")
    date_options = Helpers.get_date_range_options(daily_trends)
    
    if date_options:
        start_date = st.sidebar.date_input(
            "Start Date", 
            value=date_options['default_start'],
            min_value=date_options['min_date'],
            max_value=date_options['max_date']
        )
        
        end_date = st.sidebar.date_input(
            "End Date",
            value=date_options['default_end'], 
            min_value=date_options['min_date'],
            max_value=date_options['max_date']
        )
        
        # Filter data based on date selection
        if start_date <= end_date:
            daily_trends = Helpers.filter_data_by_date(daily_trends, start_date, end_date)
        else:
            st.sidebar.error("Start date must be before end date")
    
    # Sidebar channel filter
    st.sidebar.subheader("📺 Channel Filter")
    available_channels = ['All'] + list(channel_performance['channel'].unique())
    selected_channels = st.sidebar.multiselect(
        "Select Channels",
        available_channels,
        default=['All']
    )
    
    # Apply channel filter
    if 'All' not in selected_channels and selected_channels:
        filtered_channel_performance = channel_performance[
            channel_performance['channel'].isin(selected_channels)
        ]
    else:
        filtered_channel_performance = channel_performance
    
    st.sidebar.markdown("---")
    
    # Main Dashboard Content
    
    # 1. Executive Summary
    st.header("📈 Executive Summary")
    MetricsDisplay.show_processing_status(processed_data)
    st.markdown("---")
    MetricsDisplay.show_kpi_cards(business_metrics)
    
    st.markdown("---")
    
    # 2. Channel Performance Overview
    st.header("🎯 Channel Performance Overview")
    MetricsDisplay.show_channel_cards(filtered_channel_performance)
    
    # Channel comparison chart
    col1, col2 = st.columns(2)
    
    with col1:
        chart1 = ChartsDisplay.channel_comparison_bar(filtered_channel_performance)
        st.plotly_chart(chart1, use_container_width=True)
    
    with col2:
        chart2 = ChartsDisplay.revenue_attribution_pie(business_metrics)
        st.plotly_chart(chart2, use_container_width=True)
    
    st.markdown("---")
    
    # 3. Performance Trends
    st.header("📊 Performance Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trend_chart1 = ChartsDisplay.daily_spend_trend(daily_trends)
        st.plotly_chart(trend_chart1, use_container_width=True)
    
    with col2:
        trend_chart2 = ChartsDisplay.roas_performance_chart(daily_trends)
        st.plotly_chart(trend_chart2, use_container_width=True)
    
    # Spend vs Revenue correlation
    correlation_chart = ChartsDisplay.spend_vs_revenue_scatter(daily_trends)
    st.plotly_chart(correlation_chart, use_container_width=True)
    
    st.markdown("---")
    
    # 4. Detailed Analytics
    st.header("🔍 Detailed Analytics")
    
    # Marketing funnel metrics
    funnel_chart = ChartsDisplay.funnel_metrics_chart(filtered_channel_performance)
    st.plotly_chart(funnel_chart, use_container_width=True)
    
    st.markdown("---")
    
    # 5. Data Tables
    st.header("📋 Detailed Data")
    
    tab1, tab2, tab3 = st.tabs(["📊 Channel Performance", "📅 Daily Trends", "💼 Business Metrics"])
    
    with tab1:
        TablesDisplay.channel_performance_table(filtered_channel_performance)
    
    with tab2:
        TablesDisplay.daily_data_table(daily_trends)
    
    with tab3:
        TablesDisplay.business_metrics_table(business_metrics)
    
    st.markdown("---")
    
    # 6. Data Quality & Info
    with st.expander("🔍 Data Quality & Information"):
        st.subheader("Data Quality Checks")
        
        col1, col2, col3 = st.columns(3)
        
        final_data = processed_data['final_dataset']
        
        with col1:
            missing_dates = final_data['date'].isnull().sum()
            st.metric("Missing Dates", missing_dates, 
                     delta="✅ Good" if missing_dates == 0 else "⚠️ Issues")
        
        with col2:
            negative_spend = (final_data['spend'] < 0).sum()
            st.metric("Negative Spend Records", negative_spend,
                     delta="✅ Good" if negative_spend == 0 else "⚠️ Issues")
        
        with col3:
            zero_days = len(final_data[final_data['spend'] == 0])
            st.metric("Zero Spend Days", zero_days, delta="ℹ️ Normal")
        
        # Show data info
        Helpers.show_data_info(final_data, "Final Dataset Information")
        Helpers.show_data_info(processed_data['marketing_raw'], "Raw Marketing Data Information")

    # Footer
    st.markdown("---")
    st.markdown("*Built with ❤️ using Streamlit & Plotly | MarketPulse Dashboard v1.0*")

if __name__ == "__main__":
    main()