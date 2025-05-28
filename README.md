# WhatsApp Sales Bot

A WhatsApp bot that uses OpenRouter's LLM to handle customer conversations, provide product information, and process orders.

## Features

- WhatsApp integration for customer communication
- OpenRouter LLM integration for natural conversations
- Conversation history management for each customer
- Product information and ordering system
- Webhook handling for WhatsApp messages

## Prerequisites

- Python 3.8 or higher
- WhatsApp Business API account
- OpenRouter API access
- Gunicorn (for production deployment)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd whatsapp-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```env
# OpenRouter Configuration
API_KEY=your_openrouter_api_key
API_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=your_preferred_model

# WhatsApp Configuration
WHATSAPP_VERIFY_TOKEN=your_webhook_verification_token
WHATSAPP_PHONE_NUMBER_ID=your_whatsapp_phone_number_id
WHATSAPP_TOKEN=your_whatsapp_business_api_token
```

## Project Structure

```
whatsapp-bot/
├── whatsapp_bot.py          # Main bot implementation
├── whatsapp_webhook.py      # Webhook handler
├── conversation_manager.py  # Conversation history management
├── system_prompt.txt        # Bot behavior configuration
├── requirements.txt         # Project dependencies
└── .env                     # Environment variables (not in repo)
```

## Running the Bot

### Development Mode

For development and testing, you can run the Flask development server:

```bash
python whatsapp_webhook.py
```

### Production Mode

For production deployment, use Gunicorn:

```bash
gunicorn -w 4 -b 127.0.0.1:5000 wsgi:app
```

## WhatsApp Webhook Setup

1. Set up your WhatsApp Business API account
2. Configure your webhook URL in the WhatsApp Business API dashboard:
   - URL: `https://your-domain.com/webhook`
   - Verify Token: Use the same value as `WHATSAPP_VERIFY_TOKEN` in your `.env` file

## Bot Capabilities

- Greet customers and introduce available products
- Provide detailed product information
- Handle customer inquiries
- Process orders
- Maintain conversation context
- Schedule deliveries

## Error Handling

The bot includes error handling for:
- Invalid webhook data
- API communication issues
- Message processing errors
- Conversation management errors

## Security Considerations

- All API keys and tokens are stored in environment variables
- Webhook verification is implemented
- Phone numbers are standardized and validated
- Conversation history is maintained securely

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your chosen license]