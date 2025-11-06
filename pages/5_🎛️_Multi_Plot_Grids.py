"""
Multi-Plot Grids Page
Pair Plot, Facet Grid, Joint Plot
"""
import streamlit as st
from config import Config
from utils import DataLoader, DataProcessor, VisualizationManager, SeabornPlots
from components import render_header, render_dataframe_explorer

st.set_page_config(**Config.PAGE_CONFIG)

viz_manager = VisualizationManager(**Config.VIZ_CONFIG)


def main():
    render_header(
        "Multi-Plot Grids",
        "Explore multiple relationships simultaneously",
        "🎛️"
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
            ["Pair Plot", "Joint Plot", "Facet Grid", "LM Plot (Regression Facet)"]
        )
        
        numeric_cols = DataProcessor.get_numeric_columns(df)
        categorical_cols = DataProcessor.get_categorical_columns(df)
        
        if plot_type == "Pair Plot":
            st.markdown("### 🔢 Pair Plot")
            st.markdown("Visualize pairwise relationships between multiple numeric variables.")
            
            if len(numeric_cols) >= 2:
                st.warning("⚠️ This plot may take some time with large datasets or many variables.")
                
                # Column selection
                use_all = st.checkbox("Use all numeric columns", value=False)
                
                if use_all:
                    selected_cols = numeric_cols
                else:
                    max_default = min(5, len(numeric_cols))
                    selected_cols = st.multiselect(
                        "Select numeric columns (recommended: 3-6 columns)",
                        numeric_cols,
                        default=numeric_cols[:max_default]
                    )
                
                hue_col = None
                if categorical_cols:
                    use_hue = st.checkbox("Color by categorical variable")
                    if use_hue:
                        # Filter categorical columns with reasonable number of unique values
                        suitable_hue = [col for col in categorical_cols 
                                       if df[col].nunique() <= 10]
                        if suitable_hue:
                            hue_col = st.selectbox(
                                "Select Hue Column (max 10 unique values recommended)",
                                suitable_hue
                            )
                        else:
                            st.warning("No suitable categorical columns (need ≤10 unique values)")
                
                if selected_cols and len(selected_cols) >= 2:
                    if st.button("Generate Pair Plot", type="primary"):
                        with st.spinner("Creating pair plot... This may take a moment"):
                            try:
                                # Sample data if too large
                                if len(df) > 1000:
                                    st.info("Using random sample of 1000 rows for better performance")
                                    df_plot = df.sample(n=1000, random_state=42)
                                else:
                                    df_plot = df
                                
                                plot = SeabornPlots.pair_plot(
                                    df_plot,
                                    hue=hue_col,
                                    vars=selected_cols
                                )
                                
                                st.pyplot(plot.fig)
                                
                                # Download
                                import io
                                buf = io.BytesIO()
                                plot.fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                                buf.seek(0)
                                
                                st.download_button(
                                    label="📥 Download Pair Plot",
                                    data=buf,
                                    file_name="pairplot.png",
                                    mime="image/png"
                                )
                            except Exception as e:
                                st.error(f"Error creating pair plot: {str(e)}")
                else:
                    st.info("Please select at least 2 columns to create pair plot")
            else:
                st.warning("Need at least 2 numeric columns")
        
        elif plot_type == "Joint Plot":
            st.markdown("### 🔀 Joint Plot")
            st.markdown("Bivariate plot with marginal distributions.")
            
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("Select X Column", numeric_cols, key="joint_x")
                
                with col2:
                    available_y = [col for col in numeric_cols if col != x_col]
                    y_col = st.selectbox("Select Y Column", available_y, key="joint_y")
                
                kind = st.selectbox(
                    "Plot Type",
                    ["scatter", "kde", "hex", "reg", "resid"],
                    help="Type of plot for the joint axes"
                )
                
                hue_col = None
                if kind in ["scatter", "kde"]:  # Only these support hue
                    if categorical_cols:
                        use_hue = st.checkbox("Color by categorical variable")
                        if use_hue:
                            suitable_hue = [col for col in categorical_cols 
                                          if df[col].nunique() <= 10]
                            if suitable_hue:
                                hue_col = st.selectbox("Select Hue Column", suitable_hue)
                
                if st.button("Generate Joint Plot", type="primary"):
                    with st.spinner("Creating joint plot..."):
                        try:
                            plot = SeabornPlots.joint_plot(
                                df, x=x_col, y=y_col, kind=kind, hue=hue_col
                            )
                            
                            st.pyplot(plot.fig)
                            
                            # Download
                            import io
                            buf = io.BytesIO()
                            plot.fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                            buf.seek(0)
                            
                            st.download_button(
                                label="📥 Download Joint Plot",
                                data=buf,
                                file_name=f"jointplot_{x_col}_{y_col}.png",
                                mime="image/png"
                            )
                        except Exception as e:
                            st.error(f"Error creating joint plot: {str(e)}")
            else:
                st.warning("Need at least 2 numeric columns")
        
        elif plot_type == "Facet Grid":
            st.markdown("### 🎛️ Facet Grid")
            st.markdown("Create a grid of subplots based on categorical variables.")
            
            if numeric_cols and categorical_cols:
                st.info("Facet Grid creates multiple subplots organized by categorical variables.")
                
                # Select faceting variables
                col1, col2 = st.columns(2)
                
                with col1:
                    use_row = st.checkbox("Create row facets")
                    row_col = None
                    if use_row:
                        suitable_row = [col for col in categorical_cols 
                                       if df[col].nunique() <= 5]
                        if suitable_row:
                            row_col = st.selectbox(
                                "Row variable (max 5 unique recommended)",
                                suitable_row
                            )
                        else:
                            st.warning("No suitable columns (need ≤5 unique values)")
                
                with col2:
                    use_col = st.checkbox("Create column facets")
                    col_col = None
                    if use_col:
                        suitable_col = [col for col in categorical_cols 
                                       if col != row_col and df[col].nunique() <= 5]
                        if suitable_col:
                            col_col = st.selectbox(
                                "Column variable (max 5 unique recommended)",
                                suitable_col
                            )
                        else:
                            st.warning("No suitable columns (need ≤5 unique values)")
                
                # Select plot type and variables
                plot_kind = st.selectbox(
                    "Plot Type",
                    ["scatter", "hist", "kde"]
                )
                
                if plot_kind == "scatter":
                    col3, col4 = st.columns(2)
                    with col3:
                        x_col = st.selectbox("X Variable", numeric_cols, key="facet_x")
                    with col4:
                        available_y = [col for col in numeric_cols if col != x_col]
                        y_col = st.selectbox("Y Variable", available_y, key="facet_y")
                    
                    # Hue
                    hue_col = None
                    remaining_cat = [col for col in categorical_cols 
                                    if col not in [row_col, col_col]]
                    if remaining_cat:
                        use_hue = st.checkbox("Color by another variable")
                        if use_hue:
                            suitable_hue = [col for col in remaining_cat 
                                          if df[col].nunique() <= 5]
                            if suitable_hue:
                                hue_col = st.selectbox("Hue Variable", suitable_hue)
                else:
                    x_col = st.selectbox("Variable", numeric_cols)
                    y_col = None
                    hue_col = None
                
                if (row_col or col_col) and x_col:
                    if st.button("Generate Facet Grid", type="primary"):
                        with st.spinner("Creating facet grid..."):
                            try:
                                plot = SeabornPlots.facet_grid(
                                    df,
                                    row=row_col,
                                    col=col_col,
                                    hue=hue_col,
                                    plot_type=plot_kind,
                                    x=x_col,
                                    y=y_col
                                )
                                
                                st.pyplot(plot.fig)
                                
                                # Download
                                import io
                                buf = io.BytesIO()
                                plot.fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                                buf.seek(0)
                                
                                st.download_button(
                                    label="📥 Download Facet Grid",
                                    data=buf,
                                    file_name="facetgrid.png",
                                    mime="image/png"
                                )
                            except Exception as e:
                                st.error(f"Error creating facet grid: {str(e)}")
                else:
                    st.info("Please select at least one faceting variable (row or column)")
            else:
                st.warning("Need both numeric and categorical columns")
        
        elif plot_type == "LM Plot (Regression Facet)":
            st.markdown("### 📉 LM Plot")
            st.markdown("Regression plots in a facet grid layout.")
            
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("Select X Column", numeric_cols, key="lm_x")
                
                with col2:
                    available_y = [col for col in numeric_cols if col != x_col]
                    y_col = st.selectbox("Select Y Column", available_y, key="lm_y")
                
                hue_col = None
                col_col = None
                
                if categorical_cols:
                    use_hue = st.checkbox("Color by categorical variable")
                    if use_hue:
                        suitable_hue = [col for col in categorical_cols 
                                       if df[col].nunique() <= 5]
                        if suitable_hue:
                            hue_col = st.selectbox("Select Hue Column", suitable_hue)
                    
                    use_col = st.checkbox("Create column facets")
                    if use_col:
                        suitable_col = [col for col in categorical_cols 
                                       if col != hue_col and df[col].nunique() <= 5]
                        if suitable_col:
                            col_col = st.selectbox("Select Column Variable", suitable_col)
                
                if st.button("Generate LM Plot", type="primary"):
                    with st.spinner("Creating LM plot..."):
                        try:
                            plot = SeabornPlots.lm_plot(
                                df, x=x_col, y=y_col, hue=hue_col, col=col_col
                            )
                            
                            st.pyplot(plot.fig)
                            
                            # Download
                            import io
                            buf = io.BytesIO()
                            plot.fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                            buf.seek(0)
                            
                            st.download_button(
                                label="📥 Download LM Plot",
                                data=buf,
                                file_name=f"lmplot_{x_col}_{y_col}.png",
                                mime="image/png"
                            )
                        except Exception as e:
                            st.error(f"Error creating LM plot: {str(e)}")
            else:
                st.warning("Need at least 2 numeric columns")
    
    else:
        st.info("👈 Please select or upload a dataset from the sidebar")
        
        st.markdown("""
        ### 📚 About Multi-Plot Grids
        
        Multi-plot grids help visualize complex relationships:
        
        - **Pair Plot**: Shows all pairwise relationships between numeric variables
        - **Joint Plot**: Combines bivariate and marginal univariate plots
        - **Facet Grid**: Creates subplots for different subsets of data
        - **LM Plot**: Regression plots organized in a grid
        
        #### Tips:
        - Limit the number of variables for better readability
        - Use hue to add an extra dimension
        - Consider data size - sample large datasets
        - Choose appropriate categorical variables (≤10 unique values)
        """)


if __name__ == "__main__":
    main()
