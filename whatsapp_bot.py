import os
from typing import List, Dict
import openai
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
from whats_app_bot_constants import SYSTEM_PROMPT
from whatsapp_bot_tools import get_list_products, add_order_for_client, create_order, get_order_status

# Load environment variables
load_dotenv()

class WhatsAppBot:
    def __init__(self):
        # Check for required environment variables
        required_vars = ['API_KEY', 'API_BASE_URL', 'MODEL_NAME']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                "Please check your .env file and ensure all required variables are set."
            )

        try:
            # Configure OpenAI client
            openai.api_key = os.getenv('API_KEY')
            openai.api_base = os.getenv('API_BASE_URL')
            self.model = os.getenv('MODEL_NAME')
            self.system_prompt = SYSTEM_PROMPT
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI client: {str(e)}")
        
    def _load_system_prompt(self) -> str:
        """Load the system prompt from file"""
        try:
            with open('system_prompt.txt', 'r') as file:
                return file.read()
        except FileNotFoundError:
            print("Warning: system_prompt.txt not found, using default prompt")
            return "You are a helpful sales assistant bot."

    def process_message(self, client_id: str, history: List[Dict] = None) -> str:
        """Process incoming message and generate response using LLM"""
        try:
            # Get available products
            products = get_list_products()
            products_info = json.dumps(products, indent=2)

            # Create messages for the chat
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "system", "content": f"Available products: {products_info}"}
            ]
            
            for i in range(len(history)):
                content = history[i]['content']
                role = history[i]['role']
                messages.append({"role": role, "content": content})

            # Generate response using OpenRouter
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

# Example usage
if __name__ == "__main__":
    try:
        bot = WhatsAppBot()
        history = [
            {"role": "user", "content": "Hello! What products do you have?"},
            {"role": "assistant", "content": "I have the following products available: 1. Premium Widget, 2. Super Gadget, 3. Deluxe Toolset."}
        ]
        # Example conversation
        response = bot.process_message("client123", history)
        print(response)
    except Exception as e:
        print(f"Error initializing bot: {str(e)}")
