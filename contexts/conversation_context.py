from typing import Dict
from models.conversation import Conversation
import logging

logger = logging.getLogger(__name__)

class ConversationContext:
    """Manages active conversation sessions."""
    
    def __init__(self):
        """Initialize conversation storage."""
        self.conversations: Dict[str, Conversation] = {}

    def get_or_create_conversation(self, call_sid: str) -> Conversation:
        """Get existing conversation or create new one for given call ID."""
        if call_sid not in self.conversations:
            self.conversations[call_sid] = Conversation(call_sid)
        return self.conversations[call_sid]