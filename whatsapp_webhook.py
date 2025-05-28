from flask import Flask, request, jsonify
from whatsapp_bot import WhatsAppBot
from conversation_manager import ConversationManager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
bot = WhatsAppBot()
conversation_manager = ConversationManager()

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
                    
                    # Add user message to conversation history
                    conversation_manager.add_message(phone_number, "user", message_content)
                    
                    # Get conversation history
                    history = conversation_manager.get_conversation_history(phone_number)
                    
                    # Process message with bot
                    response = bot.process_message(message_content, phone_number)
                    
                    # Add bot response to conversation history
                    conversation_manager.add_message(phone_number, "assistant", response)
                    
                    # Send response back to WhatsApp
                    send_whatsapp_message(phone_number, response)
                    
                    return jsonify({"status": "success"})
        
        return jsonify({"status": "error", "message": "Invalid webhook data"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def send_whatsapp_message(phone_number: str, message: str):
    """Send message back to WhatsApp"""
    # This is a placeholder for the actual WhatsApp API call
    # You'll need to implement this using the WhatsApp Business API
    # or a service like Twilio
    print(f"Sending message to {phone_number}: {message}")
    
    # Example implementation using requests (you'll need to add proper authentication)
    # import requests
    # url = f"https://graph.facebook.com/v17.0/{os.getenv('WHATSAPP_PHONE_NUMBER_ID')}/messages"
    # headers = {
    #     "Authorization": f"Bearer {os.getenv('WHATSAPP_TOKEN')}",
    #     "Content-Type": "application/json"
    # }
    # data = {
    #     "messaging_product": "whatsapp",
    #     "to": phone_number,
    #     "type": "text",
    #     "text": {"body": message}
    # }
    # response = requests.post(url, headers=headers, json=data)
    # return response.json()

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verify webhook for WhatsApp"""
    # Get the verification token from the query parameters
    verify_token = request.args.get('hub.verify_token')
    
    # Check if the token matches your verification token
    if verify_token == os.getenv('WHATSAPP_VERIFY_TOKEN'):
        # Return the challenge token
        return request.args.get('hub.challenge')
    
    return 'Invalid verification token'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
