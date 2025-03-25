from typing import List, Dict, Optional

def completions_create(client, messages: List[Dict[str, str]], model: str) -> str:
    """
    Sends a request to the client's completions.create method to interact with the language model.

    Args:
        client: The OpenAI client object
        messages: A list of message objects containing chat history for the model
        model: The model to use for generating responses

    Returns:
        The content of the model's response
    """
    response = client.chat.completions.create(messages=messages, model=model)
    return response.choices[0].message.content


def build_message(content: str, role: str) -> Dict[str, str]:
    """
    Builds a structured message that includes the role and content.

    Args:
        content: The actual content of the message
        role: The role of the speaker (e.g., user, assistant, system)

    Returns:
        A dictionary representing the structured message
    """
    return {"role": role, "content": content}


class ChatHistory(list):
    """
    A specialized list for managing chat history with optional size limits.
    """
    
    def __init__(self, messages: Optional[List[Dict[str, str]]] = None, max_length: int = -1):
        """
        Initialize the chat history with optional initial messages and max length.

        Args:
            messages: A list of initial messages
            max_length: The maximum number of messages the chat history can hold
        """
        super().__init__(messages or [])
        self.max_length = max_length
    
    def add_message(self, content: str, role: str) -> None:
        """
        Add a message to the chat history.

        Args:
            content: The message content
            role: The role of the message sender
        """
        message = build_message(content, role)
        
        if self.max_length > 0 and len(self) >= self.max_length:
            # Remove oldest non-system message if we're at capacity
            for i, msg in enumerate(self):
                if msg["role"] != "system":
                    self.pop(i)
                    break
        
        self.append(message)
    
    def add_user_message(self, content: str) -> None:
        """Add a user message to the chat history."""
        self.add_message(content, "user")
    
    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the chat history."""
        self.add_message(content, "assistant")
    
    def add_system_message(self, content: str) -> None:
        """
        Add or replace a system message at the beginning of the chat history.
        """
        # Remove any existing system messages
        self[:] = [msg for msg in self if msg["role"] != "system"]
        
        # Add the new system message at the beginning
        self.insert(0, build_message(content, "system"))
    
    def clear(self) -> None:
        """Clear all messages from the chat history."""
        self[:] = [] 