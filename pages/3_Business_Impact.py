import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go

# Add path for imports
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

from src.analytics import MarketingAnalytics

st.set_page_config(page_title="Business Impact", page_icon="💰", layout="wide")

st.title("💰 Business Impact Analysis")
st.markdown("### Marketing's Impact on Business Outcomes")

# Check if data is loaded
if 'processed_data' not in st.session_state or not st.session_state.processed_data:
    st.warning("⚠️ No data loaded. Please run the main dashboard first.")
    st.stop()

processed_data = st.session_state.processed_data
analytics = MarketingAnalytics(processed_data['final_dataset'])

# Business metrics
business_metrics = analytics.calculate_business_impact()
daily_trends = analytics.calculate_daily_trends()

# Revenue Attribution
st.header("📈 Revenue Attribution")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Business Revenue",
        f"${business_metrics['total_business_revenue']:,.0f}",
        delta="All sources"
    )

with col2:
    st.metric(
        "Marketing Attributed",
        f"${business_metrics['total_attributed_revenue']:,.0f}",
        delta=f"{business_metrics['attribution_rate']:.1f}% of total"
    )

with col3:
    st.metric(
        "Non-Marketing Revenue", 
        f"${business_metrics['total_business_revenue'] - business_metrics['total_attributed_revenue']:,.0f}",
        delta=f"{100 - business_metrics['attribution_rate']:.1f}% of total"
    )

# Attribution pie chart
attributed_revenue = business_metrics['total_attributed_revenue']
other_revenue = business_metrics['total_business_revenue'] - attributed_revenue

fig = go.Figure(data=[go.Pie(
    labels=['Marketing Attributed', 'Other Sources'],
    values=[attributed_revenue, other_revenue],
    hole=0.4,
    marker_colors=['#1f77b4', '#ff7f0e']
)])

fig.update_layout(
    title="Revenue Source Attribution",
    annotations=[dict(
        text=f"Marketing<br>{business_metrics['attribution_rate']:.1f}%", 
        x=0.5, y=0.5, font_size=16, showarrow=False
    )]
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ROI Analysis
st.header("💹 Return on Investment Analysis")

col1, col2 = st.columns(2)

with col1:
    # Daily spend vs revenue trend
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_trends['date'],
        y=daily_trends['spend'],
        mode='lines',
        name='Daily Marketing Spend',
        line=dict(color='red', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_trends['date'],
        y=daily_trends['revenue'],
        mode='lines',
        name='Daily Attributed Revenue',
        yaxis='y2',
        line=dict(color='green', width=2)
    ))
    
    fig.update_layout(
        title="Marketing Spend vs Attributed Revenue",
        xaxis_title="Date",
        yaxis=dict(title="Marketing Spend ($)", side="left"),
        yaxis2=dict(title="Attributed Revenue ($)", side="right", overlaying="y"),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # ROAS trend
    fig = px.line(
        daily_trends,
        x='date',
        y='roas',
        title='Daily ROAS Trend',
        labels={'roas': 'Return on Ad Spend', 'date': 'Date'}
    )
    
    # Add average line
    avg_roas = daily_trends['roas'].mean()
    fig.add_hline(
        y=avg_roas, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"Avg ROAS: {avg_roas:.2f}x"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Business impact summary
st.header("📊 Business Impact Summary")

impact_data = {
    'Metric': [
        'Marketing Investment',
        'Attributed Revenue',
        'Marketing ROI',
        'Revenue Attribution Rate', 
        'Average Daily Marketing Spend',
        'Average Daily Attributed Revenue',
        'Cost per $ of Revenue',
        'Marketing Efficiency Score'
    ],
    'Value': [
        f"${business_metrics['total_marketing_spend']:,.0f}",
        f"${business_metrics['total_attributed_revenue']:,.0f}",
        f"{business_metrics['overall_roas']:.2f}x",
        f"{business_metrics['attribution_rate']:.1f}%",
        f"${business_metrics['avg_daily_spend']:,.0f}",
        f"${business_metrics['avg_daily_revenue']:,.0f}",
        f"${business_metrics['total_marketing_spend']/business_metrics['total_attributed_revenue']:.2f}" if business_metrics['total_attributed_revenue'] > 0 else "$0.00",
        "Excellent" if business_metrics['overall_roas'] > 3 else "Good" if business_metrics['overall_roas'] > 2 else "Needs Improvement"
    ],
    'Insight': [
        "Total marketing investment across all channels",
        "Revenue directly attributed to marketing efforts", 
        "Return generated for every marketing dollar spent",
        "Percentage of total business revenue from marketing",
        "Daily marketing budget allocation",
        "Daily revenue generation from marketing",
        "Marketing cost per revenue dollar generated",
        "Overall marketing performance rating"
    ]
}

import pandas as pd
impact_df = pd.DataFrame(impact_data)
st.dataframe(impact_df, use_container_width=True, hide_index=True)