"""
Professional Seaborn Visualization Dashboard
Main application entry point
"""
import streamlit as st
from config import Config
from utils import SessionManager
from components import render_header, render_sidebar_info

# Page configuration
st.set_page_config(**Config.PAGE_CONFIG)

# Initialize session state
SessionManager.init_session_state(st, {
    'current_dataset': None,
    'df': None,
    'theme': 'dark',
})


def main():
    """Main application"""
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stPlotlyChart {
            background-color: transparent;
        }
        div[data-testid="stMetricValue"] {
            font-size: 2rem;
        }
        .css-1d391kg {
            padding-top: 3rem;
        }
        h1 {
            padding-bottom: 1rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 1rem 2rem;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    render_header(
        title="Professional Data Visualization Dashboard",
        subtitle="Complete Seaborn & Matplotlib Visualization Suite",
        icon="📊"
    )
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        st.info(
            "👈 Use the navigation menu above to explore different types of visualizations"
        )
        
        st.markdown("---")
        
        st.markdown("## 🎨 Features")
        st.markdown("""
        - 📊 **20+ Plot Types**
        - 🔒 **Secure Data Handling**
        - 📁 **Multiple Data Sources**
        - 🎨 **Customizable Themes**
        - 📥 **Export Capabilities**
        - 📱 **Responsive Design**
        """)
        
        st.markdown("---")
        
        st.markdown("## 📚 Available Visualizations")
        st.markdown("""
        1. **Distribution Plots**
           - Histogram, KDE, ECDF
        
        2. **Categorical Plots**
           - Bar, Count, Box, Violin
        
        3. **Relationship Plots**
           - Scatter, Line, Regression
        
        4. **Matrix Plots**
           - Heatmap, Correlation
        
        5. **Multi-Plot Grids**
           - Pair Plot, Facet Grid
        
        6. **Advanced Plots**
           - Joint Plot, Residual Plot
        """)
    
    # Main content
    st.markdown("## 🚀 Getting Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color: #1e3a5f; padding: 2rem; border-radius: 10px; text-align: center;'>
            <h2>1️⃣</h2>
            <h3>Choose Dataset</h3>
            <p>Select from built-in Seaborn datasets or upload your own</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #1e3a5f; padding: 2rem; border-radius: 10px; text-align: center;'>
            <h2>2️⃣</h2>
            <h3>Select Visualization</h3>
            <p>Navigate to any visualization page from the sidebar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #1e3a5f; padding: 2rem; border-radius: 10px; text-align: center;'>
            <h2>3️⃣</h2>
            <h3>Customize & Export</h3>
            <p>Adjust settings and download your visualizations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick demo section
    st.markdown("## 📈 Quick Demo")
    
    demo_tab1, demo_tab2, demo_tab3 = st.tabs(["🎯 Overview", "📊 Example", "💡 Tips"])
    
    with demo_tab1:
        st.markdown("""
        ### Welcome to the Professional Data Visualization Dashboard!
        
        This application provides a comprehensive suite of data visualization tools using:
        
        - **Seaborn**: Statistical data visualization library
        - **Matplotlib**: Comprehensive plotting library
        - **Pandas**: Data manipulation and analysis
        - **NumPy**: Numerical computing
        
        #### Key Features:
        
        ✅ **Best Practices**
        - Proper project structure with separation of concerns
        - Environment-based configuration management
        - Security features for data handling
        - Reusable components architecture
        
        ✅ **Professional Quality**
        - Clean, modern UI design
        - Responsive layouts
        - High-quality plot exports
        - Comprehensive documentation
        
        ✅ **Easy to Use**
        - Intuitive navigation
        - Interactive controls
        - Real-time updates
        - Multiple data source support
        """)
    
    with demo_tab2:
        st.markdown("""
        ### 📊 Example Workflow
        
        1. **Navigate to a visualization page** (e.g., "Distribution Plots")
        2. **Select or upload a dataset**
        3. **Choose columns to visualize**
        4. **Customize the plot** using the controls
        5. **Download** your visualization
        
        Try starting with the **Distribution Plots** page to see examples!
        """)
        
        # Show a simple example
        import pandas as pd
        import numpy as np
        
        st.markdown("#### Sample Data Preview")
        sample_data = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D', 'E'] * 10,
            'Value': np.random.randn(50) * 10 + 50,
            'Group': np.random.choice(['Group 1', 'Group 2'], 50)
        })
        st.dataframe(sample_data.head(10), use_container_width=True)
    
    with demo_tab3:
        st.markdown("""
        ### 💡 Tips for Best Results
        
        🎨 **Visualization Tips:**
        - Choose the right plot type for your data
        - Use color strategically to highlight insights
        - Keep titles and labels clear and concise
        - Consider your audience when designing
        
        📊 **Data Tips:**
        - Clean your data before visualization
        - Check for missing values and outliers
        - Understand your data distribution
        - Use appropriate aggregations
        
        🔧 **Technical Tips:**
        - Use the sidebar filters to focus on specific data
        - Experiment with different color palettes
        - Export plots in high resolution (300+ DPI)
        - Save your favorite configurations
        
        🔒 **Security Tips:**
        - Never upload sensitive data to public servers
        - Use environment variables for credentials
        - Keep your dependencies updated
        - Review data before sharing visualizations
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
        <div style='text-align: center; padding: 2rem; color: #888;'>
            <p>Built with ❤️ using Streamlit, Seaborn, and Matplotlib</p>
            <p>Professional Data Visualization Dashboard © 2024</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
