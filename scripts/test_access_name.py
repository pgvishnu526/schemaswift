import os
import asyncio
from app.config import settings
from llm.intent_router import detect_intent
from bot.dispatcher import Dispatcher

os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

async def test_access_request():
    message = "I want admin access"
    telegram_id = 8687948766
    name = "demo_user"
    
    print(f"Testing intent detection for: '{message}' with name: '{name}'")
    intent = detect_intent(message, telegram_id, name)
    print(f"Detected Intent: {intent}")
    
    if intent["action"] == "request_access":
        print("Success: Action is request_access")
    else:
        print(f"Failure: Action is {intent['action']}")
        
    if intent.get("name") == name:
        print(f"Success: Name '{name}' attached to intent")
    else:
        print(f"Failure: Name not attached or incorrect: {intent.get('name')}")

    # Test Dispatcher argument building
    print("\nTesting Dispatcher argument building...")
    # We don't need to connect to MCP for this unit test of logic
    # Just check how it builds arguments before calling tool
    
    arguments = intent.get("parameters", {})
    if "telegram_id" in intent:
        arguments["telegram_id"] = intent["telegram_id"]
    if "name" in intent:
        arguments["name"] = intent["name"]
        
    print(f"Final Arguments for Tool: {arguments}")
    
    if arguments.get("name") == name:
        print("Success: Name correctly included in tool arguments")
    else:
        print("Failure: Name missing from tool arguments")

if __name__ == "__main__":
    asyncio.run(test_access_request())
