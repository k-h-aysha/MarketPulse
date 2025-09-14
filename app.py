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

# Custom CSS for enhanced UI
st.markdown("""
<style>
/* Force sidebar to be visible and expanded */
section[data-testid="stSidebar"] {
    background: #f8f9fa !important;
    border-right: 1px solid #e0e0e0 !important;
    width: 280px !important;
    min-width: 280px !important;
    max-width: 280px !important;
    position: relative !important;
    transform: none !important;
    transition: none !important;
}

section[data-testid="stSidebar"] > div {
    background: #f8f9fa !important;
    width: 280px !important;
    min-width: 280px !important;
    max-width: 280px !important;
}

/* Hide ALL default Streamlit navigation elements */
section[data-testid="stSidebar"] .css-1d391kg,
section[data-testid="stSidebar"] .css-1lcbmhc,
section[data-testid="stSidebar"] .css-1y4p8pa,
section[data-testid="stSidebar"] .css-12oz5g7,
section[data-testid="stSidebar"] nav,
section[data-testid="stSidebar"] ul,
section[data-testid="stSidebar"] li[role="tab"],
section[data-testid="stSidebar"] button[role="tab"],
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .css-2trqyj,
section[data-testid="stSidebar"] .css-1n76uvr,
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
}

/* Sidebar logo styling */
.sidebar-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem 0;
    margin-bottom: 1rem;
    border-bottom: 1px solid #e0e0e0;
    background: #f8f9fa;
}

.sidebar-logo svg {
    max-width: 120px;
    height: auto;
    display: block !important;
}

/* Navigation items styling */
.nav-item {
    margin: 0.5rem 0;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    background: white;
    transition: all 0.3s ease;
    cursor: pointer;
    color: #000000 !important;
    font-weight: 500;
    display: block !important;
    visibility: visible !important;
}

.nav-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-color: #1f77b4;
    background: #f8f9fa;
}

.nav-item.active {
    background: #1f77b4 !important;
    color: white !important;
    border-color: #1f77b4;
    box-shadow: 0 4px 12px rgba(31,119,180,0.3);
}

.nav-item.active strong {
    color: white !important;
}

.nav-item.active small {
    color: rgba(255,255,255,0.8) !important;
}

.nav-item strong {
    color: #000000 !important;
    font-size: 1rem;
}

.nav-item small {
    color: #666666 !important;
    font-size: 0.85rem;
}

/* Main content adjustment */
.main .block-container {
    padding-top: 5rem;
    margin-left: 0;
}

/* Ensure sidebar toggle button works */
.css-1rs6os {
    display: block !important;
}

/* Make sure sidebar content is visible */
.css-1d391kg {
    padding-top: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

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
    
    # Initialize session state for page navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    
    # Mobile navigation will be handled by JavaScript
    
    # Sidebar with logo and navigation (hidden on mobile)
    with st.sidebar:
        # Custom CSS for sidebar styling and header removal
        st.markdown("""
        <style>
        /* Hide the sidebar header completely */
        [data-testid="stSidebarHeader"] {
            display: none !important;
        }
        
        /* Hide sidebar close button and collapse elements on desktop */
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCloseButton"],
        .css-1544g2n,
        .st-emotion-cache-1544g2n {
            display: none !important;
        }
        
        /* Mobile responsive sidebar */
        @media (max-width: 768px) {
            /* Allow sidebar to close properly on mobile */
            [data-testid="stSidebarCollapseButton"],
            [data-testid="stSidebarCloseButton"] {
                display: block !important;
            }
        }
        
        /* Mobile navigation styles */
        .mobile-nav-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            background: white;
            z-index: 1001;
            flex-direction: column;
        }
        
        .mobile-nav-overlay.show {
            display: flex;
        }
        
        .mobile-nav-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background: #3366FF;
            color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .mobile-nav-logo {
            font-size: 1.3rem;
            font-weight: bold;
            display: flex;
            align-items: center;
        }
        
        .mobile-nav-close {
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 8px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        
        .mobile-nav-close:hover {
            background: rgba(255,255,255,0.1);
        }
        
        .mobile-nav-menu {
            flex: 1;
            padding: 0;
            background: white;
        }
        
        .mobile-nav-item {
            display: block;
            width: 100%;
            padding: 1.2rem 1.5rem;
            border: none;
            background: white;
            text-align: left;
            font-size: 1.1rem;
            border-bottom: 1px solid #e8e8e8;
            cursor: pointer;
            transition: all 0.2s;
            color: #333;
        }
        
        .mobile-nav-item:hover {
            background: #f8f9fa;
            color: #3366FF;
        }
        
        .mobile-nav-item.active {
            background: #3366FF;
            color: white;
            font-weight: 600;
        }
        
        .mobile-nav-item:first-child {
            border-top: 1px solid #e8e8e8;
        }
        
        /* Adjust main content padding on mobile */
        @media (max-width: 768px) {
            .main .block-container {
                padding-top: 80px !important;
            }
        }
        
        /* Remove top padding from sidebar content */
        .css-1d391kg, .st-emotion-cache-1d391kg {
            padding-top: 0.5rem !important;
        }
        
        /* Reduce main content top padding */
        .main .block-container {
            padding-top: 1rem !important;
        }
        
        /* Logo styling at absolute top */
        .sidebar-logo {
            text-align: center;
            padding: 1.5rem 0;
            border-bottom: 1px solid #e0e0e0;
            margin-bottom: 1rem;
            margin-top: 0 !important;
            position: relative;
            top: 0;
        }
        .sidebar-logo svg {
            max-width: 100%;
            height: auto;
        }
        
        /* Ensure sidebar content starts from top */
        .css-1cypcdb, .st-emotion-cache-1cypcdb {
            padding-top: 0 !important;
        }
        
        /* Enhanced button styling with hover and active states */
        .stButton > button {
            width: 100%;
            border-radius: 8px !important;
            border: 1px solid #d0d0d0 !important;
            transition: all 0.3s ease !important;
            font-weight: 500 !important;
            padding: 0.75rem 1rem !important;
            background-color: #f8f9fa !important;
        }
        
        /* Home button selected state - using key attribute */
        .stButton button[data-testid="baseButton-secondary"]:has-text("🏠 Home") {
            background-color: #3366FF !important;
            color: white !important;
            border-color: #3366FF !important;
        }
        
        /* Selected button styling - only for active page */
        button.page-selected {
            background-color: #3366FF !important;
            color: white !important;
            border-color: #3366FF !important;
        }
        
        /* Override hover for selected button */
        button.page-selected:hover {
            background-color: #2952CC !important;
            color: white !important;
        }
        
        /* Hover animation */
        .stButton > button:hover {
            background-color: #e3f2fd !important;
            border-color: #3366FF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(51, 102, 255, 0.2) !important;
        }
        
        /* Active/Selected button styling */
        .stButton > button:focus {
            background-color: #3366FF !important;
            color: white !important;
            border-color: #3366FF !important;
            box-shadow: 0 0 0 2px rgba(51, 102, 255, 0.3) !important;
        }
        
        /* Button press animation */
        .stButton > button:active {
            transform: translateY(0px) !important;
        }
        
        /* Reduce heading sizes */
        h1 {
            font-size: 2rem !important;
        }
        h2 {
            font-size: 1.5rem !important;
        }
        h3 {
            font-size: 1.25rem !important;
        }
        
        /* Scroll to top on page load */
        html {
            scroll-behavior: smooth;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Hide default Streamlit elements
        st.markdown("""
        <script>
        setTimeout(() => {
            const nav = document.querySelector('[data-testid="stSidebarNav"]');
            if (nav) nav.remove();
            const selectboxes = document.querySelectorAll('.stSelectbox');
            selectboxes.forEach(box => box.remove());
            
            // Hide sidebar header and close button
            const sidebarHeader = document.querySelector('[data-testid="stSidebarHeader"]');
            if (sidebarHeader) sidebarHeader.style.display = 'none';
            
            // Hide all sidebar close/collapse elements
            const collapseButton = document.querySelector('[data-testid="stSidebarCollapseButton"]');
            if (collapseButton) collapseButton.style.display = 'none';
            
            const closeButton = document.querySelector('[data-testid="stSidebarCloseButton"]');
            if (closeButton) closeButton.style.display = 'none';
            
            // Hide any collapse icons
            const collapseIcons = document.querySelectorAll('.css-1544g2n, .st-emotion-cache-1544g2n');
            collapseIcons.forEach(icon => icon.style.display = 'none');
            
            // Remove top padding from sidebar
            const sidebarContent = document.querySelector('[data-testid="stSidebar"] > div');
            if (sidebarContent) sidebarContent.style.paddingTop = '0.5rem';
            
            // Enhanced scroll to top functionality
            window.scrollTo({top: 0, left: 0, behavior: 'instant'});
            document.documentElement.scrollTop = 0;
            document.body.scrollTop = 0;
            
            // Enhanced button selection management
            setTimeout(() => {
                // Clear all previous selections
                const allButtons = document.querySelectorAll('[data-testid="stSidebar"] button');
                allButtons.forEach(btn => {
                    btn.classList.remove('page-selected');
                    btn.style.removeProperty('background-color');
                    btn.style.removeProperty('color');
                    btn.style.removeProperty('border-color');
                });
                
                // Set current page button as selected
                const currentPage = sessionStorage.getItem('currentPage') || 'Home';
                const buttons = document.querySelectorAll('[data-testid="stSidebar"] button');
                buttons.forEach(btn => {
                    const btnText = btn.textContent.trim();
                    if ((currentPage === 'Home' && btnText.includes('🏠 Home')) ||
                        (currentPage === 'Overview' && btnText.includes('📊 Overview')) ||
                        (currentPage === 'Channel Analysis' && btnText.includes('📺 Channel Analysis')) ||
                        (currentPage === 'Business Impact' && btnText.includes('💼 Business Impact')) ||
                        (currentPage === 'Business Intelligence' && btnText.includes('🧠 Business Intelligence'))) {
                        btn.classList.add('page-selected');
                        btn.style.setProperty('background-color', '#3366FF', 'important');
                        btn.style.setProperty('color', 'white', 'important');
                        btn.style.setProperty('border-color', '#3366FF', 'important');
                    }
                });
                
                // Enhanced mobile sidebar functionality
                function setupMobileSidebar() {
                    if (window.innerWidth <= 768) {
                        // Force close button to be visible and functional
                        const closeBtn = document.querySelector('[data-testid="stSidebarCloseButton"]');
                        if (closeBtn) {
                            closeBtn.style.display = 'block !important';
                            closeBtn.style.visibility = 'visible !important';
                            closeBtn.style.opacity = '1 !important';
                            closeBtn.style.pointerEvents = 'auto !important';
                        }
                        
                        // Add click handlers to navigation buttons for auto-close
                        const navButtons = document.querySelectorAll('[data-testid="stSidebar"] button');
                        navButtons.forEach((btn, index) => {
                            // Remove existing listeners to prevent duplicates
                            btn.replaceWith(btn.cloneNode(true));
                        });
                        
                        // Re-select buttons after cloning and add new listeners
                        const freshNavButtons = document.querySelectorAll('[data-testid="stSidebar"] button');
                        freshNavButtons.forEach(btn => {
                            btn.addEventListener('click', (e) => {
                                // Allow the original click to process first
                                setTimeout(() => {
                                    // Try multiple methods to close sidebar
                                    const closeBtn = document.querySelector('[data-testid="stSidebarCloseButton"]');
                                    const collapseBtn = document.querySelector('[data-testid="stSidebarCollapseButton"]');
                                    
                                    if (closeBtn && closeBtn.offsetParent !== null) {
                                        closeBtn.click();
                                    } else if (collapseBtn && collapseBtn.offsetParent !== null) {
                                        collapseBtn.click();
                                    } else {
                                        // Force close by manipulating the sidebar state
                                        const sidebar = document.querySelector('[data-testid="stSidebar"]');
                                        if (sidebar) {
                                            sidebar.style.transform = 'translateX(-100%)';
                                            sidebar.style.transition = 'transform 0.3s ease';
                                        }
                                    }
                                }, 200);
                            });
                        });
                        
                        // Ensure close button functionality
                        const closeBtnFinal = document.querySelector('[data-testid="stSidebarCloseButton"]');
                        if (closeBtnFinal) {
                            closeBtnFinal.addEventListener('click', () => {
                                const sidebar = document.querySelector('[data-testid="stSidebar"]');
                                if (sidebar) {
                                    sidebar.style.display = 'none';
                                }
                            });
                        }
                    }
                }
                
                setupMobileSidebar();
                
                // Force scroll to top
                document.documentElement.scrollTop = 0;
                document.body.scrollTop = 0;
                window.pageYOffset = 0;
                
                // Multiple attempts to ensure mobile functionality
                setTimeout(() => setupMobileSidebar(), 300);
                setTimeout(() => setupMobileSidebar(), 800);
                setTimeout(() => setupMobileSidebar(), 1500);
                
                // Handle dynamic content changes
                const observer = new MutationObserver(() => {
                    if (window.innerWidth <= 768) {
                        setupMobileSidebar();
                    }
                });
                
                const sidebarContainer = document.querySelector('[data-testid="stSidebar"]');
                if (sidebarContainer) {
                    observer.observe(sidebarContainer, {
                        childList: true,
                        subtree: true,
                        attributes: true
                    });
                }
                
                // Handle window resize
                window.addEventListener('resize', () => {
                    setupMobileSidebar();
                });
            }, 200);
        }, 100);
        </script>
        """, unsafe_allow_html=True)
        
        # Logo at the top of sidebar - Fully visible and properly sized
        st.markdown("""
        <div class="sidebar-logo" style="text-align: center; padding: 0.75rem 0.1rem; overflow: visible;">
            <svg width="260" height="80" viewBox="0 0 260 80" xmlns="http://www.w3.org/2000/svg">
                <polygon points="12,60 30,18 48,60" fill="#3366FF"/>
                <circle cx="30" cy="18" r="10" fill="#3366FF"/>
                <text x="60" y="45" font-family="Arial,sans-serif" font-size="26" font-weight="bold" fill="#333">MARKETPULSE</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation items with enhanced functionality
        if st.button("🏠 Home", key="home_btn", use_container_width=True):
            st.session_state.current_page = 'Home'
            st.markdown("""
            <script>
                sessionStorage.setItem('currentPage', 'Home');
                setTimeout(() => {
                    window.scrollTo({top: 0, behavior: 'instant'});
                    document.documentElement.scrollTop = 0;
                    document.body.scrollTop = 0;
                }, 100);
            </script>
            """, unsafe_allow_html=True)
            st.rerun()
            
        if st.button("📊 Overview", key="overview_btn", use_container_width=True):
            st.session_state.current_page = 'Overview'
            st.markdown("""
            <script>
                sessionStorage.setItem('currentPage', 'Overview');
                setTimeout(() => {
                    window.scrollTo({top: 0, behavior: 'instant'});
                    document.documentElement.scrollTop = 0;
                    document.body.scrollTop = 0;
                }, 100);
            </script>
            """, unsafe_allow_html=True)
            st.rerun()
            
        if st.button("📺 Channel Analysis", key="channel_btn", use_container_width=True):
            st.session_state.current_page = 'Channel Analysis'
            st.markdown("""
            <script>
                sessionStorage.setItem('currentPage', 'Channel Analysis');
                setTimeout(() => {
                    window.scrollTo({top: 0, behavior: 'instant'});
                    document.documentElement.scrollTop = 0;
                    document.body.scrollTop = 0;
                }, 100);
            </script>
            """, unsafe_allow_html=True)
            st.rerun()
            
        if st.button("💼 Business Impact", key="impact_btn", use_container_width=True):
            st.session_state.current_page = 'Business Impact'
            st.markdown("""
            <script>
                sessionStorage.setItem('currentPage', 'Business Impact');
                setTimeout(() => {
                    window.scrollTo({top: 0, behavior: 'instant'});
                    document.documentElement.scrollTop = 0;
                    document.body.scrollTop = 0;
                }, 100);
            </script>
            """, unsafe_allow_html=True)
            st.rerun()
            
        if st.button("🧠 Business Intelligence", key="bi_btn", use_container_width=True):
            st.session_state.current_page = 'Business Intelligence'
            st.markdown("""
            <script>
                sessionStorage.setItem('currentPage', 'Business Intelligence');
                setTimeout(() => {
                    window.scrollTo({top: 0, behavior: 'instant'});
                    document.documentElement.scrollTop = 0;
                    document.body.scrollTop = 0;
                }, 100);
            </script>
            """, unsafe_allow_html=True)
            st.rerun()

    # Route to different pages based on selection
    if st.session_state.current_page == 'Home':
        show_home_page()
    elif st.session_state.current_page == 'Overview':
        show_overview_page()
    elif st.session_state.current_page == 'Channel Analysis':
        show_channel_analysis_page()
    elif st.session_state.current_page == 'Business Impact':
        show_business_impact_page()
    elif st.session_state.current_page == 'Business Intelligence':
        show_business_intelligence_page()

def show_home_page():
    """Display the main dashboard home page"""
    # Main content header with enhanced styling
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🚀 MarketPulse Dashboard</h1>
        <p style="font-size: 1.2rem; color: #f8f9fa; margin-top: 0.5rem;">
            Marketing Intelligence & Business Performance Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load and process data
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
    
    # Display main dashboard content
    display_main_dashboard(processed_data)

def show_home_page():
    """Display the main dashboard home page"""
    # Main content header with enhanced styling
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2rem;">🚀 MarketPulse Dashboard</h1>
        <p style="font-size: 1.1rem; color: #f8f9fa; margin-top: 0.5rem;">
            Marketing Intelligence & Business Performance Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load and process data
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
    
    # Display main dashboard content
    display_main_dashboard(processed_data)

def display_main_dashboard(processed_data):
    """Display the main dashboard content"""
    # Initialize analytics
    analytics = MarketingAnalytics(processed_data['final_dataset'])
    
    # Display performance alerts
    display_performance_alerts(analytics)
    
    # Calculate metrics
    business_metrics = analytics.calculate_business_impact()
    channel_performance = analytics.calculate_channel_performance()
    daily_trends = analytics.calculate_daily_trends()
    
    # Success message
    st.success(f"🎉 Data loaded successfully | {len(daily_trends)} days analyzed")
    
    st.markdown("---")
    
    # Enhanced KPI Cards
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

def show_overview_page():
    """Load and display the Overview page"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("overview", os.path.join(current_dir, "pages", "1_Overview.py"))
        overview_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(overview_module)
    except Exception as e:
        st.error(f"Error loading Overview page: {e}")
        st.info("Displaying basic overview instead...")
        st.header("📊 Overview")
        st.write("Overview page content would be displayed here.")

def show_channel_analysis_page():
    """Load and display the Channel Analysis page"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("channel_analysis", os.path.join(current_dir, "pages", "2_Channel_Analysis.py"))
        channel_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(channel_module)
    except Exception as e:
        st.error(f"Error loading Channel Analysis page: {e}")
        st.info("Displaying basic channel analysis instead...")
        st.header("📺 Channel Analysis")
        st.write("Channel Analysis page content would be displayed here.")

def show_business_impact_page():
    """Load and display the Business Impact page"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("business_impact", os.path.join(current_dir, "pages", "3_Business_Impact.py"))
        business_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(business_module)
    except Exception as e:
        st.error(f"Error loading Business Impact page: {e}")
        st.info("Displaying basic business impact instead...")
        st.header("💼 Business Impact")
        st.write("Business Impact page content would be displayed here.")

def show_business_intelligence_page():
    """Load and display the Business Intelligence page"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("business_intelligence", os.path.join(current_dir, "pages", "4_Business_Intelligence.py"))
        bi_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bi_module)
    except Exception as e:
        st.error(f"Error loading Business Intelligence page: {e}")
        st.info("Displaying basic business intelligence instead...")
        st.header("🧠 Business Intelligence")
        st.write("Business Intelligence page content would be displayed here.")

if __name__ == "__main__":
    main()