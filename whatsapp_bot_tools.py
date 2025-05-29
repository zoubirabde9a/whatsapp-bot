from typing import List, Dict
from datetime import datetime, timedelta

def get_list_products() -> List[Dict]:
    """Returns a list of available products"""
    # Placeholder product list
    return [
        {
            "id": 1,
            "name": "Asus Gaming Mouse",
            "price": 6500,
            "description": "Asus Gaming Mouse with RGB lighting and 16000 DPI",
            "stock": 50,
            "image_url": "https://www.picpedia.org/chalkboard/images/example.jpg",
        },
        {
            "id": 2,
            "name": "Asus Gaming Keyboard",
            "price": 17000,
            "description": "Asus Gaming Keyboard with RGB lighting",
            "stock": 30,
            "image_url": "https://www.picpedia.org/chalkboard/images/example.jpg",
        },
        {
            "id": 3,
            "name": "Asus Gaming Headset",
            "price": 9500,
            "description": "Asus Gaming Headset with RGB lighting",
            "stock": 20,
            "image_url": "https://www.picpedia.org/chalkboard/images/example.jpg",
        },
        {
            "id": 4,
            "name": "Asus Gaming Mousepad",
            "price": 1500,
            "description": "Asus Gaming Mousepad with RGB lighting",
            "stock": 10,
        }
    ]

def add_order_for_client(client_id: str, items: List[Dict]) -> Dict:
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

def create_order(user_phone: str, user_name: str, user_location: str, products: List[Dict]) -> Dict:
    """
    Create a new order for a user
    
    Args:
        user_phone (str): User's phone number
        user_name (str): User's name
        user_location (str): User's delivery location
        products (List[Dict]): List of products to order with quantities
        
    Returns:
        Dict: Order details including order ID, status, and delivery information
    """
    # TODO: Implement actual order creation logic
    # This is a placeholder implementation
    order = {
        "order_id": f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "user_phone": user_phone,
        "user_name": user_name,
        "user_location": user_location,
        "products": products,
        "total_amount": sum(product["price"] * product["quantity"] for product in products),
        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "delivery_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
        "status": "pending"
    }
    return order

def get_order_status(user_phone: str) -> List[Dict]:
    """
    Get the status of all orders for a user
    
    Args:
        user_phone (str): User's phone number
        
    Returns:
        List[Dict]: List of orders with their current status
    """
    # TODO: Implement actual order status retrieval logic
    # This is a placeholder implementation
    return [
        {
            "order_id": "ORD-20240315123456",
            "order_date": "2024-03-15 12:34:56",
            "status": "pending",
            "delivery_date": "2024-03-18",
            "total_amount": 15000
        }
    ] 