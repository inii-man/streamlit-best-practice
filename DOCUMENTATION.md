# 📝 Documentation

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module Documentation](#module-documentation)
3. [API Reference](#api-reference)
4. [Security Guidelines](#security-guidelines)
5. [Deployment Guide](#deployment-guide)

## Architecture Overview

### Application Flow

```
User → Streamlit UI → Components → Utils → Data Processing → Visualization
                           ↓
                    Configuration Management
                           ↓
                    Security & Validation
```

### Design Patterns

1. **Separation of Concerns**

   - `utils/`: Business logic and data processing
   - `components/`: UI components
   - `pages/`: Page-specific logic
   - `config.py`: Configuration management

2. **Single Responsibility**

   - Each module has a single, well-defined purpose
   - Functions do one thing well
   - Easy to test and maintain

3. **DRY (Don't Repeat Yourself)**
   - Reusable components
   - Shared utilities
   - Configuration centralization

## Module Documentation

### config.py

Central configuration management module.

**Classes:**

- `Config`: Main configuration class with application settings

**Key Features:**

- Environment variable loading
- Path management
- Application settings
- Visualization defaults
- Page configuration

**Usage:**

```python
from config import Config

# Access settings
app_title = Config.APP_TITLE
data_dir = Config.DATA_DIR

# Get all config
config_dict = Config.get_config()
```

### utils/data_loader.py

Data loading and processing utilities.

**Classes:**

- `DataLoader`: Load data from various sources
- `DataProcessor`: Process and transform data
- `DataValidator`: Validate data quality

**Key Methods:**

**DataLoader:**

- `load_csv()`: Load CSV files
- `load_excel()`: Load Excel files
- `load_json()`: Load JSON files
- `load_sample_dataset()`: Load Seaborn datasets
- `get_available_datasets()`: List available datasets

**DataProcessor:**

- `get_basic_info()`: Get DataFrame information
- `get_numeric_columns()`: Get numeric column list
- `get_categorical_columns()`: Get categorical column list
- `clean_data()`: Clean DataFrame
- `get_statistics()`: Calculate statistics
- `correlation_matrix()`: Calculate correlations
- `pivot_table()`: Create pivot tables

**DataValidator:**

- `check_missing_data()`: Check for missing values
- `check_duplicates()`: Check for duplicates
- `detect_outliers()`: Detect outliers (IQR or Z-score)

**Usage:**

```python
from utils import DataLoader, DataProcessor

# Load data
df = DataLoader.load_sample_dataset('iris')

# Process data
numeric_cols = DataProcessor.get_numeric_columns(df)
stats = DataProcessor.get_statistics(df)
corr = DataProcessor.correlation_matrix(df)
```

### utils/visualization.py

Comprehensive visualization utilities.

**Classes:**

- `VisualizationManager`: Manage visualization settings
- `SeabornPlots`: Collection of plot functions

**Plot Types Available:**

**Distribution Plots:**

- `distribution_plot()`: Histogram with KDE
- `box_plot()`: Box plot
- `violin_plot()`: Violin plot
- `kde_plot()`: KDE plot
- `ecdf_plot()`: ECDF plot
- `rug_plot()`: Rug plot

**Categorical Plots:**

- `bar_plot()`: Bar plot
- `count_plot()`: Count plot
- `point_plot()`: Point plot
- `strip_plot()`: Strip plot
- `swarm_plot()`: Swarm plot

**Relationship Plots:**

- `scatter_plot()`: Scatter plot
- `line_plot()`: Line plot
- `regression_plot()`: Regression plot
- `residual_plot()`: Residual plot

**Matrix Plots:**

- `heatmap()`: Heatmap

**Multi-Plot:**

- `pair_plot()`: Pair plot
- `joint_plot()`: Joint plot
- `facet_grid()`: Facet grid
- `cat_plot()`: Categorical plot
- `lm_plot()`: Regression facet plot

**Usage:**

```python
from utils import VisualizationManager, SeabornPlots
import matplotlib.pyplot as plt

# Initialize
viz = VisualizationManager(style='darkgrid', palette='husl')

# Create plot
fig = SeabornPlots.scatter_plot(df, x='col1', y='col2', hue='category')
plt.show()
```

### utils/security.py

Security and session management.

**Classes:**

- `SecurityManager`: Handle security operations
- `SessionManager`: Manage Streamlit sessions

**Functions:**

- `sanitize_input()`: Sanitize user input
- `validate_file_upload()`: Validate uploaded files

**Usage:**

```python
from utils import SecurityManager, SessionManager, sanitize_input

# Security
security = SecurityManager()
encrypted = security.encrypt("sensitive data")
token = security.generate_token()

# Session
SessionManager.init_session_state(st, {'key': 'value'})
value = SessionManager.get_session_value(st, 'key')

# Input validation
clean_input = sanitize_input(user_input)
```

### components/ui_components.py

Reusable UI components.

**Functions:**

- `render_header()`: Render page header
- `render_card()`: Render card component
- `render_metric_card()`: Render metric card
- `render_sidebar_info()`: Render sidebar information
- `render_data_selector()`: Render dataset selector
- `render_column_selector()`: Render column selector
- `render_plot_controls()`: Render plot controls
- `render_dataframe_explorer()`: Render data explorer
- `render_notification()`: Render notifications

**Classes:**

- `DataUploader`: File upload component
- `PlotExporter`: Plot export component

**Usage:**

```python
from components import render_header, render_dataframe_explorer

# Render header
render_header("My Page", "Subtitle", "📊")

# Render data explorer
render_dataframe_explorer(df)
```

## API Reference

### Configuration API

```python
class Config:
    # Paths
    BASE_DIR: Path
    DATA_DIR: Path
    ASSETS_DIR: Path

    # App Settings
    APP_TITLE: str
    APP_ICON: str
    DEBUG_MODE: bool

    # Security
    SECRET_KEY: str

    # Methods
    @classmethod
    def get_config() -> Dict[str, Any]

    @classmethod
    def ensure_directories()
```

### Data Loading API

```python
class DataLoader:
    @staticmethod
    def load_csv(file_path, **kwargs) -> pd.DataFrame

    @staticmethod
    def load_excel(file_path, **kwargs) -> pd.DataFrame

    @staticmethod
    def load_json(file_path, **kwargs) -> pd.DataFrame

    @staticmethod
    def load_sample_dataset(dataset_name: str) -> pd.DataFrame

    @staticmethod
    def get_available_datasets() -> list
```

### Visualization API

```python
class SeabornPlots:
    @staticmethod
    def scatter_plot(
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: Optional[str] = None,
        size: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure

    # Similar signature for other plot types...
```

## Security Guidelines

### Environment Variables

1. **Never commit `.env` file**

   - Use `.env.example` as template
   - Add `.env` to `.gitignore`

2. **Use strong secrets**

   ```bash
   # Generate strong secret key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Rotate keys regularly**
   - Change API keys periodically
   - Update secret keys

### Input Validation

Always validate user input:

```python
from utils import sanitize_input, validate_file_upload

# Sanitize text input
clean_input = sanitize_input(user_input)

# Validate file upload
is_valid, message = validate_file_upload(uploaded_file)
if not is_valid:
    st.error(message)
```

### File Upload Security

- Validate file extensions
- Check file size limits
- Scan for malicious content
- Use temporary storage
- Clean up after processing

## Deployment Guide

### Local Deployment

Already covered in README.md Quick Start section.

### Cloud Deployment

#### Streamlit Cloud

1. **Prepare repository**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**

   - Go to https://share.streamlit.io/
   - Connect your GitHub repository
   - Select branch and main file (`app.py`)
   - Add secrets in the dashboard
   - Deploy!

3. **Configure secrets**
   - In Streamlit Cloud dashboard
   - Add secrets from `.streamlit/secrets.toml`
   - Save and redeploy

#### Heroku

1. **Create `Procfile`**

   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. **Create `setup.sh`**

   ```bash
   mkdir -p ~/.streamlit/

   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

#### Docker

1. **Create `Dockerfile`**

   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t viz-dashboard .
   docker run -p 8501:8501 viz-dashboard
   ```

### Production Considerations

1. **Performance**

   - Enable caching with `@st.cache_data`
   - Optimize data loading
   - Use data sampling for large datasets

2. **Monitoring**

   - Set up error tracking
   - Monitor resource usage
   - Track user analytics

3. **Backup**

   - Regular database backups
   - Version control
   - Document recovery procedures

4. **Security**
   - Use HTTPS
   - Enable authentication if needed
   - Regular security audits
   - Keep dependencies updated

---

For more information, consult the official documentation:

- [Streamlit Docs](https://docs.streamlit.io/)
- [Seaborn Docs](https://seaborn.pydata.org/)
- [Pandas Docs](https://pandas.pydata.org/docs/)
