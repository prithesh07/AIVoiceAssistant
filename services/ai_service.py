import requests
import logging
import os

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = "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"
        self.api_url = 'https://api.groq.com/openai/v1/chat/completions'

    async def get_response(self, user_message: str):
        logger.info(f"Getting AI response for message: '{user_message}'")
        try:
            # Use your actual API key here.
            api_key = "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"
            logger.debug("API key loaded")
            
            data = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "Assume you are running a Salon. Keep the coversation short and to the point."},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 50
            }
            logger.debug(f"AI request data prepared: {data}")
            
            headers = {
                'Authorization': f"Bearer {api_key}",
                'Content-Type': 'application/json'
            }
            
            logger.debug("Sending request to AI API")
            resp = requests.post(self.api_url, json=data, headers=headers)
            logger.info(f"AI API response status: {resp.status_code}")
            
            if resp.status_code == 200:
                response_data = resp.json()
                logger.debug(f"AI response data: {response_data}")
                ai_reply = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                logger.info(f"AI reply: '{ai_reply}'")
                return ai_reply
            else:
                logger.error(f"Error {resp.status_code} from AI API: {resp.text}")
                return "Sorry, I couldn't get a response from the AI."
        except Exception as e:
            logger.error(f"Error communicating with AI: {str(e)}", exc_info=True)
            return "Sorry, there was an issue communicating with the AI."