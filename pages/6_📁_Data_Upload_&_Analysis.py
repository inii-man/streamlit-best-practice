"""
Data Upload & Analysis Page
Upload custom data and perform exploratory analysis
"""
import streamlit as st
import pandas as pd
import numpy as np
from config import Config
from utils import DataLoader, DataProcessor, DataValidator, VisualizationManager
from components import render_header, render_dataframe_explorer

st.set_page_config(**Config.PAGE_CONFIG)


def main():
    render_header(
        "Data Upload & Analysis",
        "Upload your data and perform exploratory data analysis",
        "📁"
    )
    
    st.markdown("""
    Upload your dataset to explore its structure, quality, and basic statistics.
    Supported formats: CSV, Excel, JSON
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📤 Choose a file",
        type=['csv', 'xlsx', 'json'],
        help="Upload a CSV, Excel, or JSON file (max 200MB)"
    )
    
    if uploaded_file is not None:
        # Load data based on file type
        try:
            with st.spinner("Loading data..."):
                if uploaded_file.name.endswith('.csv'):
                    df = DataLoader.load_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = DataLoader.load_excel(uploaded_file)
                elif uploaded_file.name.endswith('.json'):
                    df = DataLoader.load_json(uploaded_file)
            
            st.success(f"✅ Successfully loaded '{uploaded_file.name}'")
            
            # Basic info
            st.markdown("## 📊 Dataset Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Rows", f"{df.shape[0]:,}")
            
            with col2:
                st.metric("Columns", f"{df.shape[1]:,}")
            
            with col3:
                memory_mb = df.memory_usage(deep=True).sum() / 1024**2
                st.metric("Memory", f"{memory_mb:.2f} MB")
            
            with col4:
                duplicates = df.duplicated().sum()
                st.metric("Duplicates", f"{duplicates:,}")
            
            st.markdown("---")
            
            # Tabs for different analyses
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📋 Data Preview",
                "📈 Statistics",
                "🔍 Data Quality",
                "🧹 Data Cleaning",
                "💾 Export"
            ])
            
            with tab1:
                st.markdown("### 📋 Data Preview")
                
                # Show/hide options
                col1, col2 = st.columns(2)
                with col1:
                    n_rows = st.number_input("Number of rows to display", 
                                            min_value=5, max_value=1000, value=10)
                with col2:
                    show_from = st.selectbox("Show from", ["Head", "Tail", "Random"])
                
                if show_from == "Head":
                    st.dataframe(df.head(n_rows), use_container_width=True)
                elif show_from == "Tail":
                    st.dataframe(df.tail(n_rows), use_container_width=True)
                else:
                    st.dataframe(df.sample(n=min(n_rows, len(df)), random_state=42), 
                               use_container_width=True)
                
                # Column information
                st.markdown("### 📊 Column Information")
                
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.values,
                    'Non-Null': df.count().values,
                    'Null': df.isnull().sum().values,
                    'Null %': (df.isnull().sum() / len(df) * 100).values,
                    'Unique': df.nunique().values
                })
                
                st.dataframe(col_info, use_container_width=True)
            
            with tab2:
                st.markdown("### 📈 Statistical Summary")
                
                # Numeric statistics
                numeric_cols = DataProcessor.get_numeric_columns(df)
                if numeric_cols:
                    st.markdown("#### Numeric Columns")
                    st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                    
                    # Correlation
                    if len(numeric_cols) > 1:
                        st.markdown("#### Correlation Matrix")
                        corr_method = st.selectbox("Method", ["pearson", "spearman", "kendall"])
                        corr = DataProcessor.correlation_matrix(df, method=corr_method)
                        st.dataframe(corr.style.background_gradient(cmap='coolwarm', axis=None),
                                   use_container_width=True)
                else:
                    st.info("No numeric columns found")
                
                # Categorical statistics
                categorical_cols = DataProcessor.get_categorical_columns(df)
                if categorical_cols:
                    st.markdown("#### Categorical Columns")
                    
                    for col in categorical_cols[:5]:  # Show first 5
                        with st.expander(f"📊 {col}"):
                            value_counts = df[col].value_counts()
                            
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.dataframe(value_counts, use_container_width=True)
                            
                            with col2:
                                st.metric("Unique Values", df[col].nunique())
                                st.metric("Most Common", value_counts.index[0])
                                st.metric("Frequency", value_counts.values[0])
                    
                    if len(categorical_cols) > 5:
                        st.info(f"Showing first 5 of {len(categorical_cols)} categorical columns")
                else:
                    st.info("No categorical columns found")
            
            with tab3:
                st.markdown("### 🔍 Data Quality Assessment")
                
                # Missing data
                st.markdown("#### Missing Data Analysis")
                missing_df = DataValidator.check_missing_data(df)
                missing_df = missing_df[missing_df['Missing_Count'] > 0]
                
                if not missing_df.empty:
                    st.dataframe(missing_df, use_container_width=True)
                    
                    # Visualize missing data
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots(figsize=(10, 6))
                    missing_df['Missing_Percent'].plot(kind='barh', ax=ax, color='#FF6B6B')
                    ax.set_xlabel('Missing Percentage (%)')
                    ax.set_title('Missing Data by Column')
                    plt.tight_layout()
                    st.pyplot(fig)
                else:
                    st.success("✅ No missing data found!")
                
                # Duplicates
                st.markdown("#### Duplicate Rows")
                dup_info = DataValidator.check_duplicates(df)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Duplicate Rows", dup_info['duplicate_count'])
                with col2:
                    st.metric("Duplicate Percentage", f"{dup_info['duplicate_percent']:.2f}%")
                
                # Outliers (for numeric columns)
                if numeric_cols:
                    st.markdown("#### Outlier Detection")
                    
                    selected_col = st.selectbox("Select column for outlier detection", numeric_cols)
                    method = st.radio("Detection method", ["IQR", "Z-score"])
                    
                    outliers = DataValidator.detect_outliers(
                        df, selected_col, 
                        method='iqr' if method == 'IQR' else 'zscore'
                    )
                    
                    outlier_count = outliers.sum()
                    outlier_pct = (outlier_count / len(df)) * 100
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Outliers Found", outlier_count)
                    with col2:
                        st.metric("Outlier Percentage", f"{outlier_pct:.2f}%")
                    
                    if outlier_count > 0:
                        with st.expander("View outlier values"):
                            st.dataframe(df[outliers][[selected_col]], use_container_width=True)
            
            with tab4:
                st.markdown("### 🧹 Data Cleaning Options")
                
                st.info("Apply cleaning operations to your dataset")
                
                # Missing data handling
                st.markdown("#### Handle Missing Data")
                
                missing_action = st.radio(
                    "Choose action",
                    ["None", "Drop rows with missing values", "Fill missing values"]
                )
                
                if missing_action == "Fill missing values":
                    fill_method = st.selectbox(
                        "Fill method",
                        ["Mean (numeric)", "Median (numeric)", "Mode (all)", "Forward fill", "Backward fill", "Custom value"]
                    )
                
                # Duplicate handling
                st.markdown("#### Handle Duplicates")
                remove_duplicates = st.checkbox("Remove duplicate rows")
                
                # Apply cleaning
                if st.button("Apply Cleaning Operations", type="primary"):
                    df_cleaned = df.copy()
                    
                    # Handle missing data
                    if missing_action == "Drop rows with missing values":
                        df_cleaned = df_cleaned.dropna()
                        st.success(f"Dropped {len(df) - len(df_cleaned)} rows with missing values")
                    elif missing_action == "Fill missing values":
                        if fill_method == "Mean (numeric)":
                            df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(
                                df_cleaned[numeric_cols].mean()
                            )
                        elif fill_method == "Median (numeric)":
                            df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(
                                df_cleaned[numeric_cols].median()
                            )
                        elif fill_method == "Mode (all)":
                            for col in df_cleaned.columns:
                                df_cleaned[col].fillna(df_cleaned[col].mode()[0], inplace=True)
                        elif fill_method == "Forward fill":
                            df_cleaned = df_cleaned.fillna(method='ffill')
                        elif fill_method == "Backward fill":
                            df_cleaned = df_cleaned.fillna(method='bfill')
                        
                        st.success("Filled missing values")
                    
                    # Handle duplicates
                    if remove_duplicates:
                        before_dup = len(df_cleaned)
                        df_cleaned = df_cleaned.drop_duplicates()
                        st.success(f"Removed {before_dup - len(df_cleaned)} duplicate rows")
                    
                    # Show cleaned data
                    st.markdown("#### Cleaned Data Preview")
                    st.dataframe(df_cleaned.head(20), use_container_width=True)
                    
                    # Store in session state for export
                    st.session_state['cleaned_data'] = df_cleaned
                    st.success("✅ Cleaned data is ready for export!")
            
            with tab5:
                st.markdown("### 💾 Export Data")
                
                # Choose data to export
                export_choice = st.radio(
                    "Choose data to export",
                    ["Original data", "Cleaned data (if available)"]
                )
                
                if export_choice == "Cleaned data (if available)":
                    if 'cleaned_data' in st.session_state:
                        export_df = st.session_state['cleaned_data']
                        st.success("Exporting cleaned data")
                    else:
                        export_df = df
                        st.warning("No cleaned data available. Exporting original data.")
                else:
                    export_df = df
                
                # Export format
                export_format = st.selectbox("Export format", ["CSV", "Excel", "JSON"])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if export_format == "CSV":
                        csv = export_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name="exported_data.csv",
                            mime="text/csv"
                        )
                    
                    elif export_format == "Excel":
                        import io
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            export_df.to_excel(writer, index=False, sheet_name='Data')
                        
                        st.download_button(
                            label="📥 Download Excel",
                            data=buffer.getvalue(),
                            file_name="exported_data.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    elif export_format == "JSON":
                        json_str = export_df.to_json(orient='records', indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name="exported_data.json",
                            mime="application/json"
                        )
                
                with col2:
                    st.markdown("#### Export Info")
                    st.metric("Rows", len(export_df))
                    st.metric("Columns", len(export_df.columns))
                    st.metric("Size", f"{export_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.info("Please check your file format and try again.")
    
    else:
        # Show instructions when no file is uploaded
        st.markdown("""
        ## 📚 How to Use
        
        1. **Upload Your Data**: Click the file uploader above and select your data file
        2. **Explore**: Use the tabs to explore different aspects of your data
        3. **Clean**: Apply cleaning operations if needed
        4. **Export**: Download your processed data
        
        ### Supported File Formats
        
        - **CSV** (.csv): Comma-separated values
        - **Excel** (.xlsx): Microsoft Excel format
        - **JSON** (.json): JavaScript Object Notation
        
        ### Tips
        
        - Ensure your data has column headers
        - Check for encoding issues (UTF-8 recommended)
        - Large files may take longer to process
        - Use the Data Cleaning tab to prepare your data for visualization
        """)


if __name__ == "__main__":
    main()
