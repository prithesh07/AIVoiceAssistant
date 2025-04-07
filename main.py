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

# Initialize FastAPI
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Application starting up...")

# Initialize services and contexts
conversation_context = ConversationContext()
ai_service = AIService()

streaming_config = speech.StreamingRecognitionConfig(
    config=speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MULAW,
        sample_rate_hertz=8000,
        language_code="en-US",
    ),
    interim_results=True
)

# Initialize services and contexts with streaming config
twilio_protocol = TwilioProtocol(
    conversation_context=conversation_context,
    ai_service=ai_service,
    streaming_config=streaming_config
)

# Routes
@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

@app.post("/twilio-webhook")
async def handle_twilio_call(request: Request):
    return await twilio_protocol.handle_webhook(request)

@app.post("/handle-input")
async def handle_input(request: Request):
    return await twilio_protocol.handle_input(request)

@app.websocket("/stream")
async def media_stream(websocket: WebSocket):
    return await twilio_protocol.handle_stream(websocket)
