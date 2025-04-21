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
        self.streaming_config = streaming_config
        self.base_url = os.getenv('BASE_URL')
        self.websocket_url = os.getenv('WEBSOCKET_URL')

    async def handle_webhook(self, request: Request):
        """Handle initial webhook from Twilio."""
        try:
            form_data = await request.form()
            call_sid = form_data.get("CallSid")
            from_number = form_data.get("From")
            to_number = form_data.get("To")
            response = VoiceResponse()
            response.start().stream(
                url=self.websocket_url 
            )
            response.say("Hello, Welcome to our Salon. How may i assist you today?")
            gather = response.gather(
                input='speech', 
                timeout=5, 
                action=f"{self.base_url}/handle-input"
            )
            return Response(content=str(response), media_type="application/xml")
        except Exception as e:
            logger.error(f"Error in handle_twilio_call: {str(e)}", exc_info=True)
            error_response = VoiceResponse()
            error_response.say("I'm sorry, there was an error processing your request.")
            return Response(content=str(error_response), media_type="application/xml")

    async def handle_input(self, request: Request):
        """Handle speech input from user."""
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
                    action=f"{self.base_url}/handle-input"
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
        """Handle real-time audio stream from Twilio."""
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
        """Handle transcription results."""
        if not response.results:
            return
        result = response.results[0]
        if not result.alternatives:
            return
        transcription = result.alternatives[0].transcript
        if result.is_final:
            logger.info(f"Final transcription: {transcription}")
