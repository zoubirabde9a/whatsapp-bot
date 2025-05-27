# WhatsApp Messaging Script

A Python script to send WhatsApp messages using the WhatsApp Business API.

## Prerequisites

- Python 3.x
- WhatsApp Business API access
- WhatsApp API token

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install requests python-dotenv
```

## Configuration

1. Create a `.env` file in the project root directory
2. Add your WhatsApp API token:
```
WHATSAPP_API_TOKEN=your_api_token_here
```

## Usage

The script can be run from the command line with the following options:

```bash
python test_whatsapp.py [--recipient RECIPIENT] [--message MESSAGE]
```

### Arguments

- `--recipient`, `-r`: Recipient's phone number (default: 213562408768)
- `--message`, `-m`: Message text to send (default: "Hello! This is a test message.")

### Examples

1. Send message with default values:
```bash
python test_whatsapp.py
```

2. Send message to specific number:
```bash
python test_whatsapp.py --recipient 213562408768
# or
python test_whatsapp.py -r 213562408768
```

3. Send custom message:
```bash
python test_whatsapp.py --message "Hello from Python!"
# or
python test_whatsapp.py -m "Hello from Python!"
```

4. Send custom message to specific number:
```bash
python test_whatsapp.py --recipient 213562408768 --message "Hello from Python!"
# or
python test_whatsapp.py -r 213562408768 -m "Hello from Python!"
```

## API Configuration

The script uses the following default configuration:
- API Version: v22.0
- Phone Number ID: 687405501116512

These values can be modified in the script if needed.

## Error Handling

The script will:
- Check for the presence of the WhatsApp API token
- Print the response status code and message from the API
- Raise a ValueError if the API token is not found

## Security Notes

- Never commit your `.env` file or expose your API token
- Keep your API token secure and rotate it periodically
- Use environment variables for sensitive information

## License

This project is open source and available under the MIT License.