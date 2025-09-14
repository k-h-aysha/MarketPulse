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

st.set_page_config(page_title="Business Intelligence", page_icon="🧠", layout="wide")

st.title("🧠 Business Intelligence & Strategic Insights")
st.markdown("### Actionable Recommendations for Marketing Excellence")

# Check if data is loaded
if 'processed_data' not in st.session_state or not st.session_state.processed_data:
    st.warning("⚠️ No data loaded. Please run the main dashboard first.")
    st.markdown("👈 Go back to the main page to load your data.")
    st.stop()

processed_data = st.session_state.processed_data
analytics = MarketingAnalytics(processed_data['final_dataset'])

# Generate business intelligence
executive_summary = analytics.generate_executive_summary()
performance_insights = analytics.get_performance_insights()
efficiency_benchmarks = analytics.calculate_efficiency_benchmarks()
budget_opportunities = analytics.calculate_budget_optimization_opportunities()
seasonal_patterns = analytics.calculate_seasonal_patterns()

# Sidebar filters
st.sidebar.header("🎯 Analysis Controls")
analysis_type = st.sidebar.selectbox(
    "Focus Area",
    ["All Insights", "Performance Optimization", "Budget Allocation", "Risk Assessment"]
)

# 1. Executive Summary Dashboard
st.header("📊 Executive Summary")

# Status indicators
col1, col2, col3, col4 = st.columns(4)

with col1:
    status_color = "🟢" if executive_summary['performance_status'] == 'Excellent' else "🟡" if executive_summary['performance_status'] == 'Good' else "🔴"
    st.metric(
        "Overall Performance",
        f"{status_color} {executive_summary['performance_status']}",
        delta=f"{executive_summary['overall_roas']:.2f}x ROAS"
    )

with col2:
    st.metric(
        "Marketing Attribution",
        f"{executive_summary['attribution_rate']:.1f}%",
        delta="of total revenue"
    )

with col3:
    st.metric(
        "Top Performing Channel",
        executive_summary['top_channel'],
        delta="Highest ROAS"
    )

with col4:
    roi_status = "📈 Strong" if executive_summary['overall_roas'] > 3 else "📊 Stable" if executive_summary['overall_roas'] > 2 else "📉 Needs Focus"
    st.metric(
        "ROI Health",
        roi_status,
        delta=f"${executive_summary['total_spend']:,.0f} invested"
    )

st.markdown("---")

# 2. Strategic Insights & Recommendations
st.header("🎯 Strategic Insights & Recommendations")

# Filter insights based on selection
if analysis_type == "Performance Optimization":
    filtered_insights = [i for i in performance_insights if i['type'] in ['Top Performer', 'Conversion Optimization']]
elif analysis_type == "Budget Allocation":
    filtered_insights = [i for i in performance_insights if i['type'] in ['Optimization Opportunity', 'Portfolio Risk']]
elif analysis_type == "Risk Assessment":
    filtered_insights = [i for i in performance_insights if i['type'] in ['Portfolio Risk', 'Attribution Gap']]
else:
    filtered_insights = performance_insights

