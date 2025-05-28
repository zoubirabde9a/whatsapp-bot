from typing import Dict, List
from datetime import datetime

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}
        
    def add_message(self, phone_number: str, role: str, content: str):
        """Add a message to the conversation history"""
        if phone_number not in self.conversations:
            self.conversations[phone_number] = []
            
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversations[phone_number].append(message)
        
    def get_conversation_history(self, phone_number: str) -> List[Dict]:
        """Get conversation history for a specific phone number"""
        return self.conversations.get(phone_number, [])
    
    def clear_conversation(self, phone_number: str):
        """Clear conversation history for a specific phone number"""
        if phone_number in self.conversations:
            self.conversations[phone_number] = [] 