from datetime import datetime
from typing import List, Dict

class Message:
    def __init__(self, content: str, sender: str):
        self.content = content
        self.sender = sender
        self.timestamp = datetime.now()

class Conversation:
    def __init__(self, call_sid: str):
        self.call_sid = call_sid
        self.messages: List[Message] = []
        self.recordings = set()

    def add_message(self, content: str, sender: str):
        message = Message(content, sender)
        self.messages.append(message)
        return message

    def add_recording(self, recording_sid: str):
        self.recordings.add(recording_sid)