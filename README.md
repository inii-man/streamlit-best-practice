# 📊 Professional Seaborn Visualization Dashboard

A comprehensive, production-ready data visualization dashboard built with Streamlit, Seaborn, and Matplotlib. This project follows best practices for Python application development with a focus on security, modularity, and professional code organization.

## ✨ Features

### 🎨 Visualization Types

- **Distribution Plots**: Histograms, KDE, Box plots, Violin plots, ECDF, Rug plots
- **Categorical Plots**: Bar plots, Count plots, Point plots, Strip plots, Swarm plots
- **Relationship Plots**: Scatter plots, Line plots, Regression plots, Residual plots
- **Matrix Plots**: Correlation heatmaps, Custom heatmaps, Pivot table heatmaps, Clustermaps
- **Multi-Plot Grids**: Pair plots, Joint plots, Facet grids, LM plots
- **Data Analysis**: Upload, explore, clean, and export your data

### 🔒 Security Features

- Environment variable management with `.env` files
- Secrets management with Streamlit secrets
- Input sanitization and validation
- Secure file upload handling
- API key encryption utilities

### 🏗️ Architecture

- **Modular Design**: Separated concerns with utils, components, and pages
- **Reusable Components**: Custom UI components for consistency
- **Configuration Management**: Centralized config with environment-based settings
- **Error Handling**: Comprehensive error handling and user feedback
- **Type Hints**: Full type annotations for better code quality

## 📁 Project Structure

```
4/
├── app.py                          # Main application entry point
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
│
├── .streamlit/                     # Streamlit configuration
│   ├── config.toml                 # Theme and server settings
│   └── secrets.toml.example        # Secrets template
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── data_loader.py             # Data loading and processing
│   ├── visualization.py           # Seaborn plot functions
│   └── security.py                # Security utilities
│
├── components/                     # Reusable UI components
│   ├── __init__.py
│   └── ui_components.py           # Streamlit components
│
├── pages/                          # Multi-page app pages
│   ├── 1_📊_Distribution_Plots.py
│   ├── 2_📈_Categorical_Plots.py
│   ├── 3_🔗_Relationship_Plots.py
│   ├── 4_🔲_Matrix_Plots.py
│   ├── 5_🎛️_Multi_Plot_Grids.py
│   └── 6_📁_Data_Upload_&_Analysis.py
│
├── data/                           # Data directory (auto-created)
└── assets/                         # Assets directory (auto-created)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project directory**

   ```bash
   cd /Users/sulaimansaleh/Documents/py/4
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   ```bash
   # On macOS/Linux
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Set up Streamlit secrets (optional)**
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit secrets.toml with your secrets
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Data Selection

Choose your data source:

- **Sample Datasets**: Use built-in Seaborn datasets (iris, tips, titanic, etc.)
- **Upload File**: Upload your own CSV, Excel, or JSON file

### 2. Visualization

Navigate through different visualization pages:

- **Distribution Plots**: Analyze single variable distributions
- **Categorical Plots**: Compare categories and groups
- **Relationship Plots**: Explore variable relationships
- **Matrix Plots**: Visualize correlations and patterns
- **Multi-Plot Grids**: Create complex multi-panel visualizations
- **Data Upload & Analysis**: Upload and analyze custom data

### 3. Customization

Each plot offers customization options:

- Figure size and dimensions
- Color palettes and styles
- Axis labels and titles
- Grouping and coloring variables
- Statistical parameters

### 4. Export

Download your visualizations:

- High-resolution PNG images (300+ DPI)
- Multiple format support
- Export cleaned data

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# Application Settings
APP_TITLE=Professional Seaborn Visualization Dashboard
APP_ICON=📊
DEBUG_MODE=False

# Security
SECRET_KEY=your_secret_key_here

# API Keys (if needed)
API_KEY=your_api_key_here

# Database (if needed)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=user
DB_PASSWORD=password
```

### Streamlit Configuration (`.streamlit/config.toml`)

Already configured with:

- Dark theme with custom colors
- Wide layout mode
- CORS and XSRF protection
- Server settings

## 📦 Dependencies

### Core Libraries

