from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import EMAIL_ADDRESS

def create_email_message(to_email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Check Out Our New Service'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    html = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }
            h1 {
                color: #2c3e50;
            }
            .cta-button {
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Check Out Our New Service!</h1>
            <p>Dear User,</p>
            <p>Thank you for joining our service. We're excited to have you on board!</p>
            <p>To get started, please click the button below:</p>
            <p><a href="https://alphabyte.co.jp/" class="cta-button">Get Started</a></p>
            <p>If you have any questions, feel free to reply to this email.</p>
            <p>Best regards,<br>Your Company Team</p>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html, 'html'))
    return msg