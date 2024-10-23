import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

BATCH_SIZE = 10
DELAY_BETWEEN_BATCHES = 2 * 60 * 60  # 2 hours
DELAY_BETWEEN_EMAILS = 10  # 10 seconds