# Display insights with priority-based styling
for i, insight in enumerate(filtered_insights):
    priority_colors = {"High": "#dc3545", "Medium": "#ffc107", "Low": "#28a745"}
    priority_icons = {"High": "🚨", "Medium": "⚡", "Low": "💡"}
    
    color = priority_colors.get(insight['priority'], "#6c757d")
    icon = priority_icons.get(insight['priority'], "💡")
    
    with st.container():
        st.markdown(f"""
        <div style="
            border-left: 4px solid {color}; 
            padding: 1.5rem; 
            margin: 1rem 0; 
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                <h4 style="color: {color}; margin: 0; font-weight: 600;">
                    {insight['type']} ({insight['priority']} Priority)
                </h4>
            </div>
            <p style="margin: 0.5rem 0; font-size: 1rem;"><strong>📋 Insight:</strong> {insight['insight']}</p>
            <p style="margin: 0.5rem 0; font-size: 1rem;"><strong>🎯 Recommendation:</strong> {insight['recommendation']}</p>
            <p style="margin: 0; font-size: 0.95rem; color: #28a745;"><strong>💰 Potential Impact:</strong> {insight['impact']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# 3. Performance Benchmarking
st.header("📈 Performance Benchmarking")

if efficiency_benchmarks:
    st.subheader("Channel Efficiency Report Card")
    
    # Create benchmarking table
    benchmark_data = []
    for channel, metrics in efficiency_benchmarks.items():
        benchmark_data.append({
            'Channel': channel,
            'Efficiency Score': f"{metrics['efficiency_score']:.0f}/100",
            'Grade': metrics['performance_grade'],
            'ROAS vs Benchmark': f"{metrics['roas_vs_benchmark']:.1f}x",
            'CTR vs Benchmark': f"{metrics['ctr_vs_benchmark']:.1f}x",
            'CPC vs Benchmark': f"{metrics['cpc_vs_benchmark']:.1f}x"
        })
    
    benchmark_df = pd.DataFrame(benchmark_data)
    
    # Color-code the grade column
    def style_grade(grade):
        colors = {'A+': '#28a745', 'A': '#20c997', 'B+': '#17a2b8', 'B': '#ffc107', 'C': '#fd7e14', 'D': '#dc3545'}
        return f'background-color: {colors.get(grade, "#ffffff")}; color: white; font-weight: bold; text-align: center;'
    
    st.dataframe(
        benchmark_df,
        column_config={
            "Channel": "Channel",
            "Efficiency Score": "Overall Score",
            "Grade": st.column_config.TextColumn("Performance Grade"),
            "ROAS vs Benchmark": "ROAS Performance",
            "CTR vs Benchmark": "CTR Performance", 
            "CPC vs Benchmark": "CPC Performance"
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Efficiency visualization
    fig = px.bar(
        benchmark_df,
        x='Channel',
        y='Efficiency Score',
        color='Grade',
        title='Channel Efficiency Scorecard',
        color_discrete_map={'A+': '#28a745', 'A': '#20c997', 'B+': '#17a2b8', 'B': '#ffc107', 'C': '#fd7e14', 'D': '#dc3545'}
    )
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 4. Budget Optimization Matrix
st.header("💰 Budget Optimization Strategy")

if budget_opportunities:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Scale-Up Opportunities")
        if budget_opportunities.get('scale_up'):
            scale_up_df = pd.DataFrame(budget_opportunities['scale_up'])
            for _, row in scale_up_df.iterrows():
                st.success(f"**{row['channel']}** - ROAS: {row['roas']:.2f}x")
                st.write(f"💡 Recommendation: Increase budget by 20-25%")
                st.write(f"💵 Current Spend: ${row['spend']:,.0f}")
                st.write("---")
        else:
            st.info("No immediate scale-up opportunities identified")
    
    with col2:
        st.subheader("🔧 Optimization Needed")
        if budget_opportunities.get('optimize'):
            optimize_df = pd.DataFrame(budget_opportunities['optimize'])
            for _, row in optimize_df.iterrows():
                st.warning(f"**{row['channel']}** - ROAS: {row['roas']:.2f}x")
                st.write(f"🎯 Recommendation: Optimize campaigns or reduce spend by 15%")
                st.write(f"💵 Current Spend: ${row['spend']:,.0f}")
                st.write("---")
        else:
            st.success("All channels performing above optimization threshold")
    
    # Budget reallocation opportunity
    if budget_opportunities.get('reallocation'):
        st.subheader("💡 Smart Budget Reallocation")
        realloc = budget_opportunities['reallocation']
        
        st.info(f"""
        **Opportunity Identified:**
        Move ${realloc['amount']:,.0f} from {realloc['from_channel']} to {realloc['to_channel']}
        
        **Projected Impact:**
        - Net Revenue Gain: ${realloc['projected_net_gain']:,.0f}
        - ROI Improvement: {realloc['roi_improvement']:.1%}
        """)

st.markdown("---")

# 5. Seasonal Performance Patterns
st.header("📅 Seasonal Performance Intelligence")

if seasonal_patterns:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Day-of-Week Performance")
        
        best_day = seasonal_patterns['best_day']
        worst_day = seasonal_patterns['worst_day']
        
        st.success(f"🏆 **Best Day:** {best_day['day']}")
        st.write(f"• Average ROAS: {best_day['avg_roas']:.2f}x")
        st.write(f"• Average Spend: ${best_day['avg_spend']:,.0f}")
        
        st.error(f"📉 **Weakest Day:** {worst_day['day']}")
        st.write(f"• Average ROAS: {worst_day['avg_roas']:.2f}x")
        st.write(f"• Average Spend: ${worst_day['avg_spend']:,.0f}")
        
    with col2:
        st.subheader("💡 Scheduling Recommendations")
        
        performance_gap = best_day['avg_roas'] - worst_day['avg_roas']
        
        if performance_gap > 0.5:
            st.write("**Optimization Opportunities:**")
            st.write(f"• Increase bids on {best_day['day']}s (+15-20%)")
            st.write(f"• Reduce bids on {worst_day['day']}s (-10-15%)")
            st.write(f"• Schedule premium creative for {best_day['day']}s")
            st.write(f"• Focus on testing/optimization on {worst_day['day']}s")
        else:
            st.write("✅ Performance is relatively consistent across days")
            st.write("Focus on overall campaign optimization rather than day-parting")
    
    # Day of week visualization
    dow_data = seasonal_patterns['dow_performance']
    fig = px.bar(
        dow_data,
        x='day_of_week',
        y='roas',
        title='ROAS Performance by Day of Week',
        color='roas',
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 6. Action Plan Summary
st.header("📋 30-Day Action Plan")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Week 1-2: Quick Wins")
    week1_actions = []
    
    # Add actions based on insights
    high_priority_insights = [i for i in performance_insights if i['priority'] == 'High']
    for insight in high_priority_insights[:2]:
        week1_actions.append(f"• {insight['recommendation']}")
    
    if budget_opportunities.get('scale_up'):
        top_performer = budget_opportunities['scale_up'][0]
        week1_actions.append(f"• Increase {top_performer['channel']} budget by 15%")
    
    if seasonal_patterns and seasonal_patterns.get('best_day'):
        best_day = seasonal_patterns['best_day']['day']
        week1_actions.append(f"• Optimize bid scheduling for {best_day}s")
    
    for action in week1_actions[:4]:
        st.write(action)

with col2:
    st.subheader("🚀 Week 3-4: Strategic Changes")
    week3_actions = []
    
    # Add strategic actions
    medium_priority_insights = [i for i in performance_insights if i['priority'] == 'Medium']
    for insight in medium_priority_insights[:2]:
        week3_actions.append(f"• {insight['recommendation']}")
    
    if budget_opportunities.get('reallocation'):
        week3_actions.append("• Implement budget reallocation strategy")
    
    week3_actions.append("• Conduct A/B tests on underperforming channels")
    week3_actions.append("• Review and optimize attribution settings")
    
    for action in week3_actions[:4]:
        st.write(action)

# Expected impact summary
st.subheader("📈 Expected Impact Summary")
if performance_insights:
    total_potential_impact = 0
    impact_summary = []
    
    for insight in performance_insights:
        impact_text = insight.get('impact', '')
        # Extract dollar amounts from impact text
        import re
        dollar_amounts = re.findall(r'\$[\d,]+', impact_text)
        if dollar_amounts:
            # Convert first dollar amount to number
            amount_str = dollar_amounts[0].replace('$', '').replace(',', '')
            try:
                amount = float(amount_str)
                total_potential_impact += amount
                impact_summary.append(f"• {insight['type']}: {dollar_amounts[0]}")
            except:
                pass
    
    if total_potential_impact > 0:
        st.success(f"**Total Potential Revenue Impact: ${total_potential_impact:,.0f}**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Conservative Estimate", f"${total_potential_impact * 0.6:,.0f}")
        with col2:
            st.metric("Expected Outcome", f"${total_potential_impact:,.0f}")
        with col3:
            st.metric("Optimistic Scenario", f"${total_potential_impact * 1.3:,.0f}")

st.markdown("---")
st.markdown("*Business Intelligence powered by data-driven insights | Updated daily*")