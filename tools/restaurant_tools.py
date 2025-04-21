from typing import List, Dict

class RestaurantTools:
    """Tools for the restaurant assistant"""
    
    @staticmethod
    def get_menu() -> List[str]:
        """Get list of available menu items"""
        menu = [
            "Pizza Margherita",
            "Pasta Carbonara",
            "Caesar Salad",
            "Grilled Chicken",
            "Fish and Chips",
            "Vegetable Curry",
            "Chocolate Cake",
            "Ice Cream"
        ]
        return menu

    @staticmethod
    def get_item_price(item: str) -> str:
        """Get price of a specific menu item"""
        prices = {
            "pizza margherita": "$12",
            "pasta carbonara": "$15",
            "caesar salad": "$10",
            "grilled chicken": "$18",
            "fish and chips": "$16",
            "vegetable curry": "$14",
            "chocolate cake": "$8",
            "ice cream": "$6"
        }
        item_lower = item.lower()
        return prices.get(item_lower, "Item not found")

    @staticmethod
    def check_availability(item: str) -> bool:
        """Check if an item is available"""
        menu = [item.lower() for item in RestaurantTools.get_menu()]
        return item.lower() in menu

restaurant_tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Get list of all available menu items",
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
            "name": "get_item_price",
            "description": "Get the price of a specific menu item",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The name of the menu item"
                    }
                },
                "required": ["item"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check if a menu item is available",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The name of the menu item"
                    }
                },
                "required": ["item"]
            }
        }
    }
]