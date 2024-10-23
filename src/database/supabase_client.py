from supabase import create_client, Client
import os
from dotenv import load_dotenv
from utils.config import SUPABASE_URL, SUPABASE_KEY

load_dotenv()

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
        raise Exception(f"Error fetching emails from Supabase: {str(e)}")