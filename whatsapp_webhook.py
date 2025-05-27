from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
import json

app = Flask(__name__)

# Load environment variables
load_dotenv()

# WhatsApp API Configuration
API_VERSION = "v22.0"
PHONE_NUMBER_ID = "687405501116512"
VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "your_verify_token_here")

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

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verify the webhook for WhatsApp API."""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('WEBHOOK_VERIFIED')
            return challenge, 200
        else:
            return 'Forbidden', 403
    # Always return a response
    return 'Bad Request', 400

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming messages from WhatsApp."""
    data = request.get_json()
    
    try:
        if data['object'] == 'whatsapp_business_account':
            for entry in data['entry']:
                for change in entry['changes']:
                    if change['value'].get('messages'):
                        for message in change['value']['messages']:
                            # Extract message details
                            from_number = message['from']
                            message_body = message['text']['body']
                            
                            # Process the message
                            print(f"Received message from {from_number}: {message_body}")
                            
                            # You can add your message handling logic here
                            # For example, send an acknowledgment
                            send_message(from_number, f"Received your message: {message_body}")
            
            return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True) 