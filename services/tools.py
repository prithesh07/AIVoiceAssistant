from typing import List, Dict
import datetime

class Tools:
    @staticmethod
    def get_current_time() -> str:
        """Get the current time"""
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def get_weather(city: str) -> str:
        """Mock weather information"""
        return f"The weather in {city} is sunny and 22°C"

tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current time",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather information for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name"
                    }
                },
                "required": ["city"]
            }
        }
    }
]