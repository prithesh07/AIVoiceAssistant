from datetime import datetime
from typing import List

class Message:
    """Represents a single message in a conversation."""
    
    def __init__(self, content: str, sender: str):
        """Initialize message with content and sender."""
        self.content = content
        self.sender = sender
        self.timestamp = datetime.now()

class Conversation:
    """Manages a conversation session with messages and recordings."""
    
    def __init__(self, call_sid: str):
        """Initialize conversation with call ID."""
        self.call_sid = call_sid
        self.messages: List[Message] = []
        self.recordings = set()

    def add_message(self, content: str, sender: str):
        """Add a new message to the conversation."""
        message = Message(content, sender)
        self.messages.append(message)
        return message

    def add_recording(self, recording_sid: str):
        """Add a recording ID to the conversation."""
        self.recordings.add(recording_sid)