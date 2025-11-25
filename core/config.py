"""
Configuration file for Twitter Bot
Contains API credentials and model settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# TWITTER API CREDENTIALS
# ============================================================================
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
API_SECRET = os.getenv('API_SECRET')  # Alternative name
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# ============================================================================
# GEMINI API CREDENTIALS
# ============================================================================
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# ============================================================================
# OPENAI API CREDENTIALS
# ============================================================================
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# ============================================================================
# MODEL CONFIGURATIONS
# ============================================================================
# Gemini models
GEMINI_TEXT_MODEL = "gemini-2.5-flash"
GEMINI_IMAGE_MODEL = "models/imagen-4.0-generate-001"

# OpenAI models
OPENAI_MODEL = "gpt-4.1-mini"

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================
# CSV file to track post history
CSV_FILE = 'data/post_history.csv'

# Topics for tweet generation
TOPICS = [
    'Artificial Intelligence',
    'Generative AI',
    'Machine Learning',
    'Python Programming',
    'Data Science',
    'Deep Learning',
    'Natural Language Processing',
    'Computer Vision',
    'Neural Networks',
    'Large Language Models',
    'Data Analytics',
    'Big Data',
    'AI Ethics',
    'MLOps',
]

# Temperature setting for content generation
TEMPERATURE = 0.7

# Tweet length limits
MAX_TWEET_LENGTH = 280

# ============================================================================
# VALIDATION
# ============================================================================
def validate_credentials():
    """Validate that all required credentials are loaded"""
    required_twitter_vars = {
        'BEARER_TOKEN': BEARER_TOKEN,
        'API_KEY': API_KEY,
        'ACCESS_TOKEN': ACCESS_TOKEN,
        'ACCESS_TOKEN_SECRET': ACCESS_TOKEN_SECRET,
    }
    
    required_gemini_vars = {
        'GEMINI_API_KEY': GEMINI_API_KEY,
    }
    
    missing_vars = []
    
    # Check Twitter credentials
    for var_name, var_value in required_twitter_vars.items():
        if not var_value:
            missing_vars.append(var_name)
    
    # Check Gemini credentials
    for var_name, var_value in required_gemini_vars.items():
        if not var_value:
            missing_vars.append(var_name)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True


# Validate on import
if __name__ != "__main__":
    try:
        validate_credentials()
    except ValueError as e:
        print(f"⚠️ Warning: {e}")
