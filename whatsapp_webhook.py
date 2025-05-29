from flask import Flask, request, jsonify
from whatsapp_bot import WhatsAppBot
from conversation_manager import ConversationManager
import os
from dotenv import load_dotenv
import logging
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# WhatsApp API Configuration
API_VERSION = "v22.0"
PHONE_NUMBER_ID = "687405501116512"

def send_message(recipient_number: str, message_text: str):
    """Send a WhatsApp message using the API."""
    token = os.getenv("WHATSAPP_API_TOKEN")
    if not token:
        raise ValueError("WHATSAPP_API_TOKEN not found in environment variables")

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    response = requests.post(
        f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages",
        headers=headers,
        json=payload
    )
    return response.json()

# Check for required WhatsApp environment variables
required_whatsapp_vars = ['WHATSAPP_VERIFY_TOKEN', 'WHATSAPP_API_TOKEN']
missing_whatsapp_vars = [var for var in required_whatsapp_vars if not os.getenv(var)]
if missing_whatsapp_vars:
    logger.warning(f"Missing WhatsApp environment variables: {', '.join(missing_whatsapp_vars)}")

app = Flask(__name__)

try:
    bot = WhatsAppBot()
    conversation_manager = ConversationManager()
    logger.info("Bot initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize bot: {str(e)}")
    raise

def format_phone_number(phone: str) -> str:
    """Format phone number to standard format"""
    # Remove any non-digit characters
    phone = ''.join(filter(str.isdigit, phone))
    # Add country code if not present (assuming US numbers)
    if len(phone) == 10:
        phone = '1' + phone
    return phone

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        data = request.get_json()
        
        # Extract message details
        if 'entry' in data and len(data['entry']) > 0:
            entry = data['entry'][0]
            if 'changes' in entry and len(entry['changes']) > 0:
                change = entry['changes'][0]
                if 'value' in change and 'messages' in change['value']:
                    message = change['value']['messages'][0]
                    
                    # Get phone number and message content
                    phone_number = format_phone_number(message['from'])
                    message_content = message['text']['body']
                    
                    logger.info(f"Received message from {phone_number}: {message_content}")

                    # Add user message to conversation history
                    conversation_manager.add_message(phone_number, "user", message_content)
                    
                    # Get conversation history
                    history = conversation_manager.get_conversation_history(phone_number)
                    
                    # Process message with bot using conversation history
                    response = bot.process_message(phone_number, history)
                    
                    # Add bot response to conversation history
                    conversation_manager.add_message(phone_number, "assistant", response)

                    # Send response back to WhatsApp
                    try:
                        send_message(phone_number, response)
                        logger.info(f"Successfully sent message to {phone_number}")
                    except Exception as e:
                        logger.error(f"Failed to send WhatsApp message: {str(e)}")
                    
                    return jsonify({"status": "success"})
        
        return jsonify({"status": "error", "message": "Invalid webhook data"})
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verify webhook for WhatsApp"""
    try:
        # Get the verification token from the query parameters
        verify_token = request.args.get('hub.verify_token')
        
        # Check if the token matches your verification token
        if verify_token == os.getenv('WHATSAPP_VERIFY_TOKEN'):
            # Return the challenge token
            return request.args.get('hub.challenge')
        
        return 'Invalid verification token'
    except Exception as e:
        logger.error(f"Error verifying webhook: {str(e)}")
        return 'Error verifying webhook'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
