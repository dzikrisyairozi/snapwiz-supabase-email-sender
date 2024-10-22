import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Email credentials
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

        batch_size = 10
        delay_between_batches = 2 * 60 * 60  # 2 hours

        for i in range(0, len(emails), batch_size):
            batch = emails[i:i + batch_size]
            logger.info(f"Sending batch {i//batch_size + 1} of {len(emails)//batch_size + 1}")
            for email in batch:
                send_email(email)
                time.sleep(10)  # Delay between individual emails

            logger.info(f"Batch {i//batch_size + 1} completed. Waiting for {delay_between_batches/3600} hours before next batch.")
            time.sleep(delay_between_batches)  # Delay between batches
    except Exception as e:
        logger.error(f"An error occurred in the main function: {str(e)}")

if __name__ == '__main__':
    main()