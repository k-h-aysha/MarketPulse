import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
import plotly.express as px
import plotly.graph_objects as go

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import our custom modules
from src.data_loader import DataLoader
from src.data_processor import MarketPulseDataProcessor
from src.analytics import MarketingAnalytics

# Page configuration
st.set_page_config(
    page_title="MarketPulse Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def filter_data_by_date_range(data, start_date, end_date):
    """Filter data by date range"""
    if 'date' not in data.columns:
        return data
    return data[(data['date'].dt.date >= start_date) & (data['date'].dt.date <= end_date)].copy()

def display_performance_alerts(analytics):
    """Display performance alerts and warnings"""
    insights = analytics.get_performance_insights()
    
    # Check for critical issues
    critical_insights = [i for i in insights if i['priority'] == 'High']
    
    if critical_insights:
        st.warning("⚠️ **Performance Alerts Detected**")
        for insight in critical_insights[:2]:  # Show top 2 critical alerts
            st.error(f"**{insight['type']}:** {insight['insight']}")

def main():
    """Enhanced main dashboard application"""
    
    # Header with enhanced styling
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #1f77b4; margin-bottom: 0;">📊 MarketPulse Dashboard</h1>
        <p style="font-size: 1.2rem; color: #6c757d; margin-top: 0.5rem;">
            Marketing Intelligence & Business Performance Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load and process data
    with st.spinner("🔄 Loading and processing data..."):
        processed_data, error = load_and_process_data()
    
    if error:
        st.error(f"❌ Error: {error}")
        st.info("📋 Please ensure all CSV files are in the `data/` folder:")
        st.code("- Facebook.csv\n- Google.csv\n- TikTok.csv\n- Business.csv")
        return
    
    if not processed_data:
        st.error("❌ Failed to load and process data")
        return
    
    # Store in session state for other pages
    st.session_state.processed_data = processed_data
    
    # Sidebar with enhanced controls
    st.sidebar.header("🎯 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Date range filter
    st.sidebar.subheader("📅 Time Period Analysis")
    
    # Get date range from data
    all_dates = processed_data['final_dataset']['date'].dt.date
    min_date = all_dates.min()
    max_date = all_dates.max()
    
    # Quick date range options
    date_option = st.sidebar.selectbox(
        "Quick Select",
        ["Custom Range", "Last 7 Days", "Last 14 Days", "Last 30 Days", "All Time"]
    )
    
    if date_option == "Last 7 Days":
        start_date = max_date - timedelta(days=7)
        end_date = max_date
    elif date_option == "Last 14 Days":
        start_date = max_date - timedelta(days=14)
        end_date = max_date
    elif date_option == "Last 30 Days":
        start_date = max_date - timedelta(days=30)
        end_date = max_date
    elif date_option == "All Time":
        start_date = min_date
        end_date = max_date
    else:  # Custom Range
        start_date = st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
        end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)
    
    # Channel filter
    st.sidebar.subheader("📺 Channel Focus")
    available_channels = ['All Channels'] + list(processed_data['marketing_daily']['channel'].unique())
    available_channels = [ch for ch in available_channels if ch != 'Total']  # Remove 'Total' from options
    
    selected_channels = st.sidebar.multiselect(
        "Select Channels",
        available_channels,
        default=['All Channels']
    )
    
    # Comparison mode
    st.sidebar.subheader("📊 Analysis Mode")
    comparison_mode = st.sidebar.radio(
        "View Type",
        ["Current Period", "Period Comparison", "Trend Analysis"]
    )
    
    if comparison_mode == "Period Comparison":
        st.sidebar.write("**Compare with:**")
        comparison_period = st.sidebar.selectbox(
            "Previous Period",
            ["Previous Period (Same Length)", "Month Ago", "Quarter Ago"]
        )
    
    st.sidebar.markdown("---")
    
    # Filter data based on selections
    filtered_final_data = filter_data_by_date_range(processed_data['final_dataset'], start_date, end_date)
    filtered_marketing_data = filter_data_by_date_range(processed_data['marketing_daily'], start_date, end_date)
    
    # Apply channel filter
    if 'All Channels' not in selected_channels and selected_channels:
        filtered_final_data = filtered_final_data[
            (filtered_final_data['channel'].isin(selected_channels)) | 
            (filtered_final_data['channel'] == 'Total')
        ]
        filtered_marketing_data = filtered_marketing_data[
            (filtered_marketing_data['channel'].isin(selected_channels)) |
            (filtered_marketing_data['channel'] == 'Total')
        ]
    
    # Initialize analytics with filtered data
    analytics = MarketingAnalytics(filtered_final_data)
    
    # Display performance alerts
    display_performance_alerts(analytics)
    
    # Calculate metrics
    business_metrics = analytics.calculate_business_impact()
    channel_performance = analytics.calculate_channel_performance()
    daily_trends = analytics.calculate_daily_trends()
    
    # Success message with period info
    period_text = f"{start_date} to {end_date}"
    st.success(f"🎉 Data loaded successfully | Analyzing: {period_text} ({len(daily_trends)} days)")
    
    st.markdown("---")
    
    # Enhanced KPI Cards with comparison
    st.header("📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        roas_status = "🚀" if business_metrics['overall_roas'] > 4 else "📈" if business_metrics['overall_roas'] > 2.5 else "⚠️"
        st.metric(
            f"{roas_status} Total ROAS",
            f"{business_metrics['overall_roas']:.2f}x",
            delta=f"${business_metrics['total_marketing_spend']:,.0f} invested"
        )
    
    with col2:
        attr_status = "🎯" if business_metrics['attribution_rate'] > 20 else "📊" if business_metrics['attribution_rate'] > 10 else "🔍"
        st.metric(
            f"{attr_status} Marketing Attribution",
            f"{business_metrics['attribution_rate']:.1f}%",
            delta=f"${business_metrics['total_attributed_revenue']:,.0f} revenue"
        )
    
    with col3:
        efficiency = business_metrics['total_attributed_revenue'] / business_metrics['total_marketing_spend'] if business_metrics['total_marketing_spend'] > 0 else 0
        eff_status = "💰" if efficiency > 4 else "💵" if efficiency > 2 else "💸"
        st.metric(
            f"{eff_status} Marketing Efficiency",
            f"${efficiency:.2f}",
            delta="Revenue per $ spent"
        )
    
    with col4:
        daily_avg = business_metrics['avg_daily_revenue']
        avg_status = "📈" if daily_avg > 10000 else "📊" if daily_avg > 5000 else "📉"
        st.metric(
            f"{avg_status} Daily Avg Revenue",
            f"${daily_avg:,.0f}",
            delta=f"{business_metrics['data_period_days']} days analyzed"
        )
    
    st.markdown("---")
    
    # Enhanced Channel Performance with insights
    st.header("🎯 Channel Performance Matrix")
    
    if not channel_performance.empty:
        # Channel performance cards with enhanced styling
        cols = st.columns(len(channel_performance))
        
        for idx, (_, row) in enumerate(channel_performance.iterrows()):
            with cols[idx]:
                # Performance grade based on ROAS
                if row['roas'] > 4:
                    grade, color = "A+", "🟢"
                elif row['roas'] > 3:
                    grade, color = "A", "🟡"  
                elif row['roas'] > 2:
                    grade, color = "B", "🟠"
                else:
                    grade, color = "C", "🔴"
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                    padding: 1rem;
                    border-radius: 8px;
                    border: 1px solid #dee2e6;
                    text-align: center;
                    margin-bottom: 1rem;
                ">
                    <h4 style="margin: 0 0 0.5rem 0; color: #495057;">{row['channel']}</h4>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #28a745; margin: 0.5rem 0;">
                        {row['roas']:.2f}x ROAS
                    </div>
                    <div style="color: #6c757d; font-size: 0.9rem;">
                        CTR: {row['ctr']*100:.2f}% | Grade: {color} {grade}
                    </div>
                    <div style="color: #6c757d; font-size: 0.85rem; margin-top: 0.5rem;">
                        ${row['spend']:,.0f} spend
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Enhanced performance table
    st.subheader("📊 Detailed Channel Metrics")
    if not channel_performance.empty:
        st.dataframe(
            channel_performance,
            column_config={
                "channel": st.column_config.TextColumn("Channel", width="medium"),
                "spend": st.column_config.NumberColumn("Spend ($)", format="$%.0f", width="medium"),
                "revenue": st.column_config.NumberColumn("Revenue ($)", format="$%.0f", width="medium"),
                "impressions": st.column_config.NumberColumn("Impressions", format="%.0f", width="medium"),
                "clicks": st.column_config.NumberColumn("Clicks", format="%.0f", width="small"),
                "roas": st.column_config.NumberColumn("ROAS", format="%.2fx", width="small"),
                "ctr": st.column_config.NumberColumn("CTR", format="%.3f%%", width="small"),
                "cpc": st.column_config.NumberColumn("CPC ($)", format="$%.2f", width="small"),
                "cpm": st.column_config.NumberColumn("CPM ($)", format="$%.2f", width="small")
            },
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    
    # Enhanced visualization section
    st.header("📈 Performance Visualizations")
    
    tab1, tab2, tab3 = st.tabs(["📊 Channel Analysis", "📈 Trend Analysis", "🎯 Efficiency Matrix"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            if not channel_performance.empty:
                fig1 = px.bar(
                    channel_performance,
                    x='channel',
                    y='spend',
                    title='Marketing Investment by Channel',
                    color='roas',
                    color_continuous_scale='RdYlGn',
                    text='spend'
                )
                fig1.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
                fig1.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            if not channel_performance.empty:
                fig2 = px.scatter(
                    channel_performance,
                    x='spend',
                    y='revenue',
                    size='clicks',
                    color='channel',
                    title='ROI Efficiency: Spend vs Revenue',
                    hover_data=['roas', 'ctr']
                )
                fig2.update_layout(height=400)
                st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        if not daily_trends.empty:
            # Trend analysis charts
            fig3 = go.Figure()
            
            fig3.add_trace(go.Scatter(
                x=daily_trends['date'],
                y=daily_trends['spend'],
                mode='lines+markers',
                name='Daily Spend',
                line=dict(color='#1f77b4', width=2),
                yaxis='y'
            ))
            
            fig3.add_trace(go.Scatter(
                x=daily_trends['date'],
                y=daily_trends['revenue'],
                mode='lines+markers',
                name='Daily Revenue',
                line=dict(color='#2ca02c', width=2),
                yaxis='y2'
            ))
            
            fig3.update_layout(
                title='Spend vs Revenue Trend Analysis',
                xaxis_title='Date',
                yaxis=dict(title='Spend ($)', side='left'),
                yaxis2=dict(title='Revenue ($)', side='right', overlaying='y'),
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig3, use_container_width=True)
            
            # ROAS trend
            fig4 = px.line(
                daily_trends,
                x='date',
                y='roas',
                title='ROAS Performance Trend',
                line_shape='spline'
            )
            
            # Add average line
            avg_roas = daily_trends['roas'].mean()
            fig4.add_hline(y=avg_roas, line_dash="dash", 
                          annotation_text=f"Average: {avg_roas:.2f}x")
            fig4.update_layout(height=400)
            
            st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
        if not channel_performance.empty:
            # Efficiency matrix
            fig5 = px.scatter(
                channel_performance,
                x='cpc',
                y='roas',
                size='spend',
                color='ctr',
                title='Marketing Efficiency Matrix',
                labels={'cpc': 'Cost Per Click ($)', 'roas': 'Return on Ad Spend', 'ctr': 'CTR'},
                hover_data=['channel', 'spend', 'revenue']
            )
            
            # Add quadrant lines
            avg_cpc = channel_performance['cpc'].median()
            avg_roas = channel_performance['roas'].median()
            
            fig5.add_hline(y=avg_roas, line_dash="dash", line_color="gray", opacity=0.5)
            fig5.add_vline(x=avg_cpc, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Add quadrant annotations
            fig5.add_annotation(x=avg_cpc*0.5, y=avg_roas*1.5, text="High ROAS<br>Low CPC", 
                               bgcolor="lightgreen", opacity=0.7)
            fig5.add_annotation(x=avg_cpc*1.5, y=avg_roas*0.5, text="Low ROAS<br>High CPC", 
                               bgcolor="lightcoral", opacity=0.7)
            
            fig5.update_layout(height=500)
            st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("---")
    
    # Footer with insights
    st.header("💡 Quick Insights")
    insights = analytics.get_performance_insights()
    
    if insights:
        insight_cols = st.columns(len(insights[:3]))
        for i, insight in enumerate(insights[:3]):
            with insight_cols[i]:
                priority_color = "#dc3545" if insight['priority'] == 'High' else "#ffc107" if insight['priority'] == 'Medium' else "#28a745"
                st.markdown(f"""
                <div style="
                    border: 1px solid {priority_color};
                    border-radius: 8px;
                    padding: 1rem;
                    background: rgba(255,255,255,0.9);
                ">
                    <strong style="color: {priority_color};">{insight['type']}</strong><br>
                    <small>{insight['insight'][:100]}...</small>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <em>Built with ❤️ using Streamlit & Plotly | MarketPulse Dashboard v2.0</em><br>
        <small>Navigate to other pages for detailed analysis →</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()