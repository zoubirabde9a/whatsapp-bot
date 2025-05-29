# WhatsApp Bot Test Scripts

This directory contains test scripts for the WhatsApp bot functionality.

## Start Conversation Test

The `test_start_conversation.py` script tests the conversation initiation endpoint.

### Usage

Run the script with a specific phone number (from repository root):
```bash
python test/test_start_conversation.py 9876543210
```

Or run without arguments to use the default phone number (1234567890):
```bash
python test/test_start_conversation.py
```

### Requirements

- Python 3.x
- curl command-line tool
- Running WhatsApp bot server (default: http://localhost:5000)

### What it does

The script sends a POST request to the `/start-conversation` endpoint with the provided phone number. It will:
1. Format the request with proper headers
2. Send the request using curl
3. Display the response status code and body

### Example Output

```bash
Status Code: 0
Response: {"status":"success","message":"Conversation initiated successfully"}
``` 