import os
from fastapi import Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
from contexts.conversation_context import ConversationContext
from services.ai_service import AIService
import logging
import json
import base64
import threading
from services.speech_client_service import SpeechClientService

logger = logging.getLogger(__name__)

class TwilioProtocol:
    """Handles Twilio webhook, input, and streaming."""

    def __init__(
        self, 
        conversation_context: ConversationContext, 
        ai_service: AIService,
        streaming_config=None
    ):
        self.context = conversation_context
        self.ai_service = ai_service
        self.service_type = ai_service.service_type
        self.streaming_config = streaming_config
        self.base_url = os.getenv('BASE_URL')
        self.websocket_url = os.getenv('WEBSOCKET_URL')

    async def handle_webhook(self, request: Request):
        """Processes initial Twilio webhook and sets up voice response."""
        try:
            form_data = await request.form()
            call_sid = form_data.get("CallSid")
            response = VoiceResponse()

            service_websocket_url = f"{self.base_url}/{self.service_type}/stream"
            service_action_url = f"{self.base_url}/{self.service_type}/handle-input"

            response.start().stream(
                url=service_websocket_url
            )

            welcome_message = (
                "Hello, Welcome to our Restaurant. How may I assist you today?"
                if self.service_type == "restaurant"
                else "Hello, Welcome to our Salon. How may I assist you today?"
            )
            response.say(welcome_message)

            gather = response.gather(
                input='speech',
                timeout=5,
                action=service_action_url
            )

            return Response(content=str(response), media_type="application/xml")
        except Exception as e:
            logger.error(f"Error in handle_webhook: {str(e)}", exc_info=True)
            error_response = VoiceResponse()
            error_response.say("I'm sorry, there was an error processing your request.")
            return Response(content=str(error_response), media_type="application/xml")

    async def handle_input(self, request: Request):
        """Processes user speech input and generates AI response."""
        try:
            form_data = await request.form()
            call_sid = form_data.get("CallSid")
            speech_result = form_data.get("SpeechResult")
            if speech_result:
                conversation = self.context.get_or_create_conversation(call_sid)
                conversation.add_message(speech_result, "user")
                ai_response = await self.ai_service.get_response(speech_result)
                conversation.add_message(ai_response, "ai")
                response = VoiceResponse()
                response.say(ai_response)
                gather = response.gather(
                    input='speech', 
                    timeout=5, 
                    action=f"{self.base_url}/{self.service_type}/handle-input"
                )
                return Response(content=str(response), media_type="application/xml")
            response = VoiceResponse()
            gather = response.gather(
                input='speech', 
                timeout=5, 
                action=f"{self.base_url}/handle-input"
            )
            return Response(content=str(response), media_type="application/xml")
        except Exception as e:
            logger.error(f"Error handling input: {str(e)}")
            error_response = VoiceResponse()
            error_response.say("I'm sorry, there was an error processing your request.")
            return Response(content=str(error_response), media_type="application/xml")

    async def handle_stream(self, websocket):
        """Manages real-time audio streaming from Twilio."""
        bridge = None
        try:
            await websocket.accept()
            bridge = SpeechClientService(self.streaming_config, self.on_transcription_response)
            t = threading.Thread(target=bridge.start)
            t.start()
            while True:
                try:
                    message = await websocket.receive_text()
                    data = json.loads(message)
                    if data["event"] in ("connected", "start"):
                        continue
                    if data["event"] == "media":
                        media = data["media"]
                        chunk = base64.b64decode(media["payload"])
                        bridge.add_request(chunk)
                    if data["event"] == "stop":
                        bridge.add_request(None)
                        bridge.terminate()
                        break
                except Exception as e:
                    logger.error(f"Error in stream loop: {str(e)}", exc_info=True)
                    break
        except Exception as e:
            logger.error(f"Error in media stream: {str(e)}", exc_info=True)
        finally:
            if bridge:
                bridge.terminate()
            logger.info("WebSocket connection closed")

    async def on_transcription_response(self, response):
        """Handles transcription results from speech recognition."""
        if not response.results:
            return
        result = response.results[0]
        if not result.alternatives:
            return
        transcription = result.alternatives[0].transcript
        if result.is_final:
            logger.info(f"Final transcription: {transcription}")
