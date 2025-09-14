import streamlit as st
import sys
import os

# Add path for imports
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

from src.analytics import MarketingAnalytics
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

st.title("📊 Dashboard Overview")
st.markdown("### Executive Summary & Key Metrics")

# Check if data is loaded in session state
if 'processed_data' not in st.session_state or not st.session_state.processed_data:
    st.warning("⚠️ No data loaded. Please run the main dashboard first.")
    st.markdown("👈 Go back to the main page to load your data.")
    st.stop()

# Get data from session state
processed_data = st.session_state.processed_data
analytics = MarketingAnalytics(processed_data['final_dataset'])

# Calculate metrics
business_metrics = analytics.calculate_business_impact()
channel_performance = analytics.calculate_channel_performance()

# Executive Summary
st.header("📈 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Overall ROAS",
        f"{business_metrics['overall_roas']:.2f}x",
        delta="Return on Ad Spend"
    )

with col2:
    st.metric(
        "Total Attribution",
        f"{business_metrics['attribution_rate']:.1f}%",
        delta="Of total revenue"
    )

with col3:
    st.metric(
        "Marketing Spend",
        f"${business_metrics['total_marketing_spend']:,.0f}",
        delta=f"{business_metrics['data_period_days']} days"
    )

with col4:
    st.metric(
        "Attributed Revenue",
        f"${business_metrics['total_attributed_revenue']:,.0f}",
        delta="Marketing driven"
    )

st.markdown("---")

# Quick Insights
st.header("🔍 Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Performing Channel")
    top_channel = channel_performance.iloc[0]
    st.success(f"**{top_channel['channel']}** leads with **{top_channel['roas']:.2f}x ROAS**")
    st.write(f"• Spend: ${top_channel['spend']:,.0f}")
    st.write(f"• Revenue: ${top_channel['revenue']:,.0f}")
    st.write(f"• CTR: {top_channel['ctr']:.2f}%")

with col2:
    st.subheader("📊 Channel Distribution")
    fig = px.pie(
        channel_performance, 
        values='spend', 
        names='channel',
        title='Marketing Spend by Channel'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Performance Overview
st.header("📊 Performance Overview")

col1, col2 = st.columns(2)

with col1:
    # ROAS comparison
    fig = px.bar(
        channel_performance,
        x='channel',
        y='roas',
        title='ROAS by Channel',
        color='roas',
        color_continuous_scale='viridis'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Spend vs Revenue
    fig = px.scatter(
        channel_performance,
        x='spend',
        y='revenue',
        size='clicks',
        color='channel',
        title='Spend vs Revenue by Channel',
        hover_data=['roas']
    )
    st.plotly_chart(fig, use_container_width=True)

# Summary table
st.header("📋 Channel Summary")
st.dataframe(
    channel_performance,
    column_config={
        "channel": "Channel",
        "spend": st.column_config.NumberColumn("Spend ($)", format="$%.0f"),
        "revenue": st.column_config.NumberColumn("Revenue ($)", format="$%.0f"),
        "roas": st.column_config.NumberColumn("ROAS", format="%.2fx"),
        "ctr": st.column_config.NumberColumn("CTR (%)", format="%.2f%%"),
        "cpc": st.column_config.NumberColumn("CPC ($)", format="$%.2f")
    },
    use_container_width=True,
    hide_index=True
)