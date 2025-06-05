import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base configuration loaded from environment variables
OUTLOOK_FOLDER = os.getenv('OUTLOOK_FOLDER', 'Bandeja de entrada')
ATTACHMENTS_DIR = Path(os.getenv('ATTACHMENTS_DIR', 'attachments'))
DB_URL = os.getenv('DB_URL', 'sqlite:///tickets.db')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LOG_FILE = os.getenv('LOG_FILE', 'tickets.log')
MAX_EMAILS = int(os.getenv('MAX_EMAILS', '10'))

ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)
