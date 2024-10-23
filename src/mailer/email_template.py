import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import EMAIL_ADDRESS

def create_email_message(to_email):
    """
    Create an email message with HTML content.

    This function generates a MIME multipart email message with HTML content
    read from an external template file. It sets up the basic email structure
    including subject, sender, and recipient.

    Args:
        to_email (str): The email address of the recipient.

    Returns:
        email.mime.multipart.MIMEMultipart: A fully formed email message object
        ready to be sent.

    Raises:
        FileNotFoundError: If the HTML template file is not found.
        IOError: If there's an error reading the HTML template file.

    The function performs the following steps:
    1. Creates a MIMEMultipart object for the email message.
    2. Sets the email subject, sender (From), and recipient (To).
    3. Reads the HTML content from a template file located at 
       'templates/index.html' relative to this script's location.
    4. Attaches the HTML content to the email message.

    Note:
        - The email subject is currently hardcoded and can be modified as needed.
        - The sender's email address is taken from the EMAIL_ADDRESS config variable.
        - The HTML template file must exist at the specified path for this function to work.

    Example usage:
        email_message = create_email_message("recipient@example.com")
        # email_message can now be used with smtplib to send the email
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Check Out Our New Service'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    # Read HTML content from file
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    with open(template_path, 'r') as file:
        html = file.read()

    msg.attach(MIMEText(html, 'html'))
    return msg