from google.cloud import speech
from google.cloud import storage
import logging

logger = logging.getLogger(__name__)

class SpeechService:
    def __init__(self):
        self.client = speech.SpeechClient()
        self.storage_client = storage.Client()

    def transcribe_audio(self, audio_content: bytes) -> str:
        """
        Transcribe the given audio content (MP3 format) using Google Cloud Speech-to-Text.
        """
        logger.info(f"Transcribing audio of size: {len(audio_content)} bytes")
        try:
            client_stt = speech.SpeechClient()
            logger.debug("Google Speech-to-Text client initialized")

            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.MP3,
                sample_rate_hertz=8000,  # adjust sample rate if needed
                language_code="en-US"
            )
            logger.debug("Recognition config set up")

            logger.debug("Sending audio to Google for transcription")
            response = client_stt.recognize(config=config, audio=audio)
            logger.debug(f"Received transcription response with {len(response.results)} results")

            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript
                logger.debug(f"Transcript part: {result.alternatives[0].transcript}")

            logger.info(f"Final transcript: '{transcript}'")
            return transcript
        except Exception as e:
            logger.error(f"Error in transcribe_audio: {str(e)}")
            raise

