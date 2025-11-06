"""
Configuration management module
Handles environment variables and app configuration
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class"""
    
    # Base paths
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    ASSETS_DIR = BASE_DIR / "assets"
    
    # App settings
    APP_TITLE = os.getenv("APP_TITLE", "Professional Seaborn Visualization Dashboard")
    APP_ICON = os.getenv("APP_ICON", "📊")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
    
    # API Keys (if needed)
    API_KEY = os.getenv("API_KEY", "")
    
    # Database (if needed)
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 5432)),
        "name": os.getenv("DB_NAME", "mydb"),
        "user": os.getenv("DB_USER", "user"),
        "password": os.getenv("DB_PASSWORD", "password"),
    }
    
    # Visualization settings
    VIZ_CONFIG = {
        "style": "darkgrid",
        "palette": "husl",
        "context": "notebook",
        "font_scale": 1.2,
    }
    
    # Page configuration
    PAGE_CONFIG = {
        "page_title": APP_TITLE,
        "page_icon": APP_ICON,
        "layout": "wide",
        "initial_sidebar_state": "expanded",
        "menu_items": {
            'Get Help': 'https://docs.streamlit.io/',
            'Report a bug': "https://github.com/yourusername/yourrepo/issues",
            'About': f"# {APP_TITLE}\nA professional data visualization dashboard"
        }
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            "app_title": cls.APP_TITLE,
            "app_icon": cls.APP_ICON,
            "debug_mode": cls.DEBUG_MODE,
            "base_dir": str(cls.BASE_DIR),
            "data_dir": str(cls.DATA_DIR),
        }
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.ASSETS_DIR.mkdir(exist_ok=True)


# Create directories on import
Config.ensure_directories()
