from typing import List

class SalonTools:
    """Tools for the salon assistant"""
    @staticmethod
    def get_services() -> List[str]:
        """Get list of available salon services"""
        services = [
            "Haircut",
            "Hair Coloring",
            "Manicure",
            "Pedicure",
            "Facial",
            "Hair Styling",
            "Deep Conditioning",
            "Eyebrow Threading"
        ]
        return services

    @staticmethod
    def get_service_cost(service: str) -> str:
        """Get cost of a specific service"""
        costs = {
            "haircut": "$30",
            "hair coloring": "$75",
            "manicure": "$25",
            "pedicure": "$35",
            "facial": "$50",
            "hair styling": "$45",
            "deep conditioning": "$40",
            "eyebrow threading": "$15"
        }
        service_lower = service.lower()
        return costs.get(service_lower, "Service not found")

salon_tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "get_services",
            "description": "Get list of all available salon services",
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
            "name": "get_service_cost",
            "description": "Get the cost of a specific salon service",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "The name of the service"
                    }
                },
                "required": ["service"]
            }
        }
    }
]