from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv
import os
from ..utils.completions import completions_create, ChatHistory

# Load environment variables
load_dotenv()

class LLM:
    """
    A class to interact with OpenAI's language models.
    
    Attributes:
        client: OpenAI client instance
        model: The model name to use for generation
    """
    
    def __init__(self):
        """Initialize the LLM with OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("MODEL_NAME")
        self.chat_history = ChatHistory()
    
    def generate(self, query: str, use_history: bool = False, custom_messages: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate a response from the language model.
        
        Args:
            query: The user's input query
            use_history: Whether to include previous conversation history
            custom_messages: Optional custom message list to use instead of building from query
            
        Returns:
            The model's response text
        """
        if custom_messages:
            # Use provided custom messages directly
            messages = custom_messages
        elif use_history:
            # Add the query to history and use the full history
            self.chat_history.add_user_message(query)
            messages = self.chat_history
        else:
            # Just use the query without history
            messages = [{"role": "user", "content": query}]
        
        # Get response from the model
        response = completions_create(self.client, messages, self.model)
        
        # If using history, add the response to history
        if use_history:
            self.chat_history.add_assistant_message(response)
        
        return response
    
    def add_system_message(self, content: str) -> None:
        """Add or replace a system message in the chat history."""
        self.chat_history.add_system_message(content)
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.chat_history.clear()
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get a copy of the current conversation history."""
        return list(self.chat_history)
    
