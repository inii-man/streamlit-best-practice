"""
Distribution Plots Page
Histogram, KDE, ECDF, Box Plot, Violin Plot
"""
import streamlit as st
import seaborn as sns
from config import Config
from utils import DataLoader, DataProcessor, VisualizationManager, SeabornPlots
from components import (
    render_header, render_data_selector, render_column_selector,
    render_plot_controls, render_dataframe_explorer, render_download_button
)

st.set_page_config(**Config.PAGE_CONFIG)

# Initialize visualization manager
viz_manager = VisualizationManager(**Config.VIZ_CONFIG)


def main():
    render_header(
        "Distribution Plots",
        "Explore data distributions with histograms, KDE, box plots, and violin plots",
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
        dataset_name = st.sidebar.selectbox(
            "Select Dataset",
            available_datasets,
            help="Choose from Seaborn's built-in datasets"
        )
        
        if dataset_name:
            try:
                df = DataLoader.load_sample_dataset(dataset_name)
                st.sidebar.success(f"✅ Loaded '{dataset_name}' dataset")
            except Exception as e:
                st.sidebar.error(f"Error loading dataset: {str(e)}")
    
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload your data",
            type=['csv', 'xlsx', 'json'],
            help="Upload a CSV, Excel, or JSON file"
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
                st.sidebar.error(f"Error loading file: {str(e)}")
    
    if df is not None:
        # Data explorer
        with st.expander("🔍 Explore Dataset", expanded=False):
            render_dataframe_explorer(df)
        
        st.markdown("---")
        
        # Plot type selection
        plot_type = st.selectbox(
            "Select Plot Type",
            [
                "Histogram with KDE",
                "Box Plot",
                "Violin Plot",
                "KDE Plot",
                "ECDF Plot",
                "Rug Plot"
            ]
        )
        
        numeric_cols = DataProcessor.get_numeric_columns(df)
        categorical_cols = DataProcessor.get_categorical_columns(df)
        
        if plot_type == "Histogram with KDE":
            st.markdown("### 📊 Histogram with KDE")
            st.markdown("Visualize the distribution of a numeric variable with optional kernel density estimation.")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if numeric_cols:
                    column = st.selectbox("Select Numeric Column", numeric_cols)
                    
                    with st.expander("⚙️ Plot Settings"):
                        bins = st.slider("Number of Bins", 10, 100, 30)
                        kde = st.checkbox("Show KDE", value=True)
                        figsize_w = st.slider("Figure Width", 6, 20, 10)
                        figsize_h = st.slider("Figure Height", 4, 16, 6)
                    
                    # Create plot
                    fig = SeabornPlots.distribution_plot(
                        df, column, kde=kde, bins=bins,
                        figsize=(figsize_w, figsize_h)
                    )
                    
                    st.pyplot(fig)
                    render_download_button(fig, f"histogram_{column}.png")
                else:
                    st.warning("No numeric columns found in the dataset")
            
            with col2:
                if numeric_cols:
                    st.markdown("#### 📈 Statistics")
                    st.metric("Mean", f"{df[column].mean():.2f}")
                    st.metric("Median", f"{df[column].median():.2f}")
                    st.metric("Std Dev", f"{df[column].std():.2f}")
                    st.metric("Min", f"{df[column].min():.2f}")
                    st.metric("Max", f"{df[column].max():.2f}")
        
        elif plot_type == "Box Plot":
            st.markdown("### 📦 Box Plot")
            st.markdown("Show the distribution of data through quartiles, highlighting outliers.")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if numeric_cols:
                    y_col = st.selectbox("Select Numeric Column (Y-axis)", numeric_cols)
                    
                    x_col = None
                    hue_col = None
                    
                    if categorical_cols:
                        use_x = st.checkbox("Group by categorical variable")
                        if use_x:
                            x_col = st.selectbox("Select Categorical Column (X-axis)", categorical_cols)
                        
                        use_hue = st.checkbox("Color by another variable")
                        if use_hue:
                            available_hue = [col for col in categorical_cols if col != x_col]
                            if available_hue:
                                hue_col = st.selectbox("Select Hue Column", available_hue)
                    
                    with st.expander("⚙️ Plot Settings"):
                        figsize_w = st.slider("Figure Width", 6, 20, 10)
                        figsize_h = st.slider("Figure Height", 4, 16, 6)
                    
                    # Create plot
                    fig = SeabornPlots.box_plot(
                        df, x=x_col, y=y_col, hue=hue_col,
                        figsize=(figsize_w, figsize_h)
                    )
                    
                    st.pyplot(fig)
                    render_download_button(fig, f"boxplot_{y_col}.png")
                else:
                    st.warning("No numeric columns found in the dataset")
            
            with col2:
                if numeric_cols:
                    st.markdown("#### 📊 Box Plot Info")
                    st.info("""
                    **Elements:**
                    - Box: IQR (Q1-Q3)
                    - Line: Median
                    - Whiskers: 1.5×IQR
                    - Points: Outliers
                    """)
        
        elif plot_type == "Violin Plot":
            st.markdown("### 🎻 Violin Plot")
            st.markdown("Combine box plot with kernel density estimation for richer distribution view.")
            
            if numeric_cols:
                y_col = st.selectbox("Select Numeric Column (Y-axis)", numeric_cols)
                
                x_col = None
                hue_col = None
                
                if categorical_cols:
                    use_x = st.checkbox("Group by categorical variable")
                    if use_x:
                        x_col = st.selectbox("Select Categorical Column (X-axis)", categorical_cols)
                    
                    use_hue = st.checkbox("Color by another variable")
                    if use_hue:
                        available_hue = [col for col in categorical_cols if col != x_col]
                        if available_hue:
                            hue_col = st.selectbox("Select Hue Column", available_hue)
                
                with st.expander("⚙️ Plot Settings"):
                    figsize_w = st.slider("Figure Width", 6, 20, 10)
                    figsize_h = st.slider("Figure Height", 4, 16, 6)
                
                # Create plot
                fig = SeabornPlots.violin_plot(
                    df, x=x_col, y=y_col, hue=hue_col,
                    figsize=(figsize_w, figsize_h)
                )
                
                st.pyplot(fig)
                render_download_button(fig, f"violinplot_{y_col}.png")
            else:
                st.warning("No numeric columns found in the dataset")
        
        elif plot_type == "KDE Plot":
            st.markdown("### 📈 KDE Plot")
            st.markdown("Kernel Density Estimation - smooth estimation of probability density.")
            
            if numeric_cols:
                x_col = st.selectbox("Select X Column", numeric_cols)
                
                use_y = st.checkbox("Create 2D KDE plot")
                y_col = None
                if use_y and len(numeric_cols) > 1:
                    available_y = [col for col in numeric_cols if col != x_col]
                    y_col = st.selectbox("Select Y Column", available_y)
                
                hue_col = None
                if categorical_cols:
                    use_hue = st.checkbox("Color by categorical variable")
                    if use_hue:
                        hue_col = st.selectbox("Select Hue Column", categorical_cols)
                
                with st.expander("⚙️ Plot Settings"):
                    fill = st.checkbox("Fill under curve", value=True)
                    figsize_w = st.slider("Figure Width", 6, 20, 10)
                    figsize_h = st.slider("Figure Height", 4, 16, 6)
                
                # Create plot
                fig = SeabornPlots.kde_plot(
                    df, x=x_col, y=y_col, hue=hue_col, fill=fill,
                    figsize=(figsize_w, figsize_h)
                )
                
                st.pyplot(fig)
                render_download_button(fig, f"kdeplot_{x_col}.png")
            else:
                st.warning("No numeric columns found in the dataset")
        
        elif plot_type == "ECDF Plot":
            st.markdown("### 📊 ECDF Plot")
            st.markdown("Empirical Cumulative Distribution Function - shows proportion of data below each value.")
            
            if numeric_cols:
                x_col = st.selectbox("Select Column", numeric_cols)
                
                hue_col = None
                if categorical_cols:
                    use_hue = st.checkbox("Color by categorical variable")
                    if use_hue:
                        hue_col = st.selectbox("Select Hue Column", categorical_cols)
                
                with st.expander("⚙️ Plot Settings"):
                    figsize_w = st.slider("Figure Width", 6, 20, 10)
                    figsize_h = st.slider("Figure Height", 4, 16, 6)
                
                # Create plot
                fig = SeabornPlots.ecdf_plot(
                    df, x=x_col, hue=hue_col,
                    figsize=(figsize_w, figsize_h)
                )
                
                st.pyplot(fig)
                render_download_button(fig, f"ecdfplot_{x_col}.png")
            else:
                st.warning("No numeric columns found in the dataset")
        
        elif plot_type == "Rug Plot":
            st.markdown("### 📏 Rug Plot")
            st.markdown("Display individual data points along an axis - useful for showing data density.")
            
            if numeric_cols:
                x_col = st.selectbox("Select Column", numeric_cols)
                
                hue_col = None
                if categorical_cols:
                    use_hue = st.checkbox("Color by categorical variable")
                    if use_hue:
                        hue_col = st.selectbox("Select Hue Column", categorical_cols)
                
                with st.expander("⚙️ Plot Settings"):
                    figsize_w = st.slider("Figure Width", 6, 20, 10)
                    figsize_h = st.slider("Figure Height", 4, 16, 4)
                
                # Create plot
                fig = SeabornPlots.rug_plot(
                    df, x=x_col, hue=hue_col,
                    figsize=(figsize_w, figsize_h)
                )
                
                st.pyplot(fig)
                render_download_button(fig, f"rugplot_{x_col}.png")
            else:
                st.warning("No numeric columns found in the dataset")
    
    else:
        st.info("👈 Please select or upload a dataset from the sidebar to begin")
        
        st.markdown("""
        ### 📚 About Distribution Plots
        
        Distribution plots help you understand how your data is spread out:
        
        - **Histogram**: Shows frequency distribution of a numeric variable
        - **KDE**: Smooth curve showing probability density
        - **Box Plot**: Shows quartiles, median, and outliers
        - **Violin Plot**: Combines box plot with KDE for richer view
        - **ECDF**: Shows cumulative distribution
        - **Rug Plot**: Shows individual data points
        """)


if __name__ == "__main__":
    main()
