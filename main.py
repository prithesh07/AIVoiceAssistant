import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.websockets import WebSocket
from contexts.conversation_context import ConversationContext
from services.ai_service import AIService
from protocols.twilio_protocol import TwilioProtocol
import logging
from google.cloud import speech

# Load environment variables
load_dotenv()
print("Environment variables loaded")

# Get service type from environment
service_type = os.getenv('SERVICE_TYPE', 'salon')

# Initialize FastAPI
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Application starting up...")

# Initialize services and contexts
conversation_context = ConversationContext()
ai_service = AIService(service_type=service_type)

streaming_config = speech.StreamingRecognitionConfig(
    config=speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MULAW,
        sample_rate_hertz=8000,
        language_code="en-US",
    ),
    interim_results=True
)

# Create single protocol instance
protocol = TwilioProtocol(
    conversation_context=conversation_context,
    ai_service=ai_service,
    streaming_config=streaming_config
)

# Routes
@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

# Define routes using service type
@app.post(f"/{service_type}/twilio-webhook")
async def handle_call(request: Request):
    return await protocol.handle_webhook(request)

@app.post(f"/{service_type}/handle-input")
async def handle_input(request: Request):
    return await protocol.handle_input(request)

@app.websocket(f"/{service_type}/stream")
async def media_stream(websocket: WebSocket):
    return await protocol.handle_stream(websocket)
