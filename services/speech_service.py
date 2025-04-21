from google.cloud import speech
from google.cloud import storage
import logging

logger = logging.getLogger(__name__)

class SpeechService:
    """Handles audio transcription using Google Cloud Speech-to-Text."""
    
    def __init__(self):
        self.client = speech.SpeechClient()
        self.storage_client = storage.Client()

    def transcribe_audio(self, audio_content: bytes) -> str:
        """Convert audio bytes to text using Google Speech-to-Text."""
        try:
            client_stt = speech.SpeechClient()
            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.MP3,
                sample_rate_hertz=8000,
                language_code="en-US"
            )

            response = client_stt.recognize(config=config, audio=audio)

            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript

            return transcript
        except Exception as e:
            logger.error(f"Error in transcribe_audio: {str(e)}")
            raise

