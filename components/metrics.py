import streamlit as st
from typing import Dict, Any

class MetricsDisplay:
    """Handles all metric card displays"""
    
    @staticmethod
    def show_kpi_cards(metrics: Dict[str, Any]):
        """Display main KPI cards"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total ROAS",
                f"{metrics.get('overall_roas', 0):.2f}x",
                delta=f"${metrics.get('total_marketing_spend', 0):,.0f} spent"
            )
        
        with col2:
            st.metric(
                "Attributed Revenue",
                f"${metrics.get('total_attributed_revenue', 0):,.0f}",
                delta=f"{metrics.get('attribution_rate', 0):.1f}% of total"
            )
        
        with col3:
            st.metric(
                "Avg Daily Spend",
                f"${metrics.get('avg_daily_spend', 0):,.0f}",
                delta=f"{metrics.get('data_period_days', 0)} days"
            )
        
        with col4:
            st.metric(
                "Avg Daily Revenue",
                f"${metrics.get('avg_daily_revenue', 0):,.0f}",
                delta="Marketing driven"
            )
    
    @staticmethod
    def show_channel_cards(channel_data):
        """Display channel performance cards"""
        st.subheader("📊 Channel Performance")
        
        cols = st.columns(len(channel_data))
        
        for idx, (_, row) in enumerate(channel_data.iterrows()):
            with cols[idx]:
                st.metric(
                    f"{row['channel']}",
                    f"{row['roas']:.2f}x ROAS",
                    delta=f"{row['ctr']:.2f}% CTR"
                )
    
    @staticmethod
    def show_processing_status(processing_result):
        """Display data processing status"""
        if processing_result and processing_result['success']:
            st.success("🎉 Data Processing Complete!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                date_parts = processing_result['date_range'].split(' to ')
                st.metric("Start Date", date_parts[0])
            
            with col2:
                st.metric("End Date", date_parts[1])
            
            with col3:
                st.metric("Total Days", processing_result['total_days'])
        else:
            st.error("❌ Data processing failed")