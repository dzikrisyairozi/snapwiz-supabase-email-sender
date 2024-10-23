import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
from utils.config import EMAIL_ADDRESS, EMAIL_PASSWORD
from email_logging.email_logger import log_email
from .email_template import create_email_message

load_dotenv()

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
    msg = create_email_message(to_email)

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