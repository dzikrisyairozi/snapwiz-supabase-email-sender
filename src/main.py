import time
import logging
from database.supabase_client import get_supabase_client, fetch_emails
from mailer.sender import send_email
from email_logging.email_logger import get_last_sent_email, log_email, close_log_file
from utils.config import BATCH_SIZE, DELAY_BETWEEN_BATCHES, DELAY_BETWEEN_EMAILS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
logger = logging.getLogger()

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

        last_number, last_email = get_last_sent_email()
        
        if last_email:
            start_index = emails.index(last_email) + 1 if last_email in emails else 0
        else:
            start_index = 0

        for i in range(start_index, len(emails), BATCH_SIZE):
            batch = emails[i:i + BATCH_SIZE]
            logger.info(f"Sending batch {i//BATCH_SIZE + 1} of {(len(emails) - start_index)//BATCH_SIZE + 1}")
            for email in batch:
                send_email(email)
                time.sleep(DELAY_BETWEEN_EMAILS)

            logger.info(f"Batch {i//BATCH_SIZE + 1} completed. Waiting for {DELAY_BETWEEN_BATCHES/3600} hours before next batch.")
            time.sleep(DELAY_BETWEEN_BATCHES)
    except Exception as e:
        logger.error(f"An error occurred in the main function: {str(e)}")
    finally:
        close_log_file()

if __name__ == '__main__':
    main()