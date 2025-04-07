import asyncio
from google.cloud import speech
from queue import Queue

class SpeechClientBridge:
    def __init__(self, streaming_config, callback):
        self._callback = callback
        self._streaming_config = streaming_config
        self._client = speech.SpeechClient()
        self._queue = Queue()
        self._ended = False
        self._loop = asyncio.get_event_loop()

    def start(self):
        while not self._ended:
            requests = self._request_generator()
            responses = self._client.streaming_recognize(self._streaming_config, requests)
            
            try:
                for response in responses:
                    # Run callback in the event loop
                    asyncio.run_coroutine_threadsafe(
                        self._callback(response), 
                        self._loop
                    )
            except Exception as e:
                print(f"Error in streaming recognize: {e}")
                break

    def _request_generator(self):
        while not self._ended:
            chunk = self._queue.get()
            if chunk is None:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    def add_request(self, chunk):
        self._queue.put(chunk)

    def terminate(self):
        self._ended = True
        self._queue.put(None)