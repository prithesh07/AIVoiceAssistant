from openai import OpenAI
from typing import List, Dict
import json
import asyncio
import time
from .tools import Tools, tools_definition

class AIService:
    def __init__(self):
        self.client = OpenAI()
        self.tools = Tools()
        self.tools_definition = tools_definition
        self.assistant = None
        self.thread = None
        self.current_run_id = None
        self._setup()

    def _setup(self):
        if not self.assistant:
            self.assistant = self.client.beta.assistants.create(
                name="Salon Assistant",
                instructions="""You are a quick-response salon assistant. Give immediate, 
                one-sentence answers. Be direct and concise.""",
                model="gpt-4o-mini",
                tools=self.tools_definition
            )
        if not self.thread:
            self.thread = self.client.beta.threads.create()

    async def get_response(self, user_input: str) -> str:
        try:
            # Cancel previous run if exists
            if self.current_run_id:
                try:
                    self.client.beta.threads.runs.cancel(
                        thread_id=self.thread.id,
                        run_id=self.current_run_id
                    )
                except:
                    pass
                self.current_run_id = None

            # Create message and run immediately
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=user_input
            )

            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )
            self.current_run_id = run.id

            # Shorter timeout and faster polling
            start_time = time.time()
            max_wait_time = 15  # Reduced from 30 to 15 seconds
            
            while time.time() - start_time < max_wait_time:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
                
                if run_status.status == 'completed':
                    messages = self.client.beta.threads.messages.list(
                        thread_id=self.thread.id,
                        limit=1,
                        order='desc'  # Get most recent first
                    )
                    self.current_run_id = None
                    if messages.data:
                        return messages.data[0].content[0].text.value
                    break
                    
                elif run_status.status in ['failed', 'cancelled', 'expired']:
                    self.current_run_id = None
                    return "Please repeat that."
                
                await asyncio.sleep(0.1)  # Reduced from 0.5 to 0.1 seconds

            self.current_run_id = None
            return "Please continue."

        except Exception as e:
            self.current_run_id = None
            print(f"Error: {str(e)}")
            return "Please try again."