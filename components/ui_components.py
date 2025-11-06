"""
Reusable Streamlit components
"""
import streamlit as st
import pandas as pd
from typing import Optional, List, Dict, Any
import plotly.graph_objects as go


def render_header(title: str, subtitle: Optional[str] = None, icon: str = "📊"):
    """Render a consistent header across pages"""
    st.markdown(
        f"""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #FF6B6B;'>{icon} {title}</h1>
            {f"<p style='font-size: 1.2rem; color: #888;'>{subtitle}</p>" if subtitle else ""}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_card(title: str, content: Any, icon: str = "📌"):
    """Render a card component"""
    st.markdown(
        f"""
        <div style='background-color: #262730; padding: 1.5rem; border-radius: 10px; 
                    margin: 1rem 0; border-left: 5px solid #FF6B6B;'>
            <h3>{icon} {title}</h3>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_metric_card(label: str, value: Any, delta: Optional[str] = None, 
                      icon: str = "📈"):
    """Render a metric card"""
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<div style='font-size: 3rem;'>{icon}</div>", 
                   unsafe_allow_html=True)
    with col2:
        st.metric(label=label, value=value, delta=delta)


def render_sidebar_info(config: Dict[str, Any]):
    """Render sidebar information"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info(
            "This is a professional data visualization dashboard "
            "built with Streamlit, Seaborn, and Matplotlib."
        )
        
        if config:
            with st.expander("📋 Configuration"):
                for key, value in config.items():
                    st.text(f"{key}: {value}")


def render_data_selector(datasets: List[str]) -> str:
    """Render dataset selector"""
    st.sidebar.markdown("### 📂 Dataset Selection")
    selected = st.sidebar.selectbox(
        "Choose a dataset",
        options=datasets,
        help="Select a dataset to visualize"
    )
    return selected


def render_column_selector(df: pd.DataFrame, 
                          selection_type: str = "single",
                          numeric_only: bool = False,
                          label: str = "Select Column") -> Any:
    """Render column selector"""
    columns = df.columns.tolist()
    
    if numeric_only:
        columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if selection_type == "single":
        return st.selectbox(label, columns)
    elif selection_type == "multi":
        return st.multiselect(label, columns)
    else:
        return st.radio(label, columns)


def render_filter_panel(df: pd.DataFrame, column: str) -> List[Any]:
    """Render filter panel for a column"""
    unique_values = df[column].unique().tolist()
    
    if len(unique_values) <= 20:
        selected = st.multiselect(
            f"Filter by {column}",
            options=unique_values,
            default=unique_values
        )
    else:
        selected = unique_values
        st.info(f"Too many unique values ({len(unique_values)}) to show filter")
    
    return selected


def render_plot_controls(plot_type: str) -> Dict[str, Any]:
    """Render plot control panel"""
    controls = {}
    
    with st.expander("🎨 Plot Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            controls['figsize_width'] = st.slider("Figure Width", 6, 20, 12)
            controls['style'] = st.selectbox(
                "Style", 
                ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']
            )
        
        with col2:
            controls['figsize_height'] = st.slider("Figure Height", 4, 16, 6)
            controls['palette'] = st.selectbox(
                "Color Palette",
                ['husl', 'deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind']
            )
        
        if plot_type in ['scatter', 'line']:
            controls['alpha'] = st.slider("Transparency", 0.1, 1.0, 0.6)
        
        if plot_type == 'histogram':
            controls['bins'] = st.slider("Number of Bins", 10, 100, 30)
            controls['kde'] = st.checkbox("Show KDE", value=True)
    
    return controls


def render_download_button(fig, filename: str = "plot.png"):
    """Render download button for plot"""
    import io
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    
    st.download_button(
        label="📥 Download Plot",
        data=buf,
        file_name=filename,
        mime="image/png"
    )


def render_dataframe_explorer(df: pd.DataFrame):
    """Render interactive dataframe explorer"""
    st.markdown("### 🔍 Data Explorer")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Preview", "📈 Statistics", "🔎 Info", "🧹 Quality"])
    
    with tab1:
        st.dataframe(df.head(100), use_container_width=True)
        st.caption(f"Showing first 100 rows of {len(df)} total rows")
    
    with tab2:
        st.dataframe(df.describe(), use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rows", df.shape[0])
            st.metric("Columns", df.shape[1])
        with col2:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            st.metric("Duplicates", df.duplicated().sum())
        
        st.markdown("#### Column Types")
        st.dataframe(
            pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.values,
                'Non-Null': df.count().values,
                'Null': df.isnull().sum().values
            }),
            use_container_width=True
        )
    
    with tab4:
        st.markdown("#### Missing Data")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing Count': missing.values,
            'Missing %': missing_pct.values
        }).sort_values('Missing Count', ascending=False)
        
        st.dataframe(missing_df, use_container_width=True)


def render_notification(message: str, type: str = "info"):
    """Render notification"""
    if type == "success":
        st.success(message)
    elif type == "error":
        st.error(message)
    elif type == "warning":
        st.warning(message)
    else:
        st.info(message)


def render_loading_animation(text: str = "Loading..."):
    """Render loading animation"""
    return st.spinner(text)


def render_progress_bar(progress: float, text: str = ""):
    """Render progress bar"""
    st.progress(progress, text=text)


def render_code_block(code: str, language: str = "python"):
    """Render code block"""
    st.code(code, language=language)


def render_collapsible_section(title: str, content: Any, expanded: bool = False):
    """Render collapsible section"""
    with st.expander(title, expanded=expanded):
        st.write(content)


def render_tabs(tabs: Dict[str, Any]):
    """Render tabs with content"""
    tab_objects = st.tabs(list(tabs.keys()))
    
    for tab_obj, (tab_name, content) in zip(tab_objects, tabs.items()):
        with tab_obj:
            if callable(content):
                content()
            else:
                st.write(content)


def render_columns(num_cols: int, contents: List[Any]):
    """Render columns with content"""
    cols = st.columns(num_cols)
    
    for col, content in zip(cols, contents):
        with col:
            if callable(content):
                content()
            else:
                st.write(content)


class DataUploader:
    """Component for uploading data"""
    
    @staticmethod
    def render(accepted_types: List[str] = None):
        """Render file uploader"""
        if accepted_types is None:
            accepted_types = ['csv', 'xlsx', 'json']
        
        st.markdown("### 📁 Upload Your Data")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=accepted_types,
            help=f"Supported formats: {', '.join(accepted_types)}"
        )
        
        return uploaded_file


class PlotExporter:
    """Component for exporting plots"""
    
    @staticmethod
    def render(fig, formats: List[str] = None):
        """Render export options"""
        if formats is None:
            formats = ['png', 'pdf', 'svg']
        
        st.markdown("### 💾 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            format_choice = st.selectbox("Format", formats)
        
        with col2:
            dpi = st.number_input("DPI", min_value=72, max_value=600, value=300)
        
        if st.button("Export Plot"):
            import io
            buf = io.BytesIO()
            fig.savefig(buf, format=format_choice, dpi=dpi, bbox_inches='tight')
            buf.seek(0)
            
            st.download_button(
                label=f"📥 Download {format_choice.upper()}",
                data=buf,
                file_name=f"plot.{format_choice}",
                mime=f"image/{format_choice}"
            )
