from typing import Dict
from models.conversation import Conversation
import logging

logger = logging.getLogger(__name__)

class ConversationContext:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}

    def get_or_create_conversation(self, call_sid: str) -> Conversation:
        if call_sid not in self.conversations:
            self.conversations[call_sid] = Conversation(call_sid)
        return self.conversations[call_sid]