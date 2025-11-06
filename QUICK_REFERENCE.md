# 🎯 Quick Reference Guide

## 🚀 Quick Start Commands

### First Time Setup

```bash
# Make scripts executable (macOS/Linux)
chmod +x setup.sh run.sh

# Run setup
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Running the App

```bash
# Quick run
./run.sh

# Or manually:
source venv/bin/activate
streamlit run app.py
```

### Running Examples

```bash
source venv/bin/activate
python example_usage.py
```

## 📊 Available Visualizations

### Distribution Plots

- **Histogram with KDE**: `SeabornPlots.distribution_plot()`
- **Box Plot**: `SeabornPlots.box_plot()`
- **Violin Plot**: `SeabornPlots.violin_plot()`
- **KDE Plot**: `SeabornPlots.kde_plot()`
- **ECDF Plot**: `SeabornPlots.ecdf_plot()`
- **Rug Plot**: `SeabornPlots.rug_plot()`

### Categorical Plots

- **Bar Plot**: `SeabornPlots.bar_plot()`
- **Count Plot**: `SeabornPlots.count_plot()`
- **Point Plot**: `SeabornPlots.point_plot()`
- **Strip Plot**: `SeabornPlots.strip_plot()`
- **Swarm Plot**: `SeabornPlots.swarm_plot()`

### Relationship Plots

- **Scatter Plot**: `SeabornPlots.scatter_plot()`
- **Line Plot**: `SeabornPlots.line_plot()`
- **Regression Plot**: `SeabornPlots.regression_plot()`
- **Residual Plot**: `SeabornPlots.residual_plot()`

### Matrix Plots

- **Heatmap**: `SeabornPlots.heatmap()`
- **Correlation Matrix**: `DataProcessor.correlation_matrix()`

### Multi-Plot Grids

- **Pair Plot**: `SeabornPlots.pair_plot()`
- **Joint Plot**: `SeabornPlots.joint_plot()`
- **Facet Grid**: `SeabornPlots.facet_grid()`
- **LM Plot**: `SeabornPlots.lm_plot()`

## 🔧 Common Code Snippets

### Load Data

```python
from utils import DataLoader

# Load sample dataset
df = DataLoader.load_sample_dataset('iris')

# Load CSV
df = DataLoader.load_csv('data/myfile.csv')

# Load Excel
df = DataLoader.load_excel('data/myfile.xlsx')
```

### Process Data

```python
from utils import DataProcessor

# Get column types
numeric_cols = DataProcessor.get_numeric_columns(df)
categorical_cols = DataProcessor.get_categorical_columns(df)

# Get statistics
stats = DataProcessor.get_statistics(df)

# Calculate correlation
corr = DataProcessor.correlation_matrix(df, method='pearson')

# Clean data
df_clean = DataProcessor.clean_data(
    df,
    drop_na=True,
    drop_duplicates=True
)
```

### Create Visualizations

```python
from utils import SeabornPlots, VisualizationManager
import matplotlib.pyplot as plt

# Initialize visualization settings
viz = VisualizationManager(style='darkgrid', palette='husl')

# Create scatter plot
fig = SeabornPlots.scatter_plot(
    df,
    x='column1',
    y='column2',
    hue='category',
    figsize=(10, 6)
)

# Show plot
plt.show()

# Save plot
plt.savefig('output.png', dpi=300, bbox_inches='tight')
```

### Use Components in Streamlit

```python
import streamlit as st
from components import render_header, render_dataframe_explorer

# Render header
render_header("My Page", "Description", "📊")

# Render data explorer
render_dataframe_explorer(df)
```

## 📁 File Structure Quick Reference

```
app.py                  # Main entry point
config.py              # Configuration
requirements.txt       # Dependencies

utils/
  ├── data_loader.py   # Data loading
  ├── visualization.py # Plotting functions
  └── security.py      # Security utilities

components/
  └── ui_components.py # UI components

pages/
  ├── 1_📊_Distribution_Plots.py
  ├── 2_📈_Categorical_Plots.py
  ├── 3_🔗_Relationship_Plots.py
  ├── 4_🔲_Matrix_Plots.py
  ├── 5_🎛️_Multi_Plot_Grids.py
  └── 6_📁_Data_Upload_&_Analysis.py
```

## 🎨 Customization

### Change Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#FF6B6B"
backgroundColor="#0E1117"
secondaryBackgroundColor="#262730"
textColor="#FAFAFA"
```

### Change Default Plot Settings

Edit `config.py`:

```python
VIZ_CONFIG = {
    "style": "darkgrid",      # or: whitegrid, dark, white, ticks
    "palette": "husl",        # or: deep, muted, bright, pastel, dark
    "context": "notebook",    # or: paper, talk, poster
    "font_scale": 1.2,
}
```

## 🐛 Troubleshooting

### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Large Dataset Issues

- Sample data: `df.sample(n=1000)`
- Use chunks: `pd.read_csv('file.csv', chunksize=10000)`
- Filter data before plotting

### Memory Issues

- Close unused plots: `plt.close()`
- Clear cache: `st.cache_data.clear()`
- Use smaller datasets

## 📚 Useful Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Seaborn Gallery](https://seaborn.pydata.org/examples/index.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)

## 🔑 Environment Variables

Create `.env` file:

```bash
APP_TITLE=My Dashboard
APP_ICON=📊
DEBUG_MODE=False
SECRET_KEY=your_secret_key_here
```

## 💡 Pro Tips

1. **Use caching for expensive operations**

   ```python
   @st.cache_data
   def load_data():
       return pd.read_csv('large_file.csv')
   ```

2. **Sample large datasets**

   ```python
   if len(df) > 10000:
       df = df.sample(n=10000, random_state=42)
   ```

3. **Handle errors gracefully**

   ```python
   try:
       # Your code
   except Exception as e:
       st.error(f"Error: {str(e)}")
   ```

4. **Use progress indicators**

   ```python
   with st.spinner("Loading..."):
       # Long operation
   ```

5. **Export high-quality plots**
   ```python
   fig.savefig('plot.png', dpi=300, bbox_inches='tight')
   ```

## 🎯 Best Practices

✅ **Do:**

- Use descriptive variable names
- Add docstrings to functions
- Handle errors appropriately
- Validate user input
- Use type hints
- Keep functions small and focused

❌ **Don't:**

- Hard-code sensitive information
- Ignore error handling
- Create overly complex functions
- Forget to close plots
- Neglect data validation

---

**Need Help?** Check README.md and DOCUMENTATION.md for detailed information.
