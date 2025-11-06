"""
Visualization utilities
Comprehensive plotting functions using Seaborn and Matplotlib
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Tuple, List, Any
import warnings
warnings.filterwarnings('ignore')


class VisualizationManager:
    """Manage visualization settings and styles"""
    
    def __init__(self, style: str = 'darkgrid', palette: str = 'husl', 
                 context: str = 'notebook', font_scale: float = 1.2):
        self.style = style
        self.palette = palette
        self.context = context
        self.font_scale = font_scale
        self.apply_settings()
    
    def apply_settings(self):
        """Apply visualization settings"""
        sns.set_style(self.style)
        sns.set_palette(self.palette)
        sns.set_context(self.context, font_scale=self.font_scale)
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['figure.dpi'] = 100
    
    def get_color_palette(self, n_colors: int = 10) -> list:
        """Get color palette"""
        return sns.color_palette(self.palette, n_colors)


class SeabornPlots:
    """Collection of Seaborn plot functions"""
    
    @staticmethod
    def distribution_plot(data: pd.DataFrame, column: str, 
                         kde: bool = True, bins: int = 30,
                         figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create distribution plot (histogram with KDE)"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.histplot(data=data, x=column, kde=kde, bins=bins, ax=ax)
        ax.set_title(f'Distribution of {column}', fontsize=14, fontweight='bold')
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def box_plot(data: pd.DataFrame, x: Optional[str] = None, y: str = None,
                figsize: Tuple[int, int] = (10, 6), hue: Optional[str] = None) -> plt.Figure:
        """Create box plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.boxplot(data=data, x=x, y=y, hue=hue, ax=ax)
        ax.set_title(f'Box Plot: {y}', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def violin_plot(data: pd.DataFrame, x: Optional[str] = None, y: str = None,
                   figsize: Tuple[int, int] = (10, 6), hue: Optional[str] = None) -> plt.Figure:
        """Create violin plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.violinplot(data=data, x=x, y=y, hue=hue, ax=ax)
        ax.set_title(f'Violin Plot: {y}', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def scatter_plot(data: pd.DataFrame, x: str, y: str,
                    hue: Optional[str] = None, size: Optional[str] = None,
                    figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create scatter plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.scatterplot(data=data, x=x, y=y, hue=hue, size=size, ax=ax, alpha=0.6)
        ax.set_title(f'Scatter Plot: {x} vs {y}', fontsize=14, fontweight='bold')
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel(y, fontsize=12)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def line_plot(data: pd.DataFrame, x: str, y: str,
                 hue: Optional[str] = None, style: Optional[str] = None,
                 figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """Create line plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.lineplot(data=data, x=x, y=y, hue=hue, style=style, ax=ax, marker='o')
        ax.set_title(f'Line Plot: {x} vs {y}', fontsize=14, fontweight='bold')
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel(y, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def bar_plot(data: pd.DataFrame, x: str, y: str,
                hue: Optional[str] = None, estimator=np.mean,
                figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create bar plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.barplot(data=data, x=x, y=y, hue=hue, estimator=estimator, ax=ax)
        ax.set_title(f'Bar Plot: {x} vs {y}', fontsize=14, fontweight='bold')
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel(y, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def count_plot(data: pd.DataFrame, x: str, hue: Optional[str] = None,
                  figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create count plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.countplot(data=data, x=x, hue=hue, ax=ax)
        ax.set_title(f'Count Plot: {x}', fontsize=14, fontweight='bold')
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def heatmap(data: pd.DataFrame, annot: bool = True, fmt: str = '.2f',
               cmap: str = 'coolwarm', figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """Create heatmap"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.heatmap(data, annot=annot, fmt=fmt, cmap=cmap, 
                   center=0, square=True, linewidths=1, ax=ax)
        ax.set_title('Heatmap', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def pair_plot(data: pd.DataFrame, hue: Optional[str] = None,
                 vars: Optional[List[str]] = None,
                 figsize: Tuple[int, int] = (12, 12)) -> sns.PairGrid:
        """Create pair plot"""
        if vars:
            plot = sns.pairplot(data[vars + ([hue] if hue else [])], 
                              hue=hue, diag_kind='kde', corner=False)
        else:
            plot = sns.pairplot(data, hue=hue, diag_kind='kde', corner=False)
        plot.fig.suptitle('Pair Plot', y=1.01, fontsize=14, fontweight='bold')
        return plot
    
    @staticmethod
    def joint_plot(data: pd.DataFrame, x: str, y: str,
                  kind: str = 'scatter', hue: Optional[str] = None,
                  figsize: Tuple[int, int] = (10, 10)) -> sns.JointGrid:
        """Create joint plot"""
        plot = sns.jointplot(data=data, x=x, y=y, kind=kind, hue=hue, height=10)
        plot.fig.suptitle(f'Joint Plot: {x} vs {y}', y=1.01, fontsize=14, fontweight='bold')
        return plot
    
    @staticmethod
    def regression_plot(data: pd.DataFrame, x: str, y: str,
                       figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create regression plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.regplot(data=data, x=x, y=y, ax=ax, scatter_kws={'alpha': 0.5})
        ax.set_title(f'Regression Plot: {x} vs {y}', fontsize=14, fontweight='bold')
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel(y, fontsize=12)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def cat_plot(data: pd.DataFrame, x: str, y: str, 
                kind: str = 'strip', hue: Optional[str] = None,
                col: Optional[str] = None, row: Optional[str] = None,
                figsize: Tuple[int, int] = (12, 6)) -> sns.FacetGrid:
        """Create categorical plot"""
        plot = sns.catplot(data=data, x=x, y=y, kind=kind, 
                          hue=hue, col=col, row=row, height=6, aspect=1.5)
        plot.fig.suptitle(f'Categorical Plot: {kind}', y=1.01, fontsize=14, fontweight='bold')
        return plot
    
    @staticmethod
    def facet_grid(data: pd.DataFrame, row: Optional[str] = None, 
                  col: Optional[str] = None, hue: Optional[str] = None,
                  plot_type: str = 'scatter', x: str = None, y: str = None,
                  figsize: Tuple[int, int] = (12, 8)) -> sns.FacetGrid:
        """Create facet grid"""
        g = sns.FacetGrid(data, row=row, col=col, hue=hue, height=4, aspect=1.5)
        
        if plot_type == 'scatter':
            g.map(plt.scatter, x, y, alpha=0.6)
        elif plot_type == 'hist':
            g.map(plt.hist, x, bins=20, alpha=0.6)
        elif plot_type == 'kde':
            g.map(sns.kdeplot, x, shade=True)
        
        g.add_legend()
        g.fig.suptitle('Facet Grid', y=1.01, fontsize=14, fontweight='bold')
        return g
    
    @staticmethod
    def swarm_plot(data: pd.DataFrame, x: str, y: str,
                  hue: Optional[str] = None,
                  figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create swarm plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.swarmplot(data=data, x=x, y=y, hue=hue, ax=ax)
        ax.set_title(f'Swarm Plot: {x} vs {y}', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def strip_plot(data: pd.DataFrame, x: str, y: str,
                  hue: Optional[str] = None,
                  figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create strip plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.stripplot(data=data, x=x, y=y, hue=hue, ax=ax, alpha=0.6)
        ax.set_title(f'Strip Plot: {x} vs {y}', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def point_plot(data: pd.DataFrame, x: str, y: str,
                  hue: Optional[str] = None,
                  figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create point plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.pointplot(data=data, x=x, y=y, hue=hue, ax=ax)
        ax.set_title(f'Point Plot: {x} vs {y}', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def lm_plot(data: pd.DataFrame, x: str, y: str,
               hue: Optional[str] = None, col: Optional[str] = None,
               figsize: Tuple[int, int] = (12, 6)) -> sns.FacetGrid:
        """Create regression plot with facets"""
        plot = sns.lmplot(data=data, x=x, y=y, hue=hue, col=col, 
                         height=6, aspect=1.5, scatter_kws={'alpha': 0.5})
        plot.fig.suptitle(f'LM Plot: {x} vs {y}', y=1.01, fontsize=14, fontweight='bold')
        return plot
    
    @staticmethod
    def residual_plot(data: pd.DataFrame, x: str, y: str,
                     figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create residual plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.residplot(data=data, x=x, y=y, ax=ax, scatter_kws={'alpha': 0.5})
        ax.set_title(f'Residual Plot: {x} vs {y}', fontsize=14, fontweight='bold')
        ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def kde_plot(data: pd.DataFrame, x: str, y: Optional[str] = None,
                hue: Optional[str] = None, fill: bool = True,
                figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create KDE plot"""
        fig, ax = plt.subplots(figsize=figsize)
        if y:
            sns.kdeplot(data=data, x=x, y=y, hue=hue, fill=fill, ax=ax)
            title = f'KDE Plot: {x} vs {y}'
        else:
            sns.kdeplot(data=data, x=x, hue=hue, fill=fill, ax=ax)
            title = f'KDE Plot: {x}'
        ax.set_title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def ecdf_plot(data: pd.DataFrame, x: str, hue: Optional[str] = None,
                 figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create ECDF plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.ecdfplot(data=data, x=x, hue=hue, ax=ax)
        ax.set_title(f'ECDF Plot: {x}', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def rug_plot(data: pd.DataFrame, x: str, hue: Optional[str] = None,
                figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """Create rug plot"""
        fig, ax = plt.subplots(figsize=figsize)
        sns.rugplot(data=data, x=x, hue=hue, ax=ax, height=0.5)
        ax.set_title(f'Rug Plot: {x}', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig
