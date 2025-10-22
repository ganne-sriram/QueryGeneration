"""
Configuration module for database connection and NL2SQL settings.
Loads environment variables from .env file.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for database and NL2SQL settings."""
    
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'citi_db')
    
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gemini-2.0-flash')
    
    CSV_PATH = os.getenv('CSV_PATH', '../MockData/exports/CSV Files')
    
    @classmethod
    def get_database_url(cls):
        """Generate SQLAlchemy database URL."""
        return f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
