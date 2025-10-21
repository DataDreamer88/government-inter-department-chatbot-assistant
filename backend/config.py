# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    DATA_GOV_API_KEY = os.getenv('DATA_GOV_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # Application Settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'groq')
    LLM_MODEL = os.getenv('LLM_MODEL', 'mixtral-8x7b-32768')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # Cache Settings
    CACHE_DURATION = int(os.getenv('CACHE_DURATION', 3600))
    
    # Data.gov.in API Base URL
    DATA_GOV_BASE_URL = "https://api.data.gov.in/resource/"