- **streamlit**: Web application framework
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **seaborn**: Statistical visualization
- **matplotlib**: Plotting library
- **plotly**: Interactive visualizations

### Utilities

- **python-dotenv**: Environment variable management
- **cryptography**: Security and encryption
- **scipy**: Scientific computing
- **scikit-learn**: Machine learning utilities

See `requirements.txt` for complete list with versions.

## 🏗️ Development

### Best Practices Implemented

1. **Code Organization**

   - Separation of concerns (utils, components, pages)
   - Modular and reusable code
   - Clear naming conventions

2. **Security**

   - Environment-based configuration
   - Secrets management
   - Input validation and sanitization
   - Secure file handling

3. **Documentation**

   - Comprehensive docstrings
   - Type hints throughout
   - README and inline comments

4. **Error Handling**

   - Try-except blocks
   - User-friendly error messages
   - Graceful degradation

5. **Performance**
   - Data sampling for large datasets
   - Lazy loading where possible
   - Efficient data structures

### Adding New Visualizations

1. Create a new file in `pages/` directory:

   ```python
   # pages/7_🎨_Your_New_Plot.py
   import streamlit as st
   from config import Config
   from utils import DataLoader, SeabornPlots

   st.set_page_config(**Config.PAGE_CONFIG)

   def main():
       # Your visualization code here
       pass

   if __name__ == "__main__":
       main()
   ```

2. Add plot function to `utils/visualization.py` if needed

3. Test thoroughly with different datasets

### Adding New Components

Add reusable components to `components/ui_components.py`:

```python
def render_your_component(param1, param2):
    """Component description"""
    # Component code here
    pass
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] All visualization types render correctly
- [ ] File upload works for CSV, Excel, JSON
- [ ] Sample datasets load properly
- [ ] Export functionality works
- [ ] Error messages are clear and helpful
- [ ] Responsive design works on different screen sizes
- [ ] Performance is acceptable with large datasets

### Data Testing

Test with:

- Small datasets (<100 rows)
- Medium datasets (100-10,000 rows)
- Large datasets (>10,000 rows)
- Various data types (numeric, categorical, datetime)
- Data with missing values
- Data with outliers

## 📊 Example Datasets

Built-in Seaborn datasets available:

- `anagrams`: Letter puzzle response times
- `anscombe`: Anscombe's quartet
- `attention`: Attention experiment data
- `brain_networks`: Brain network data
- `car_crashes`: US car crash statistics
- `diamonds`: Diamond prices and characteristics
- `dots`: Visual search experiment
- `exercise`: Exercise and pulse rates
- `flights`: Airline passenger numbers
- `fmri`: fMRI data
- `gammas`: Gamma-ray astronomy data
- `geyser`: Old Faithful geyser data
- `iris`: Iris flower measurements
- `mpg`: Fuel economy data
- `penguins`: Palmer Penguins data
- `planets`: Exoplanet characteristics
- `tips`: Restaurant tipping data
- `titanic`: Titanic passenger survival

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📝 License

This project is provided as-is for educational and professional use.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Seaborn](https://seaborn.pydata.org/) and [Matplotlib](https://matplotlib.org/)
- Data manipulation with [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/)
- Inspired by Seaborn's comprehensive visualization guide

## 📞 Support

For questions or issues:

1. Check the documentation in this README
2. Review code comments and docstrings
3. Check Streamlit and Seaborn documentation
4. Open an issue in the repository

## 🔄 Version History

### Version 1.0.0 (Initial Release)

- Complete visualization suite with 20+ plot types
- Multi-page Streamlit application
- Security features and best practices
- Professional code organization
- Data upload and analysis tools
- Export functionality
- Comprehensive documentation

## 🎯 Future Enhancements

Potential improvements:

- [ ] Add more statistical tests
- [ ] Implement data transformation tools
- [ ] Add plot templates/presets
- [ ] Support for more file formats
- [ ] Database connectivity
- [ ] User authentication
- [ ] Plot comparison views
- [ ] Automated report generation
- [ ] API integration
- [ ] Docker containerization

---

**Built with ❤️ using Streamlit, Seaborn, and Matplotlib**
