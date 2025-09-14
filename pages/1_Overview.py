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

st.set_page_config(page_title="Executive Overview", page_icon="📊", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
}

.insight-box {
    background: #f8f9fa;
    border-left: 4px solid #28a745;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}

.warning-box {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Executive Dashboard Overview")
st.markdown("### Strategic Performance Summary & Key Business Insights")

# Check if data is loaded
if 'processed_data' not in st.session_state or not st.session_state.processed_data:
    st.warning("⚠️ No data loaded. Please run the main dashboard first.")
    st.markdown("👈 Go back to the main page to load your data.")
    st.stop()

processed_data = st.session_state.processed_data
analytics = MarketingAnalytics(processed_data['final_dataset'])

# Calculate key metrics
business_metrics = analytics.calculate_business_impact()
channel_performance = analytics.calculate_channel_performance()
daily_trends = analytics.calculate_daily_trends()
performance_insights = analytics.get_performance_insights()
executive_summary = analytics.generate_executive_summary()

# 1. Executive Summary Header
st.header("🎯 Executive Summary")

# Performance status banner
status = executive_summary['performance_status']
status_colors = {
    'Excellent': '#28a745',
    'Good': '#17a2b8', 
    'Needs Improvement': '#dc3545'
}

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {status_colors.get(status, '#6c757d')} 0%, {status_colors.get(status, '#6c757d')}dd 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
">
    <h2 style="margin: 0; font-size: 2rem;">Marketing Performance: {status}</h2>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
        Overall ROAS: {executive_summary['overall_roas']:.2f}x | 
        Attribution: {executive_summary['attribution_rate']:.1f}% | 
        Top Channel: {executive_summary['top_channel']}
    </p>
</div>
""", unsafe_allow_html=True)

# 2. Key Performance Indicators
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    roas_trend = "↗️" if business_metrics['overall_roas'] > 3 else "→" if business_metrics['overall_roas'] > 2 else "↘️"
    st.metric(
        f"{roas_trend} Marketing ROI",
        f"{business_metrics['overall_roas']:.2f}x",
        delta=f"${business_metrics['total_marketing_spend']:,.0f} invested",
        help="Return on advertising spend - industry benchmark: 3.0x"
    )

with col2:
    attr_trend = "🎯" if business_metrics['attribution_rate'] > 20 else "📊"
    st.metric(
        f"{attr_trend} Attribution Rate",
        f"{business_metrics['attribution_rate']:.1f}%",
        delta=f"${business_metrics['total_attributed_revenue']:,.0f} attributed",
        help="Percentage of total revenue attributed to marketing"
    )

with col3:
    total_revenue = business_metrics['total_business_revenue']
    revenue_trend = "💰" if total_revenue > 5000000 else "💵"
    st.metric(
        f"{revenue_trend} Total Revenue",
        f"${total_revenue:,.0f}",
        delta=f"{business_metrics['data_period_days']} days",
        help="Total business revenue across all sources"
    )

with col4:
    efficiency = business_metrics['total_attributed_revenue'] / business_metrics['total_marketing_spend'] if business_metrics['total_marketing_spend'] > 0 else 0
    eff_trend = "🚀" if efficiency > 4 else "📈" if efficiency > 2.5 else "⚠️"
    st.metric(
        f"{eff_trend} Marketing Efficiency", 
        f"${efficiency:.2f}",
        delta="Revenue per $ spent",
        help="Revenue generated per marketing dollar invested"
    )

st.markdown("---")

# 3. Performance Insights & Alerts
st.header("💡 Strategic Insights")

# Display top insights with enhanced styling
if performance_insights:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Key Performance Insights")
        
        for i, insight in enumerate(performance_insights[:3]):
            priority_colors = {"High": "#dc3545", "Medium": "#ffc107", "Low": "#28a745"}
            color = priority_colors.get(insight['priority'], "#6c757d")
            
            st.markdown(f"""
            <div style="
                border-left: 4px solid {color};
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                padding: 1.5rem;
                margin: 1rem 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            ">
                <h4 style="color: {color}; margin: 0 0 0.5rem 0;">
                    {insight['type']} ({insight['priority']} Priority)
                </h4>
                <p style="margin: 0.5rem 0; color: #495057;"><strong>Insight:</strong> {insight['insight']}</p>
                <p style="margin: 0.5rem 0; color: #28a745;"><strong>Impact:</strong> {insight['impact']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Quick Actions")
        
        # Action items from insights
        for insight in performance_insights[:3]:
            if insight['priority'] == 'High':
                st.error(f"🚨 {insight['recommendation'][:50]}...")
            elif insight['priority'] == 'Medium':
                st.warning(f"⚡ {insight['recommendation'][:50]}...")
            else:
                st.info(f"💡 {insight['recommendation'][:50]}...")

st.markdown("---")

# 4. Channel Performance Overview
st.header("🎯 Channel Performance Matrix")

if not channel_performance.empty:
    # Performance grades
    def get_performance_grade(roas):
        if roas >= 4: return "A+", "#28a745"
        elif roas >= 3: return "A", "#20c997" 
        elif roas >= 2: return "B", "#ffc107"
        elif roas >= 1: return "C", "#fd7e14"
        else: return "D", "#dc3545"
    
    # Channel cards with grades
    cols = st.columns(len(channel_performance))
    
    for idx, (_, row) in enumerate(channel_performance.iterrows()):
        grade, color = get_performance_grade(row['roas'])
        
        with cols[idx]:
            spend_pct = (row['spend'] / channel_performance['spend'].sum()) * 100
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #ffffff 0%, #f1f3f4 100%);
                border: 2px solid {color};
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                margin: 0.5rem 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            ">
                <h3 style="margin: 0 0 0.5rem 0; color: #495057;">{row['channel']}</h3>
                <div style="font-size: 2rem; font-weight: bold; color: {color}; margin: 0.5rem 0;">
                    {row['roas']:.2f}x ROAS
                </div>
                <div style="
                    background: {color};
                    color: white;
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-weight: bold;
                    margin: 0.5rem 0;
                ">
                    Grade: {grade}
                </div>
                <div style="color: #6c757d; font-size: 0.9rem;">
                    CTR: {row['ctr']*100:.2f}% | ${row['spend']:,.0f} ({spend_pct:.0f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)

# Channel performance table with insights
st.subheader("📊 Detailed Performance Analysis")

# Add performance insights to the table
channel_performance_enhanced = channel_performance.copy()
channel_performance_enhanced['grade'] = channel_performance_enhanced['roas'].apply(lambda x: get_performance_grade(x)[0])
channel_performance_enhanced['spend_share'] = (channel_performance_enhanced['spend'] / channel_performance_enhanced['spend'].sum() * 100).round(1)

st.dataframe(
    channel_performance_enhanced,
    column_config={
        "channel": st.column_config.TextColumn("Channel"),
        "spend": st.column_config.NumberColumn("Spend ($)", format="$%.0f"),
        "revenue": st.column_config.NumberColumn("Revenue ($)", format="$%.0f"),
        "roas": st.column_config.NumberColumn("ROAS", format="%.2fx"),
        "grade": st.column_config.TextColumn("Performance Grade"),
        "ctr": st.column_config.NumberColumn("CTR (%)", format="%.3f%%"),
        "cpc": st.column_config.NumberColumn("CPC ($)", format="$%.2f"),
        "spend_share": st.column_config.NumberColumn("Budget Share (%)", format="%.1f%%")
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# 5. Visual Performance Analysis
st.header("📈 Performance Visualization")

tab1, tab2, tab3 = st.tabs(["🎯 ROI Analysis", "📊 Channel Mix", "📈 Efficiency Matrix"])

with tab1:
    # ROI waterfall or comparison
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue attribution breakdown
        attributed = business_metrics['total_attributed_revenue']
        non_attributed = business_metrics['total_business_revenue'] - attributed
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Marketing Attributed', 'Other Sources'],
            values=[attributed, non_attributed],
            hole=0.4,
            marker_colors=['#1f77b4', '#ff7f0e'],
            textinfo='label+percent',
            textfont_size=12
        )])
        
        fig_pie.update_layout(
            title="Revenue Attribution Breakdown",
            annotations=[dict(
                text=f"Marketing<br>{business_metrics['attribution_rate']:.1f}%<br>of Total", 
                x=0.5, y=0.5, font_size=14, showarrow=False
            )]
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # ROI by channel
        fig_bar = px.bar(
            channel_performance,
            x='channel',
            y='roas',
            title='ROAS Performance by Channel',
            color='roas',
            color_continuous_scale='RdYlGn',
            text='roas'
        )
        
        fig_bar.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
        fig_bar.add_hline(y=3.0, line_dash="dash", line_color="red", 
                         annotation_text="Industry Benchmark: 3.0x")
        fig_bar.update_layout(showlegend=False)
        
        st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    # Channel mix analysis
    fig_treemap = px.treemap(
        channel_performance,
        path=['channel'],
        values='spend',
        color='roas',
        color_continuous_scale='RdYlGn',
        title='Marketing Spend Distribution & ROAS Performance'
    )
    
    st.plotly_chart(fig_treemap, use_container_width=True)
    
    # Channel mix insights
    top_spender = channel_performance.iloc[0]
    spend_concentration = (top_spender['spend'] / channel_performance['spend'].sum()) * 100
    
    if spend_concentration > 60:
        st.warning(f"⚠️ **Portfolio Risk**: {spend_concentration:.0f}% of spend concentrated in {top_spender['channel']}")
    elif spend_concentration < 40:
        st.success("✅ **Balanced Portfolio**: Well-diversified marketing spend across channels")
    else:
        st.info(f"📊 **Moderate Concentration**: {spend_concentration:.0f}% spend in {top_spender['channel']}")

with tab3:
    # Efficiency scatter plot
    fig_scatter = px.scatter(
        channel_performance,
        x='cpc',
        y='roas',
        size='spend',
        color='channel',
        title='Marketing Efficiency Matrix: Cost vs Performance',
        labels={'cpc': 'Cost Per Click ($)', 'roas': 'Return on Ad Spend'},
        hover_data=['ctr', 'spend', 'revenue']
    )
    
    # Add benchmark lines
    fig_scatter.add_hline(y=3.0, line_dash="dash", line_color="green", opacity=0.5,
                         annotation_text="Good ROAS: 3.0x")
    fig_scatter.add_vline(x=2.0, line_dash="dash", line_color="orange", opacity=0.5,
                         annotation_text="Target CPC: $2.00")
    
    # Add quadrant labels
    fig_scatter.add_annotation(x=1.0, y=4.5, text="High Efficiency<br>(Low Cost, High ROAS)", 
                              bgcolor="lightgreen", opacity=0.7)
    fig_scatter.add_annotation(x=3.0, y=1.5, text="Low Efficiency<br>(High Cost, Low ROAS)", 
                              bgcolor="lightcoral", opacity=0.7)
    
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# 6. Executive Recommendations
st.header("📋 Executive Recommendations")

recommendations = []

# Generate recommendations based on performance
if not channel_performance.empty:
    top_performer = channel_performance.iloc[0]
    bottom_performer = channel_performance.iloc[-1]
    
    # Top performer scaling
    if top_performer['roas'] > 3.0:
        recommendations.append({
            'priority': 'High',
            'action': f"Scale {top_performer['channel']} budget by 20-25%",
            'rationale': f"Delivering {top_performer['roas']:.2f}x ROAS above industry benchmark",
            'impact': 'Revenue Growth'
        })
    
    # Bottom performer optimization
    if bottom_performer['roas'] < 2.0:
        recommendations.append({
            'priority': 'High', 
            'action': f"Optimize or reduce {bottom_performer['channel']} spend by 15%",
            'rationale': f"ROAS of {bottom_performer['roas']:.2f}x below acceptable threshold",
            'impact': 'Cost Savings'
        })

# Attribution recommendations
if business_metrics['attribution_rate'] < 15:
    recommendations.append({
        'priority': 'Medium',
        'action': 'Improve attribution tracking and measurement',
        'rationale': f"Only {business_metrics['attribution_rate']:.1f}% attribution suggests measurement gaps",
        'impact': 'Better Decision Making'
    })

# Portfolio diversification
spend_concentration = (channel_performance.iloc[0]['spend'] / channel_performance['spend'].sum()) * 100
if spend_concentration > 70:
    recommendations.append({
        'priority': 'Medium',
        'action': 'Diversify marketing mix to reduce platform risk',
        'rationale': f"{spend_concentration:.0f}% concentration creates platform dependency",
        'impact': 'Risk Mitigation'
    })

# Display recommendations
if recommendations:
    for i, rec in enumerate(recommendations[:4], 1):
        priority_colors = {'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#28a745'}
        color = priority_colors.get(rec['priority'], '#6c757d')
        
        st.markdown(f"""
        <div style="
            border: 1px solid {color};
            border-left: 4px solid {color};
            background: #ffffff;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        ">
            <strong style="color: {color};">#{i} {rec['priority']} Priority:</strong> {rec['action']}<br>
            <small style="color: #6c757d;">
                <strong>Why:</strong> {rec['rationale']}<br>
                <strong>Expected Impact:</strong> {rec['impact']}
            </small>
        </div>
        """, unsafe_allow_html=True)

# 7. Performance Summary
st.header("📊 Performance Summary")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 Strengths")
    strengths = []
    
    if business_metrics['overall_roas'] > 3:
        strengths.append("Strong overall ROAS performance")
    
    if not channel_performance.empty:
        high_performers = channel_performance[channel_performance['roas'] > 3]
        if len(high_performers) > 0:
            strengths.append(f"{len(high_performers)} channels exceeding 3.0x ROAS")
    
    if business_metrics['attribution_rate'] > 15:
        strengths.append("Good marketing attribution coverage")
    
    if not strengths:
        strengths.append("Stable marketing performance")
    
    for strength in strengths:
        st.success(f"✅ {strength}")

with col2:
    st.subheader("🔴 Areas for Improvement")
    improvements = []
    
    if business_metrics['overall_roas'] < 2.5:
        improvements.append("Overall ROAS below optimal threshold")
    
    if not channel_performance.empty:
        low_performers = channel_performance[channel_performance['roas'] < 2]
        if len(low_performers) > 0:
            improvements.append(f"{len(low_performers)} channels need optimization")
    
    if business_metrics['attribution_rate'] < 10:
        improvements.append("Low attribution rate suggests measurement gaps")
    
    if not improvements:
        improvements.append("Consider testing new growth opportunities")
    
    for improvement in improvements:
        st.error(f"⚠️ {improvement}")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <em>Executive Overview | Updated with latest performance data</em><br>
    <small>For detailed analysis, navigate to Channel Analysis and Business Impact pages</small>
</div>
""", unsafe_allow_html=True)