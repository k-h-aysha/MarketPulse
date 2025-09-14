import streamlit as st
import pandas as pd

class TablesDisplay:
    """Handles all data table displays"""
    
    @staticmethod
    def channel_performance_table(channel_data):
        """Display channel performance table"""
        st.subheader("📊 Detailed Channel Performance")
        
        # Format the data for better display
        display_data = channel_data.copy()
        
        st.dataframe(
            display_data,
            column_config={
                "channel": "Channel",
                "spend": st.column_config.NumberColumn(
                    "Spend",
                    format="$%.0f"
                ),
                "revenue": st.column_config.NumberColumn(
                    "Revenue",
                    format="$%.0f"
                ),
                "impressions": st.column_config.NumberColumn(
                    "Impressions",
                    format="%.0f"
                ),
                "clicks": st.column_config.NumberColumn(
                    "Clicks",
                    format="%.0f"
                ),
                "roas": st.column_config.NumberColumn(
                    "ROAS",
                    format="%.2fx"
                ),
                "ctr": st.column_config.NumberColumn(
                    "CTR",
                    format="%.2f%%"
                ),
                "cpc": st.column_config.NumberColumn(
                    "CPC",
                    format="$%.2f"
                ),
                "cpm": st.column_config.NumberColumn(
                    "CPM",
                    format="$%.2f"
                )
            },
            use_container_width=True,
            hide_index=True
        )
    
    @staticmethod
    def daily_data_table(daily_data, max_rows=50):
        """Display daily data table"""
        st.subheader("📅 Daily Performance Data")
        
        # Show recent data first
        display_data = daily_data.sort_values('date', ascending=False).head(max_rows)
        
        st.dataframe(
            display_data,
            column_config={
                "date": st.column_config.DateColumn("Date"),
                "spend": st.column_config.NumberColumn("Spend", format="$%.0f"),
                "revenue": st.column_config.NumberColumn("Revenue", format="$%.0f"),
                "roas": st.column_config.NumberColumn("ROAS", format="%.2fx"),
                "impressions": st.column_config.NumberColumn("Impressions", format="%.0f"),
                "clicks": st.column_config.NumberColumn("Clicks", format="%.0f"),
                "ctr": st.column_config.NumberColumn("CTR", format="%.2f%%")
            },
            use_container_width=True,
            hide_index=True
        )
        
        if len(daily_data) > max_rows:
            st.info(f"Showing latest {max_rows} days. Total days available: {len(daily_data)}")
    
    @staticmethod
    def business_metrics_table(business_metrics):
        """Display business metrics summary table"""
        st.subheader("💼 Business Impact Summary")
        
        metrics_data = {
            'Metric': [
                'Total Marketing Spend',
                'Total Attributed Revenue',
                'Total Business Revenue', 
                'Attribution Rate',
                'Overall ROAS',
                'Average Daily Spend',
                'Average Daily Revenue',
                'Data Period (Days)'
            ],
            'Value': [
                f"${business_metrics['total_marketing_spend']:,.0f}",
                f"${business_metrics['total_attributed_revenue']:,.0f}",
                f"${business_metrics['total_business_revenue']:,.0f}",
                f"{business_metrics['attribution_rate']:.1f}%",
                f"{business_metrics['overall_roas']:.2f}x",
                f"${business_metrics['avg_daily_spend']:,.0f}",
                f"${business_metrics['avg_daily_revenue']:,.0f}",
                f"{business_metrics['data_period_days']} days"
            ]
        }
        
        st.dataframe(
            pd.DataFrame(metrics_data),
            column_config={
                "Metric": "Business Metric",
                "Value": "Value"
            },
            use_container_width=True,
            hide_index=True
        )