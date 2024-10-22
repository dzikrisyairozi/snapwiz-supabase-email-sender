import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from supabase import create_client, Client
from dotenv import load_dotenv
import logging
from datetime import datetime
import glob
# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Email credentials
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure log directory exists
os.makedirs('log', exist_ok=True)

# Global variables for logging
email_count = 0
current_log_file = None

def get_supabase_client() -> Client:
    """
    Create and return a Supabase client.

    This function uses the SUPABASE_URL and SUPABASE_KEY environment variables
    to initialize a connection to the Supabase project.

    Returns:
        Client: An initialized Supabase client object.

    Raises:
        ValueError: If SUPABASE_URL or SUPABASE_KEY is not set in the environment.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase credentials are not set in the environment.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_emails(client: Client):
    """
    Fetch email addresses from the Supabase database.

    This function executes a custom RPC function 'select_from_auth_users'
    on the Supabase server to retrieve email addresses from the auth.users table.

    Args:
        client (Client): An initialized Supabase client.

    Returns:
        list: A list of email addresses.

    Raises:
        Exception: If there's an error in fetching emails from Supabase.
    """
    try:
        response = client.rpc('select_from_auth_users').execute()
        return [user['email'] for user in response.data]
    except Exception as e:
        logger.error(f"Error fetching emails from Supabase: {str(e)}")
        raise

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

def send_email(to_email):
    """
    Send an email to a specified address.

    This function creates and sends an email using the Gmail SMTP server.
    It uses the EMAIL_ADDRESS and EMAIL_PASSWORD environment variables for authentication.

    Args:
        to_email (str): The recipient's email address.

    Raises:
        smtplib.SMTPAuthenticationError: If authentication with the SMTP server fails.
        smtplib.SMTPException: For other SMTP-related errors.
        Exception: For any other unexpected errors during the email sending process.
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = 'Your Subject Here'

    body = 'Your email body here'
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        logger.info(f"Email sent successfully to {to_email}")
        log_email(to_email)
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed. Check your email credentials. Error: {str(e)}")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}. Error: {str(e)}")

def main():
    """
    Main function to orchestrate the email sending process.

    This function performs the following steps:
    1. Connects to Supabase and fetches email addresses.
    2. Sends emails in batches, with delays between individual emails and batches.
    3. Logs the progress of email sending.

    The batch size and delay between batches can be adjusted as needed.

    Raises:
        Exception: For any unexpected errors during the execution.
    """
    try:
        client = get_supabase_client()
        emails = fetch_emails(client)
        logger.info(f"Fetched {len(emails)} email addresses from Supabase")

        global email_count, current_log_file
        last_number, last_email = get_last_sent_email()
        email_count = last_number
        
        if last_email:
            start_index = emails.index(last_email) + 1 if last_email in emails else 0
        else:
            start_index = 0

        batch_size = 10
        delay_between_batches = 2 * 60 * 60  # 2 hours

        for i in range(start_index, len(emails), batch_size):
            batch = emails[i:i + batch_size]
            logger.info(f"Sending batch {i//batch_size + 1} of {(len(emails) - start_index)//batch_size + 1}")
            for email in batch:
                send_email(email)
                time.sleep(10)  # Delay between individual emails

            logger.info(f"Batch {i//batch_size + 1} completed. Waiting for {delay_between_batches/3600} hours before next batch.")
            time.sleep(delay_between_batches)  # Delay between batches
    except Exception as e:
        logger.error(f"An error occurred in the main function: {str(e)}")
    finally:
        if current_log_file:
            current_log_file.close()

if __name__ == '__main__':
    main()