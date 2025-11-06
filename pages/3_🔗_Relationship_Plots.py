"""
Relationship Plots Page
Scatter, Line, Regression plots
"""
import streamlit as st
from config import Config
from utils import DataLoader, DataProcessor, VisualizationManager, SeabornPlots
from components import render_header, render_dataframe_explorer, render_download_button

st.set_page_config(**Config.PAGE_CONFIG)

viz_manager = VisualizationManager(**Config.VIZ_CONFIG)


def main():
    render_header(
        "Relationship Plots",
        "Explore relationships between two or more variables",
        "🔗"
    )
    
    # Sidebar
    st.sidebar.markdown("## 📂 Data Source")
    data_source = st.sidebar.radio("Choose data source", ["Sample Datasets", "Upload File"])
    
    df = None
    
    if data_source == "Sample Datasets":
        available_datasets = DataLoader.get_available_datasets()
        dataset_name = st.sidebar.selectbox("Select Dataset", available_datasets)
        if dataset_name:
            try:
                df = DataLoader.load_sample_dataset(dataset_name)
                st.sidebar.success(f"✅ Loaded '{dataset_name}' dataset")
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")
    else:
        uploaded_file = st.sidebar.file_uploader("Upload your data", type=['csv', 'xlsx', 'json'])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = DataLoader.load_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = DataLoader.load_excel(uploaded_file)
                elif uploaded_file.name.endswith('.json'):
                    df = DataLoader.load_json(uploaded_file)
                st.sidebar.success("✅ File uploaded successfully")
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")
    
    if df is not None:
        with st.expander("🔍 Explore Dataset", expanded=False):
            render_dataframe_explorer(df)
        
        st.markdown("---")
        
        plot_type = st.selectbox(
            "Select Plot Type",
            ["Scatter Plot", "Line Plot", "Regression Plot", "Residual Plot"]
        )
        
        numeric_cols = DataProcessor.get_numeric_columns(df)
        categorical_cols = DataProcessor.get_categorical_columns(df)
        
        if plot_type == "Scatter Plot":
            st.markdown("### 🎯 Scatter Plot")
            st.markdown("Visualize relationship between two numeric variables.")
            
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    x_col = st.selectbox("Select X Column", numeric_cols, key="scatter_x")
                    available_y = [col for col in numeric_cols if col != x_col]
                    y_col = st.selectbox("Select Y Column", available_y, key="scatter_y")
                    
                    hue_col = None
                    size_col = None
                    
                    if categorical_cols:
                        use_hue = st.checkbox("Color by categorical variable")
                        if use_hue:
                            hue_col = st.selectbox("Select Hue Column", categorical_cols)
                    
                    if len(numeric_cols) > 2:
                        use_size = st.checkbox("Size by numeric variable")
                        if use_size:
                            available_size = [col for col in numeric_cols if col not in [x_col, y_col]]
                            size_col = st.selectbox("Select Size Column", available_size)
                    
                    with st.expander("⚙️ Plot Settings"):
                        figsize_w = st.slider("Figure Width", 6, 20, 10)
                        figsize_h = st.slider("Figure Height", 4, 16, 6)
                    
                    fig = SeabornPlots.scatter_plot(
                        df, x=x_col, y=y_col, hue=hue_col, size=size_col,
                        figsize=(figsize_w, figsize_h)
                    )
                    
                    st.pyplot(fig)
                    render_download_button(fig, f"scatter_{x_col}_{y_col}.png")
                
                with col2:
                    st.markdown("#### 📊 Correlation")
                    import numpy as np
                    corr = df[[x_col, y_col]].corr().iloc[0, 1]
                    st.metric("Pearson Correlation", f"{corr:.3f}")
                    
                    if abs(corr) < 0.3:
                        st.info("Weak correlation")
                    elif abs(corr) < 0.7:
                        st.warning("Moderate correlation")
                    else:
                        st.success("Strong correlation")
            else:
                st.warning("Need at least 2 numeric columns")
        
        elif plot_type == "Line Plot":
            st.markdown("### 📈 Line Plot")
            st.markdown("Show trends and changes over time or ordered categories.")
            
            if len(numeric_cols) >= 2 or (len(numeric_cols) >= 1 and len(categorical_cols) >= 1):
                x_col = st.selectbox("Select X Column", df.columns.tolist(), key="line_x")
                y_col = st.selectbox("Select Y Column", numeric_cols, key="line_y")
                
                hue_col = None
                style_col = None
                
                if categorical_cols:
                    use_hue = st.checkbox("Color by categorical variable")
                    if use_hue:
                        hue_col = st.selectbox("Select Hue Column", categorical_cols, key="line_hue")
                    
                    if len(categorical_cols) > 1:
                        use_style = st.checkbox("Style by categorical variable")
                        if use_style:
                            available_style = [col for col in categorical_cols if col != hue_col]
                            if available_style:
                                style_col = st.selectbox("Select Style Column", available_style)
                
                with st.expander("⚙️ Plot Settings"):
                    figsize_w = st.slider("Figure Width", 6, 20, 12)
                    figsize_h = st.slider("Figure Height", 4, 16, 6)
                
                fig = SeabornPlots.line_plot(
                    df, x=x_col, y=y_col, hue=hue_col, style=style_col,
                    figsize=(figsize_w, figsize_h)
                )
                
                st.pyplot(fig)
                render_download_button(fig, f"line_{x_col}_{y_col}.png")
            else:
                st.warning("Need appropriate columns for line plot")
        
        elif plot_type == "Regression Plot":
            st.markdown("### 📉 Regression Plot")
            st.markdown("Scatter plot with linear regression fit and confidence interval.")
            
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    x_col = st.selectbox("Select X Column", numeric_cols, key="reg_x")
                    available_y = [col for col in numeric_cols if col != x_col]
                    y_col = st.selectbox("Select Y Column", available_y, key="reg_y")
                    
                    with st.expander("⚙️ Plot Settings"):
                        figsize_w = st.slider("Figure Width", 6, 20, 10)
                        figsize_h = st.slider("Figure Height", 4, 16, 6)
                    
                    fig = SeabornPlots.regression_plot(
                        df, x=x_col, y=y_col,
                        figsize=(figsize_w, figsize_h)
                    )
                    
                    st.pyplot(fig)
                    render_download_button(fig, f"regression_{x_col}_{y_col}.png")
                
                with col2:
                    st.markdown("#### 📊 Statistics")
                    from scipy import stats
                    
                    # Remove NaN values
                    clean_data = df[[x_col, y_col]].dropna()
                    
                    if len(clean_data) > 2:
                        slope, intercept, r_value, p_value, std_err = stats.linregress(
                            clean_data[x_col], clean_data[y_col]
                        )
                        
                        st.metric("R-squared", f"{r_value**2:.3f}")
                        st.metric("P-value", f"{p_value:.4f}")
                        st.metric("Slope", f"{slope:.3f}")
                        st.metric("Intercept", f"{intercept:.3f}")
                        
                        st.markdown("#### 📝 Equation")
                        st.latex(f"y = {slope:.3f}x + {intercept:.3f}")
            else:
                st.warning("Need at least 2 numeric columns")
        
        elif plot_type == "Residual Plot":
            st.markdown("### 📉 Residual Plot")
            st.markdown("Check regression assumptions by plotting residuals.")
            
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    x_col = st.selectbox("Select X Column", numeric_cols, key="resid_x")
                    available_y = [col for col in numeric_cols if col != x_col]
                    y_col = st.selectbox("Select Y Column", available_y, key="resid_y")
                    
                    with st.expander("⚙️ Plot Settings"):
                        figsize_w = st.slider("Figure Width", 6, 20, 10)
                        figsize_h = st.slider("Figure Height", 4, 16, 6)
                    
                    fig = SeabornPlots.residual_plot(
                        df, x=x_col, y=y_col,
                        figsize=(figsize_w, figsize_h)
                    )
                    
                    st.pyplot(fig)
                    render_download_button(fig, f"residual_{x_col}_{y_col}.png")
                
                with col2:
                    st.markdown("#### ℹ️ Interpretation")
                    st.info("""
                    **Good fit:**
                    - Random scatter
                    - No patterns
                    - Centered at 0
                    
                    **Poor fit:**
                    - Clear patterns
                    - Curves
                    - Funnel shapes
                    """)
            else:
                st.warning("Need at least 2 numeric columns")
    
    else:
        st.info("👈 Please select or upload a dataset from the sidebar")
        
        st.markdown("""
        ### 📚 About Relationship Plots
        
        These plots help visualize relationships between variables:
        
        - **Scatter Plot**: Shows correlation between two numeric variables
        - **Line Plot**: Displays trends over time or categories
        - **Regression Plot**: Adds linear regression line to scatter plot
        - **Residual Plot**: Checks if regression assumptions are met
        
        #### Tips:
        - Look for patterns, trends, and outliers
        - Use color and size to add extra dimensions
        - Check correlation strength
        - Verify regression assumptions
        """)


if __name__ == "__main__":
    main()
