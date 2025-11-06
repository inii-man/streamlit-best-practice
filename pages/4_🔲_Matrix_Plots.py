"""
Matrix Plots Page
Heatmap, Correlation Matrix, Clustermap
"""
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from config import Config
from utils import DataLoader, DataProcessor, VisualizationManager, SeabornPlots
from components import render_header, render_dataframe_explorer, render_download_button

st.set_page_config(**Config.PAGE_CONFIG)

viz_manager = VisualizationManager(**Config.VIZ_CONFIG)


def main():
    render_header(
        "Matrix Plots",
        "Visualize matrices, correlations, and hierarchical clustering",
        "🔲"
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
            ["Correlation Heatmap", "Custom Heatmap", "Pivot Table Heatmap", "Clustermap"]
        )
        
        numeric_cols = DataProcessor.get_numeric_columns(df)
        categorical_cols = DataProcessor.get_categorical_columns(df)
        
        if plot_type == "Correlation Heatmap":
            st.markdown("### 🔥 Correlation Heatmap")
            st.markdown("Visualize correlations between all numeric variables.")
            
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Column selection
                    use_all = st.checkbox("Use all numeric columns", value=True)
                    
                    if use_all:
                        selected_cols = numeric_cols
                    else:
                        selected_cols = st.multiselect(
                            "Select columns",
                            numeric_cols,
                            default=numeric_cols[:min(10, len(numeric_cols))]
                        )
                    
                    if selected_cols and len(selected_cols) >= 2:
                        with st.expander("⚙️ Plot Settings"):
                            corr_method = st.selectbox(
                                "Correlation Method",
                                ["pearson", "spearman", "kendall"]
                            )
                            
                            annot = st.checkbox("Show values", value=True)
                            
                            cmap = st.selectbox(
                                "Color Palette",
                                ["coolwarm", "RdBu_r", "viridis", "plasma", "YlOrRd", "RdYlGn"]
                            )
                            
                            figsize_w = st.slider("Figure Width", 8, 20, 12)
                            figsize_h = st.slider("Figure Height", 6, 20, 10)
                        
                        # Calculate correlation
                        corr_matrix = DataProcessor.correlation_matrix(
                            df[selected_cols], method=corr_method
                        )
                        
                        # Create heatmap
                        fig = SeabornPlots.heatmap(
                            corr_matrix,
                            annot=annot,
                            fmt='.2f',
                            cmap=cmap,
                            figsize=(figsize_w, figsize_h)
                        )
                        
                        st.pyplot(fig)
                        render_download_button(fig, "correlation_heatmap.png")
                        
                        # Show correlation table
                        with st.expander("📊 Correlation Matrix Data"):
                            st.dataframe(corr_matrix, use_container_width=True)
                    else:
                        st.warning("Please select at least 2 columns")
                
                with col2:
                    st.markdown("#### 📊 Info")
                    st.info(f"""
                    **Method:** {corr_method if 'corr_method' in locals() else 'N/A'}
                    
                    **Interpretation:**
                    - 1.0: Perfect positive
                    - 0.0: No correlation
                    - -1.0: Perfect negative
                    
                    **Strength:**
                    - |r| < 0.3: Weak
                    - 0.3 ≤ |r| < 0.7: Moderate
                    - |r| ≥ 0.7: Strong
                    """)
            else:
                st.warning("Need at least 2 numeric columns")
        
        elif plot_type == "Custom Heatmap":
            st.markdown("### 🎨 Custom Heatmap")
            st.markdown("Create heatmap from selected numeric data.")
            
            if len(numeric_cols) >= 2:
                # Select columns
                selected_cols = st.multiselect(
                    "Select numeric columns",
                    numeric_cols,
                    default=numeric_cols[:min(10, len(numeric_cols))]
                )
                
                if selected_cols and len(selected_cols) >= 2:
                    # Optional row filtering
                    if categorical_cols:
                        use_filter = st.checkbox("Filter by categorical variable")
                        if use_filter:
                            filter_col = st.selectbox("Select filter column", categorical_cols)
                            unique_values = df[filter_col].unique().tolist()
                            selected_values = st.multiselect(
                                f"Select {filter_col} values",
                                unique_values,
                                default=unique_values[:min(5, len(unique_values))]
                            )
                            df_filtered = df[df[filter_col].isin(selected_values)]
                        else:
                            df_filtered = df
                    else:
                        df_filtered = df
                    
                    # Limit rows if too many
                    if len(df_filtered) > 100:
                        st.warning(f"Dataset has {len(df_filtered)} rows. Showing first 100 for better visualization.")
                        df_plot = df_filtered[selected_cols].head(100)
                    else:
                        df_plot = df_filtered[selected_cols]
                    
                    with st.expander("⚙️ Plot Settings"):
                        annot = st.checkbox("Show values", value=False)
                        cmap = st.selectbox(
                            "Color Palette",
                            ["viridis", "coolwarm", "RdBu_r", "plasma", "YlOrRd", "RdYlGn"]
                        )
                        figsize_w = st.slider("Figure Width", 8, 20, 12)
                        figsize_h = st.slider("Figure Height", 6, 20, 10)
                    
                    # Create heatmap
                    fig = SeabornPlots.heatmap(
                        df_plot,
                        annot=annot,
                        fmt='.1f',
                        cmap=cmap,
                        figsize=(figsize_w, figsize_h)
                    )
                    
                    st.pyplot(fig)
                    render_download_button(fig, "custom_heatmap.png")
                else:
                    st.warning("Please select at least 2 columns")
            else:
                st.warning("Need at least 2 numeric columns")
        
        elif plot_type == "Pivot Table Heatmap":
            st.markdown("### 📊 Pivot Table Heatmap")
            st.markdown("Create heatmap from aggregated pivot table data.")
            
            if numeric_cols and len(categorical_cols) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    index_col = st.selectbox("Select Index (Rows)", categorical_cols)
                
                with col2:
                    available_cols = [col for col in categorical_cols if col != index_col]
                    columns_col = st.selectbox("Select Columns", available_cols)
                
                values_col = st.selectbox("Select Values (Numeric)", numeric_cols)
                
                aggfunc = st.selectbox(
                    "Aggregation Function",
                    ["mean", "sum", "median", "count", "min", "max"]
                )
                
                try:
                    # Create pivot table
                    pivot_data = DataProcessor.pivot_table(
                        df, 
                        index=index_col,
                        columns=columns_col,
                        values=values_col,
                        aggfunc=aggfunc
                    )
                    
                    with st.expander("⚙️ Plot Settings"):
                        annot = st.checkbox("Show values", value=True)
                        cmap = st.selectbox(
                            "Color Palette",
                            ["YlOrRd", "coolwarm", "RdBu_r", "viridis", "plasma"]
                        )
                        figsize_w = st.slider("Figure Width", 8, 20, 12)
                        figsize_h = st.slider("Figure Height", 6, 20, 10)
                    
                    # Create heatmap
                    fig = SeabornPlots.heatmap(
                        pivot_data,
                        annot=annot,
                        fmt='.1f',
                        cmap=cmap,
                        figsize=(figsize_w, figsize_h)
                    )
                    
                    st.pyplot(fig)
                    render_download_button(fig, "pivot_heatmap.png")
                    
                    # Show pivot table
                    with st.expander("📊 Pivot Table Data"):
                        st.dataframe(pivot_data, use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error creating pivot table: {str(e)}")
            else:
                st.warning("Need at least 1 numeric and 2 categorical columns")
        
        elif plot_type == "Clustermap":
            st.markdown("### 🌳 Clustermap")
            st.markdown("Heatmap with hierarchical clustering of rows and columns.")
            
            if len(numeric_cols) >= 2:
                selected_cols = st.multiselect(
                    "Select numeric columns",
                    numeric_cols,
                    default=numeric_cols[:min(10, len(numeric_cols))]
                )
                
                if selected_cols and len(selected_cols) >= 2:
                    # Limit rows
                    max_rows = st.slider("Maximum rows to display", 10, 100, 50)
                    
                    if len(df) > max_rows:
                        st.info(f"Using first {max_rows} rows for clustering")
                        df_plot = df[selected_cols].head(max_rows)
                    else:
                        df_plot = df[selected_cols]
                    
                    with st.expander("⚙️ Plot Settings"):
                        method = st.selectbox(
                            "Clustering Method",
                            ["average", "single", "complete", "ward"]
                        )
                        
                        metric = st.selectbox(
                            "Distance Metric",
                            ["euclidean", "correlation", "cosine", "manhattan"]
                        )
                        
                        cmap = st.selectbox(
                            "Color Palette",
                            ["viridis", "coolwarm", "RdBu_r", "plasma", "YlOrRd"]
                        )
                        
                        standard_scale = st.selectbox(
                            "Standardize",
                            [None, "rows", "columns"]
                        )
                    
                    try:
                        # Create clustermap
                        fig = plt.figure(figsize=(12, 10))
                        g = sns.clustermap(
                            df_plot,
                            method=method,
                            metric=metric,
                            cmap=cmap,
                            standard_scale=standard_scale,
                            figsize=(12, 10),
                            cbar_kws={'label': 'Value'}
                        )
                        
                        st.pyplot(g.fig)
                        
                        # Download button
                        import io
                        buf = io.BytesIO()
                        g.fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                        buf.seek(0)
                        
                        st.download_button(
                            label="📥 Download Clustermap",
                            data=buf,
                            file_name="clustermap.png",
                            mime="image/png"
                        )
                    
                    except Exception as e:
                        st.error(f"Error creating clustermap: {str(e)}")
                        st.info("Try selecting fewer columns or rows, or check for missing values.")
                else:
                    st.warning("Please select at least 2 columns")
            else:
                st.warning("Need at least 2 numeric columns")
    
    else:
        st.info("👈 Please select or upload a dataset from the sidebar")
        
        st.markdown("""
        ### 📚 About Matrix Plots
        
        Matrix plots are excellent for showing patterns in tabular data:
        
        - **Correlation Heatmap**: Shows correlations between all numeric variables
        - **Custom Heatmap**: Visualize any matrix of numeric values
        - **Pivot Table Heatmap**: Aggregate and visualize categorical relationships
        - **Clustermap**: Group similar rows/columns using hierarchical clustering
        
        #### Tips:
        - Use appropriate color schemes (diverging for correlations, sequential for values)
        - Consider standardization for clustering
        - Limit data size for better readability
        - Check for missing values before creating heatmaps
        """)


if __name__ == "__main__":
    main()
