from openai import OpenAI
import json
import time
from .tools import Tools, tools_definition

class AIService:
    """Handles AI assistant setup and response logic."""

    def __init__(self):
        """Initialize AI service and setup assistant."""
        self.client = OpenAI()
        self.tools = Tools()
        self.tools_definition = tools_definition
        self.assistant = None
        self.thread = None
        self.current_run_id = None
        self._setup()

    def _setup(self):
        """Setup assistant and thread if not already created."""
        if not self.assistant:
            self.assistant = self.client.beta.assistants.create(
                name="Salon Assistant",
                instructions="""You are a salon assistant. When asked about services or prices:
                - Use get_services() to list available services
                - Use get_service_cost() to check specific service prices
                Give immediate, one-sentence answers. Be direct and concise.""",
                model="gpt-4o-mini",
                tools=self.tools_definition
            )
        if not self.thread:
            self.thread = self.client.beta.threads.create()

    async def get_response(self, user_input: str) -> str:
        """Process user input and return assistant response."""
        try:
            if self.current_run_id:
                try:
                    self.client.beta.threads.runs.cancel(
                        thread_id=self.thread.id,
                        run_id=self.current_run_id
                    )
                except:
                    pass
                self.current_run_id = None

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

            start_time = time.time()
            max_wait_time = 30

            while time.time() - start_time < max_wait_time:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )

                if run_status.status == 'requires_action':
                    tool_outputs = []
                    tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
                    
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        result = getattr(self.tools, function_name)(**function_args)
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(result)
                        })

                    self.client.beta.threads.runs.submit_tool_outputs(
                        thread_id=self.thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    continue

                elif run_status.status == 'completed':
                    messages = self.client.beta.threads.messages.list(
                        thread_id=self.thread.id,
                        limit=1,
                        order='desc'
                    )
                    self.current_run_id = None
                    if messages.data:
                        return messages.data[0].content[0].text.value
                    break
                
                elif run_status.status in ['failed', 'cancelled', 'expired']:
                    self.current_run_id = None

            self.current_run_id = None
            return "Please go ahead with your question."

        except Exception as e:
            self.current_run_id = None
            print(f"Error: {str(e)}")
            return "Please repeat your question."