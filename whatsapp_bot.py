import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

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
            self.client = OpenAI(
                api_key=os.getenv('API_KEY'),
                base_url=os.getenv('API_BASE_URL')
            )
            self.model = os.getenv('MODEL_NAME')
            self.system_prompt = self._load_system_prompt()
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

    def get_list_products(self) -> List[Dict]:
        """Returns a list of available products"""
        # Placeholder product list
        return [
            {
                "id": 1,
                "name": "Premium Widget",
                "price": 99.99,
                "description": "High-quality widget with advanced features",
                "stock": 50
            },
            {
                "id": 2,
                "name": "Super Gadget",
                "price": 149.99,
                "description": "Innovative gadget for modern needs",
                "stock": 30
            },
            {
                "id": 3,
                "name": "Deluxe Toolset",
                "price": 199.99,
                "description": "Complete set of professional tools",
                "stock": 20
            }
        ]

    def add_order_for_client(self, client_id: str, items: List[Dict]) -> Dict:
        """Process an order for a client"""
        # Placeholder order processing
        order = {
            "order_id": f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "client_id": client_id,
            "items": items,
            "total_amount": sum(item["price"] * item["quantity"] for item in items),
            "delivery_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "status": "scheduled"
        }
        return order

    def process_message(self, message: str, client_id: str) -> str:
        """Process incoming message and generate response using LLM"""
        try:
            # Get available products
            products = self.get_list_products()
            products_info = json.dumps(products, indent=2)

            # Create messages for the chat
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "system", "content": f"Available products: {products_info}"},
                {"role": "user", "content": message}
            ]

            # Generate response using OpenRouter
            response = self.client.chat.completions.create(
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
        # Example conversation
        response = bot.process_message("Hello! What products do you have?", "client123")
        print(response)
    except Exception as e:
        print(f"Error initializing bot: {str(e)}")
