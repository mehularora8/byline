import logging
import os
from dotenv import load_dotenv

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('executive_summary.log'),
            logging.StreamHandler()  # Also print to console
        ]
    )
    logging.info("Logging setup completed")

def load_environment_variables():
    """Load environment variables from .env file"""
    load_dotenv(override=True)
    logging.info("Environment variables loaded")
    # Get API keys
    EXA_API_KEY = os.getenv("EXA_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

    # Validate required environment variables
    assert EXA_API_KEY is not None, "EXA_API_KEY not found in environment"
    assert OPENAI_API_KEY is not None, "OPENAI_API_KEY not found in environment"
    assert SENDER_EMAIL is not None, "SENDER_EMAIL not found in environment"
    assert SENDER_PASSWORD is not None, "SENDER_PASSWORD not found in environment"
    assert SUPABASE_URL is not None, "SUPABASE_URL not found in environment"
    assert SUPABASE_SERVICE_KEY is not None, "SUPABASE_SERVICE_KEY not found in environment"

    return {
        "EXA_API_KEY": EXA_API_KEY,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "SENDER_EMAIL": SENDER_EMAIL,
        "SENDER_PASSWORD": SENDER_PASSWORD,
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_SERVICE_KEY": SUPABASE_SERVICE_KEY
    }