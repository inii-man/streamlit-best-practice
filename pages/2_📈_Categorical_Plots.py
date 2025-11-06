"""
Categorical Plots Page
Bar, Count, Point, Strip, Swarm plots
"""
import streamlit as st
from config import Config
from utils import DataLoader, DataProcessor, VisualizationManager, SeabornPlots
from components import render_header, render_dataframe_explorer, render_download_button

st.set_page_config(**Config.PAGE_CONFIG)

viz_manager = VisualizationManager(**Config.VIZ_CONFIG)


def main():
    render_header(
        "Categorical Plots",
        "Visualize relationships between categorical and numeric variables",
        "📊"
    )
    
    # Sidebar - Dataset selection
    st.sidebar.markdown("## 📂 Data Source")
    
    data_source = st.sidebar.radio(
        "Choose data source",
        ["Sample Datasets", "Upload File"]
    )
    
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
        uploaded_file = st.sidebar.file_uploader(
            "Upload your data",
            type=['csv', 'xlsx', 'json']
        )
        
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
            ["Bar Plot", "Count Plot", "Point Plot", "Strip Plot", "Swarm Plot"]
        )
        
        numeric_cols = DataProcessor.get_numeric_columns(df)
        categorical_cols = DataProcessor.get_categorical_columns(df)
        
        if plot_type == "Bar Plot":
            st.markdown("### 📊 Bar Plot")
            st.markdown("Show estimates and confidence intervals for numeric values across categories.")
            
            if categorical_cols and numeric_cols:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    x_col = st.selectbox("Select Categorical Column (X-axis)", categorical_cols)
                    y_col = st.selectbox("Select Numeric Column (Y-axis)", numeric_cols)
                    
                    hue_col = None
                    if len(categorical_cols) > 1:
                        use_hue = st.checkbox("Color by another categorical variable")
                        if use_hue:
                            available_hue = [col for col in categorical_cols if col != x_col]
                            hue_col = st.selectbox("Select Hue Column", available_hue)
                    
                    with st.expander("⚙️ Plot Settings"):
                        estimator_choice = st.selectbox(
                            "Estimator",
                            ["mean", "median", "sum", "count"]
                        )
                        import numpy as np
                        estimator_map = {
                            "mean": np.mean,
                            "median": np.median,
                            "sum": np.sum,
                            "count": len
                        }
                        estimator = estimator_map[estimator_choice]
                        
                        figsize_w = st.slider("Figure Width", 6, 20, 10)
                        figsize_h = st.slider("Figure Height", 4, 16, 6)
                    
                    fig = SeabornPlots.bar_plot(
                        df, x=x_col, y=y_col, hue=hue_col, estimator=estimator,
                        figsize=(figsize_w, figsize_h)
                    )
                    
                    st.pyplot(fig)
                    render_download_button(fig, f"barplot_{x_col}_{y_col}.png")
                
                with col2:
                    st.markdown("#### 📈 Info")
                    st.info(f"""
                    **Aggregation:** {estimator_choice}
                    
                    Shows {estimator_choice} of {y_col} for each {x_col} category.
                    
                    Error bars represent confidence intervals.
                    """)
            else:
                st.warning("Need both categorical and numeric columns")
        
        elif plot_type == "Count Plot":
            st.markdown("### 🔢 Count Plot")
            st.markdown("Show counts of observations in each categorical bin.")
            
            if categorical_cols:
                x_col = st.selectbox("Select Categorical Column", categorical_cols)
                
                hue_col = None
                if len(categorical_cols) > 1:
                    use_hue = st.checkbox("Color by another categorical variable")
                    if use_hue:
                        available_hue = [col for col in categorical_cols if col != x_col]
                        hue_col = st.selectbox("Select Hue Column", available_hue)
                
                with st.expander("⚙️ Plot Settings"):
                    figsize_w = st.slider("Figure Width", 6, 20, 10)
                    figsize_h = st.slider("Figure Height", 4, 16, 6)
                
                fig = SeabornPlots.count_plot(
                    df, x=x_col, hue=hue_col,
                    figsize=(figsize_w, figsize_h)
                )
                
                st.pyplot(fig)
                render_download_button(fig, f"countplot_{x_col}.png")
                
                # Show counts
                st.markdown("#### 📊 Value Counts")
                counts = df[x_col].value_counts()
                st.dataframe(counts, use_container_width=True)
            else:
                st.warning("No categorical columns found")
        
        elif plot_type == "Point Plot":
            st.markdown("### 📍 Point Plot")
            st.markdown("Show point estimates and confidence intervals with connected lines.")
            
            if categorical_cols and numeric_cols:
                x_col = st.selectbox("Select Categorical Column (X-axis)", categorical_cols)
                y_col = st.selectbox("Select Numeric Column (Y-axis)", numeric_cols)
                
                hue_col = None
                if len(categorical_cols) > 1:
                    use_hue = st.checkbox("Color by another categorical variable")
                    if use_hue:
                        available_hue = [col for col in categorical_cols if col != x_col]
                        hue_col = st.selectbox("Select Hue Column", available_hue)
                
                with st.expander("⚙️ Plot Settings"):
                    figsize_w = st.slider("Figure Width", 6, 20, 10)
                    figsize_h = st.slider("Figure Height", 4, 16, 6)
                
                fig = SeabornPlots.point_plot(
                    df, x=x_col, y=y_col, hue=hue_col,
                    figsize=(figsize_w, figsize_h)
                )
                
                st.pyplot(fig)
                render_download_button(fig, f"pointplot_{x_col}_{y_col}.png")
            else:
                st.warning("Need both categorical and numeric columns")
        
        elif plot_type == "Strip Plot":
            st.markdown("### 🎯 Strip Plot")
            st.markdown("Show all observations with small random jitter to reduce overlap.")
            
            if categorical_cols and numeric_cols:
                x_col = st.selectbox("Select Categorical Column (X-axis)", categorical_cols)
                y_col = st.selectbox("Select Numeric Column (Y-axis)", numeric_cols)
                
                hue_col = None
                if len(categorical_cols) > 1:
                    use_hue = st.checkbox("Color by another categorical variable")
                    if use_hue:
                        available_hue = [col for col in categorical_cols if col != x_col]
                        hue_col = st.selectbox("Select Hue Column", available_hue)
                
                with st.expander("⚙️ Plot Settings"):
                    figsize_w = st.slider("Figure Width", 6, 20, 10)
                    figsize_h = st.slider("Figure Height", 4, 16, 6)
                
                fig = SeabornPlots.strip_plot(
                    df, x=x_col, y=y_col, hue=hue_col,
                    figsize=(figsize_w, figsize_h)
                )
                
                st.pyplot(fig)
                render_download_button(fig, f"stripplot_{x_col}_{y_col}.png")
            else:
                st.warning("Need both categorical and numeric columns")
        
        elif plot_type == "Swarm Plot":
            st.markdown("### 🐝 Swarm Plot")
            st.markdown("Show all observations with adjusted positions to avoid overlap.")
            
            if categorical_cols and numeric_cols:
                # Check data size
                if len(df) > 1000:
                    st.warning("⚠️ Swarm plot works best with smaller datasets (<1000 rows). Consider sampling your data.")
                    use_sample = st.checkbox("Use random sample (1000 rows)")
                    if use_sample:
                        df_plot = df.sample(n=1000, random_state=42)
                    else:
                        df_plot = df
                else:
                    df_plot = df
                
                x_col = st.selectbox("Select Categorical Column (X-axis)", categorical_cols)
                y_col = st.selectbox("Select Numeric Column (Y-axis)", numeric_cols)
                
                hue_col = None
                if len(categorical_cols) > 1:
                    use_hue = st.checkbox("Color by another categorical variable")
                    if use_hue:
                        available_hue = [col for col in categorical_cols if col != x_col]
                        hue_col = st.selectbox("Select Hue Column", available_hue)
                
                with st.expander("⚙️ Plot Settings"):
                    figsize_w = st.slider("Figure Width", 6, 20, 10)
                    figsize_h = st.slider("Figure Height", 4, 16, 6)
                
                try:
                    fig = SeabornPlots.swarm_plot(
                        df_plot, x=x_col, y=y_col, hue=hue_col,
                        figsize=(figsize_w, figsize_h)
                    )
                    
                    st.pyplot(fig)
                    render_download_button(fig, f"swarmplot_{x_col}_{y_col}.png")
                except Exception as e:
                    st.error(f"Error creating swarm plot: {str(e)}")
                    st.info("Try reducing your dataset size or use strip plot instead.")
            else:
                st.warning("Need both categorical and numeric columns")
    
    else:
        st.info("👈 Please select or upload a dataset from the sidebar")
        
        st.markdown("""
        ### 📚 About Categorical Plots
        
        These plots show relationships between categorical and numeric variables:
        
        - **Bar Plot**: Shows aggregated values with confidence intervals
        - **Count Plot**: Shows frequency of categorical values
        - **Point Plot**: Connects point estimates across categories
        - **Strip Plot**: Shows all individual data points with jitter
        - **Swarm Plot**: Shows all points with no overlap (best for smaller datasets)
        """)


if __name__ == "__main__":
    main()
