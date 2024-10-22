# Supabase Email Sender

This Python script automates the process of sending emails to users stored in a Supabase database. It's designed to send emails in batches with configurable delays to avoid triggering spam filters, and can resume from where it left off if interrupted.

## Features

- Fetches user emails from a Supabase database
- Sends emails using Gmail SMTP
- Implements batch sending with configurable delays
- Includes error handling and logging
- Resumes from the last sent email if the script is interrupted

## Prerequisites

- Python 3.7+
- A Supabase account and project
- A Gmail account (for sending emails)

## Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file and fill in your credentials:
   - SUPABASE_URL: Your Supabase project URL
   - SUPABASE_KEY: Your Supabase API key
   - EMAIL_ADDRESS: Your Gmail address
   - EMAIL_PASSWORD: Your Gmail App Password (see below for instructions)

## Gmail App Password Setup

To use this script with Gmail, you need to create an App Password:

1. Go to your [Google Account](https://myaccount.google.com/).
2. Select "Security" on the left navigation panel.
3. Under "Signing in to Google," select "2-Step Verification" and turn it on if it's not already.
4. Back on the Security page, select "App passwords" (you might need to scroll down).
5. Select "Mail" and "Other (Custom name)" from the dropdowns.
6. Enter a name for the app (e.g., "Python Email Script") and click "Generate".
7. Copy the 16-character password and use it as your EMAIL_PASSWORD in the `.env` file.

## Usage

Run the script using:

```bash
python main.py
```

The script will:
1. Connect to your Supabase database
2. Fetch email addresses
3. Check the last sent email from the log files
4. Resume sending emails from where it left off
5. Send emails in batches with configurable delays

## Configuration

You can adjust the following parameters in the `main()` function:

- `batch_size`: Number of emails to send in each batch (default: 10)
- `delay_between_batches`: Delay between batches in seconds (default: 2 hours)
- `delay_between_emails`: Delay between individual emails in seconds (default: 10)

## Logging

The script logs its activities to the console and creates log files in the `/log` directory. Each log file contains up to 100 sent emails and is named with a timestamp (e.g., `sent_emails_20230515_120000.log`). These log files are used to track progress and allow the script to resume from where it left off if interrupted.

## Error Handling

The script includes error handling for common issues such as SMTP authentication failures and connection problems. If an error occurs, it will be logged, and the script will attempt to continue with the next email.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
