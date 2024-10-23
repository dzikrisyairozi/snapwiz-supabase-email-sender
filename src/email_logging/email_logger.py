import os
from datetime import datetime
import glob
import logging
# Ensure log directory exists
os.makedirs('log', exist_ok=True)

# Global variables for logging
email_count = 0
current_log_file = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_last_sent_email():
    """
    Retrieve the last sent email and its number from the most recent log file.

    This function performs the following steps:
    1. Finds all log files in the 'log' directory matching the pattern 'sent_emails_*.log'.
    2. Sorts the log files by name in reverse order to get the most recent one.
    3. Reads the last line of the most recent log file.
    4. Extracts the email number and address from the last line.

    Returns:
        tuple: A tuple containing two elements:
            - int: The number of the last sent email (0 if no emails have been sent).
            - str or None: The email address of the last sent email (None if no emails have been sent).

    If no log files are found or if the log file is empty, the function returns (0, None).

    Example:
        >>> get_last_sent_email()
        (3, 'prince.davies@telus.com')
    """
    log_files = sorted(glob.glob('log/sent_emails_*.log'), reverse=True)
    if not log_files:
        return 0, None
    
    with open(log_files[0], 'r') as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1].strip()
            number, email = last_line.split('. ', 1)
            return int(number), email
    
    return 0, None

def log_email(email):
    """
    Log the sent email to a file.

    This function logs the email to a file in the /log directory.
    It creates a new file every 100 emails.

    Args:
        email (str): The email address that was sent.
    """
    global email_count, current_log_file

    if current_log_file is None:
        last_number, _ = get_last_sent_email()
        email_count = last_number

    if current_log_file is None or email_count % 100 == 0:
        if current_log_file:
            current_log_file.close()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"log/sent_emails_{timestamp}.log"
        current_log_file = open(filename, "w")
        logger.info(f"Created new log file: {filename}")

    email_count += 1
    current_log_file.write(f"{email_count}. {email}\n")
    current_log_file.flush()  # Ensure the write is committed to the file

def close_log_file():
    """Close the current log file if it's open."""
    global current_log_file
    if current_log_file:
        current_log_file.close()
        current_log_file = None