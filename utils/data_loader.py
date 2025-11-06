"""
Data loading and processing utilities
"""
import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path
from typing import Optional, Union, Dict, Any
import io
import json


class DataLoader:
    """Handle data loading from various sources"""
    
    @staticmethod
    def load_csv(file_path: Union[str, Path, io.BytesIO], **kwargs) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            return pd.read_csv(file_path, **kwargs)
        except Exception as e:
            raise ValueError(f"Error loading CSV: {str(e)}")
    
    @staticmethod
    def load_excel(file_path: Union[str, Path, io.BytesIO], **kwargs) -> pd.DataFrame:
        """Load data from Excel file"""
        try:
            return pd.read_excel(file_path, **kwargs)
        except Exception as e:
            raise ValueError(f"Error loading Excel: {str(e)}")
    
    @staticmethod
    def load_json(file_path: Union[str, Path, io.BytesIO], **kwargs) -> pd.DataFrame:
        """Load data from JSON file"""
        try:
            return pd.read_json(file_path, **kwargs)
        except Exception as e:
            raise ValueError(f"Error loading JSON: {str(e)}")
    
    @staticmethod
    def load_sample_dataset(dataset_name: str) -> pd.DataFrame:
        """Load sample datasets from seaborn"""
        available_datasets = sns.get_dataset_names()
        if dataset_name not in available_datasets:
            raise ValueError(f"Dataset '{dataset_name}' not found. Available: {available_datasets}")
        return sns.load_dataset(dataset_name)
    
    @staticmethod
    def get_available_datasets() -> list:
        """Get list of available seaborn datasets"""
        return sns.get_dataset_names()


class DataProcessor:
    """Process and transform data"""
    
    @staticmethod
    def get_basic_info(df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic information about the dataframe"""
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum() / 1024**2,  # MB
        }
    
    @staticmethod
    def get_numeric_columns(df: pd.DataFrame) -> list:
        """Get list of numeric columns"""
        return df.select_dtypes(include=[np.number]).columns.tolist()
    
    @staticmethod
    def get_categorical_columns(df: pd.DataFrame) -> list:
        """Get list of categorical columns"""
        return df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    @staticmethod
    def clean_data(df: pd.DataFrame, 
                   drop_na: bool = False,
                   fill_na: Optional[Any] = None,
                   drop_duplicates: bool = False) -> pd.DataFrame:
        """Clean the dataframe"""
        df_cleaned = df.copy()
        
        if drop_na:
            df_cleaned = df_cleaned.dropna()
        elif fill_na is not None:
            df_cleaned = df_cleaned.fillna(fill_na)
        
        if drop_duplicates:
            df_cleaned = df_cleaned.drop_duplicates()
        
        return df_cleaned
    
    @staticmethod
    def get_statistics(df: pd.DataFrame) -> pd.DataFrame:
        """Get statistical summary of the dataframe"""
        return df.describe(include='all')
    
    @staticmethod
    def filter_data(df: pd.DataFrame, 
                   column: str, 
                   values: Union[list, Any]) -> pd.DataFrame:
        """Filter dataframe by column values"""
        if isinstance(values, list):
            return df[df[column].isin(values)]
        else:
            return df[df[column] == values]
    
    @staticmethod
    def create_bins(df: pd.DataFrame, 
                   column: str, 
                   bins: int = 5,
                   labels: Optional[list] = None) -> pd.DataFrame:
        """Create bins for a numeric column"""
        df_copy = df.copy()
        df_copy[f'{column}_binned'] = pd.cut(df_copy[column], bins=bins, labels=labels)
        return df_copy
    
    @staticmethod
    def normalize_column(df: pd.DataFrame, 
                        column: str, 
                        method: str = 'minmax') -> pd.DataFrame:
        """Normalize a numeric column"""
        df_copy = df.copy()
        if method == 'minmax':
            df_copy[f'{column}_normalized'] = (
                (df_copy[column] - df_copy[column].min()) / 
                (df_copy[column].max() - df_copy[column].min())
            )
        elif method == 'zscore':
            df_copy[f'{column}_normalized'] = (
                (df_copy[column] - df_copy[column].mean()) / 
                df_copy[column].std()
            )
        return df_copy
    
    @staticmethod
    def pivot_table(df: pd.DataFrame,
                   index: str,
                   columns: str,
                   values: str,
                   aggfunc: str = 'mean') -> pd.DataFrame:
        """Create a pivot table"""
        return df.pivot_table(
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc
        )
    
    @staticmethod
    def correlation_matrix(df: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
        """Calculate correlation matrix for numeric columns"""
        numeric_df = df.select_dtypes(include=[np.number])
        return numeric_df.corr(method=method)


class DataValidator:
    """Validate data quality"""
    
    @staticmethod
    def check_missing_data(df: pd.DataFrame) -> pd.DataFrame:
        """Check for missing data"""
        missing = df.isnull().sum()
        missing_percent = (missing / len(df)) * 100
        return pd.DataFrame({
            'Missing_Count': missing,
            'Missing_Percent': missing_percent
        }).sort_values('Missing_Count', ascending=False)
    
    @staticmethod
    def check_duplicates(df: pd.DataFrame) -> Dict[str, Any]:
        """Check for duplicate rows"""
        duplicates = df.duplicated().sum()
        return {
            'duplicate_count': duplicates,
            'duplicate_percent': (duplicates / len(df)) * 100
        }
    
    @staticmethod
    def detect_outliers(df: pd.DataFrame, column: str, method: str = 'iqr') -> pd.Series:
        """Detect outliers in a numeric column"""
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (df[column] < lower_bound) | (df[column] > upper_bound)
        elif method == 'zscore':
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            return z_scores > 3
        else:
            raise ValueError("Method must be 'iqr' or 'zscore'")
