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
                "channel": "Channel",
                "spend": st.column_config.NumberColumn("Spend", format="$%.0f"),
                "revenue": st.column_config.NumberColumn("Revenue", format="$%.0f"),
                "roas": st.column_config.NumberColumn("ROAS", format="%.2fx"),
                "impressions": st.column_config.NumberColumn("Impressions", format="%.0f"),
                "clicks": st.column_config.NumberColumn("Clicks", format="%.0f"),
                "ctr": st.column_config.NumberColumn("CTR", format="%.2f%%"),
                "orders": st.column_config.NumberColumn("Orders", format="%.0f"),
                "new_orders": st.column_config.NumberColumn("New Orders", format="%.0f"),
                "new_customers": st.column_config.NumberColumn("New Customers", format="%.0f"),
                "total_revenue": st.column_config.NumberColumn("Total Revenue", format="$%.0f"),
                "gross_profit": st.column_config.NumberColumn("Gross Profit", format="$%.0f")
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
    
    @staticmethod
    def business_data_table(final_dataset, max_rows=30):
        """Display business performance data"""
        st.subheader("🏢 Business Performance Data")
        
        # Filter for Total channel only to avoid duplicates
        business_data = final_dataset[final_dataset['channel'] == 'Total'].copy()
        business_data = business_data.sort_values('date', ascending=False).head(max_rows)
        
        # Select relevant business columns
        display_cols = ['date', 'orders', 'new_orders', 'new_customers', 'total_revenue', 'gross_profit', 'cogs']
        display_data = business_data[display_cols]
        
        st.dataframe(
            display_data,
            column_config={
                "date": st.column_config.DateColumn("Date"),
                "orders": st.column_config.NumberColumn("Total Orders", format="%.0f"),
                "new_orders": st.column_config.NumberColumn("New Orders", format="%.0f"),
                "new_customers": st.column_config.NumberColumn("New Customers", format="%.0f"),
                "total_revenue": st.column_config.NumberColumn("Total Revenue", format="$%.0f"),
                "gross_profit": st.column_config.NumberColumn("Gross Profit", format="$%.0f"),
                "cogs": st.column_config.NumberColumn("COGS", format="$%.0f")
            },
            use_container_width=True,
            hide_index=True
        )
        
        if len(business_data) > max_rows:
            st.info(f"Showing latest {max_rows} days. Total days available: {len(business_data)}")
    
    @staticmethod
    def raw_data_preview(raw_data, title="Raw Data Preview", max_rows=20):
        """Display raw data preview"""
        st.subheader(f"🔍 {title}")
        
        # Show sample of raw data
        display_data = raw_data.head(max_rows)
        
        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )
        
        # Show data info
        st.info(f"""
        **Data Summary:**
        - Total Rows: {len(raw_data):,}
        - Columns: {len(raw_data.columns)}
        - Date Range: {raw_data['date'].min().date() if 'date' in raw_data.columns else 'N/A'} to {raw_data['date'].max().date() if 'date' in raw_data.columns else 'N/A'}
        """)