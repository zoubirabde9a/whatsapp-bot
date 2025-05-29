import subprocess
import json
import argparse

DEFAULT_PHONE_NUMBER = "1234567890"

def test_start_conversation(phone_number):
    # The curl command to test the endpoint
    curl_command = [
        'curl',
        '-X', 'POST',
        'http://localhost:5000/start-conversation',
        '-H', 'Content-Type: application/json',
        '-d', f'{{"phone_number": "{phone_number}"}}'
    ]
    
    # Execute the curl command
    result = subprocess.run(curl_command, capture_output=True, text=True)
    
    # Print the response
    print("Status Code:", result.returncode)
    print("Response:", result.stdout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test WhatsApp conversation initiation')
    parser.add_argument('phone_number', nargs='?', default=DEFAULT_PHONE_NUMBER, 
                       help=f'Phone number to start conversation with (default: {DEFAULT_PHONE_NUMBER})')
    args = parser.parse_args()
    
    test_start_conversation(args.phone_number) 