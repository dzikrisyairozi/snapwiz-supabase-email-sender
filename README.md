# Supabase Email Sender

This Python script automates the process of sending emails to users stored in a Supabase database. It's designed to send emails in batches with configurable delays to avoid triggering spam filters.

## Features

- Fetches user emails from a Supabase database
- Sends emails using Gmail SMTP
- Implements batch sending with configurable delays
- Includes error handling and logging

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
3. Send emails in batches with configurable delays

## Configuration

You can adjust the following parameters in the `main()` function:

- `batch_size`: Number of emails to send in each batch (default: 10)
- `delay_between_batches`: Delay between batches in seconds (default: 2 hours)
- `delay_between_emails`: Delay between individual emails in seconds (default: 10)

## Logging

The script logs its activities to the console. You can adjust the logging level in the `logging.basicConfig()` call if needed.
