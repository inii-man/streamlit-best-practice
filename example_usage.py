"""
Example script showing how to use the visualization utilities programmatically
"""
import pandas as pd
import matplotlib.pyplot as plt
from utils import DataLoader, DataProcessor, SeabornPlots, VisualizationManager

def main():
    """Main example function"""
    
    # Initialize visualization manager
    viz_manager = VisualizationManager(
        style='darkgrid',
        palette='husl',
        context='notebook',
        font_scale=1.2
    )
    
    print("=" * 50)
    print("Seaborn Visualization Examples")
    print("=" * 50)
    print()
    
    # Load sample dataset
    print("Loading sample dataset (iris)...")
    df = DataLoader.load_sample_dataset('iris')
    print(f"✓ Loaded dataset with shape: {df.shape}")
    print()
    
    # Get basic information
    print("Dataset Information:")
    print("-" * 50)
    info = DataProcessor.get_basic_info(df)
    print(f"Shape: {info['shape']}")
    print(f"Columns: {info['columns']}")
    print(f"Memory Usage: {info['memory_usage']:.2f} MB")
    print()
    
    # Get column types
    numeric_cols = DataProcessor.get_numeric_columns(df)
    categorical_cols = DataProcessor.get_categorical_columns(df)
    print(f"Numeric columns: {numeric_cols}")
    print(f"Categorical columns: {categorical_cols}")
    print()
    
    # Create visualizations
    print("Creating visualizations...")
    print("-" * 50)
    
    # 1. Distribution plot
    print("1. Creating distribution plot...")
    fig1 = SeabornPlots.distribution_plot(
        df, 
        column='sepal_length',
        kde=True,
        bins=30
    )
    plt.savefig('assets/example_distribution.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved to: assets/example_distribution.png")
    plt.close()
    
    # 2. Scatter plot
    print("2. Creating scatter plot...")
    fig2 = SeabornPlots.scatter_plot(
        df,
        x='sepal_length',
        y='sepal_width',
        hue='species'
    )
    plt.savefig('assets/example_scatter.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved to: assets/example_scatter.png")
    plt.close()
    
    # 3. Box plot
    print("3. Creating box plot...")
    fig3 = SeabornPlots.box_plot(
        df,
        x='species',
        y='petal_length'
    )
    plt.savefig('assets/example_boxplot.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved to: assets/example_boxplot.png")
    plt.close()
    
    # 4. Correlation heatmap
    print("4. Creating correlation heatmap...")
    corr_matrix = DataProcessor.correlation_matrix(df)
    fig4 = SeabornPlots.heatmap(
        corr_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm'
    )
    plt.savefig('assets/example_heatmap.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved to: assets/example_heatmap.png")
    plt.close()
    
    # 5. Pair plot
    print("5. Creating pair plot...")
    plot = SeabornPlots.pair_plot(df, hue='species')
    plot.fig.savefig('assets/example_pairplot.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved to: assets/example_pairplot.png")
    plt.close()
    
    print()
    print("=" * 50)
    print("All visualizations created successfully!")
    print("Check the 'assets' folder for the generated plots.")
    print("=" * 50)


if __name__ == "__main__":
    main()
