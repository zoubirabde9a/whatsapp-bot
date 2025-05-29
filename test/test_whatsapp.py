import os
import requests
import argparse
from dotenv import load_dotenv

# API Configuration
API_VERSION = "v22.0"
PHONE_NUMBER_ID = "687405501116512"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"

# Default Values
DEFAULT_RECIPIENT = "213562408768"
DEFAULT_MESSAGE = "ya kho rak hna ?"

# Environment Variables
ENV_TOKEN_KEY = "WHATSAPP_API_TOKEN"

def send_whatsapp_message(recipient_number: str, message_text: str):
    """
    Send a WhatsApp message to a specific recipient.
    
    Args:
        recipient_number (str): The recipient's phone number
        message_text (str): The message text to send
    """
    # Load environment variables
    load_dotenv()
    
    # Get API token from environment variable
    token = os.getenv(ENV_TOKEN_KEY)
    if not token:
        raise ValueError(f"{ENV_TOKEN_KEY} not found in environment variables")

    # Headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Request payload
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    # Make the POST request
    response = requests.post(BASE_URL, headers=headers, json=payload)
    
    # Print response details
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Send a WhatsApp message to a specified number.')
    parser.add_argument('--recipient', '-r', 
                       default=DEFAULT_RECIPIENT,
                       help=f'Recipient phone number (default: {DEFAULT_RECIPIENT})')
    parser.add_argument('--message', '-m',
                       default=DEFAULT_MESSAGE,
                       help=f'Message text to send (default: {DEFAULT_MESSAGE})')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Send the message
    send_whatsapp_message(args.recipient, args.message) 