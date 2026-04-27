import asyncio
import os
import json
from app.config import settings
from bot.dispatcher import Dispatcher
from bot.formatter import format_response

# Ensure Groq API Key is set
os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

async def test_operation(dispatcher, query, telegram_id=5046300090):
    print(f"\n--- Testing Query: '{query}' ---")
    from llm.intent_router import detect_intent
    
    # 1. Detect Intent
    intent = detect_intent(query, telegram_id)
    print(f"[Intent] {intent}")
    
    # 2. Dispatch
    result = await dispatcher.dispatch(intent)
    print(f"[Result] {result}")
    
    # 3. Format
    formatted = format_response(result)
    print(f"[Formatted] {formatted}")

async def main():
    print("Initializing Dispatcher and MCP Client...")
    dispatcher = Dispatcher()
    await dispatcher.mcp_client.connect()
    
    try:
        # Test 1: Insert Product (Verification of 'product_name' param)
        await test_operation(dispatcher, "add a monitor to electronics")
        
        # Test 2: Search Product
        await test_operation(dispatcher, "search for television")
        
        # Test 3: Check Exists
        await test_operation(dispatcher, "is television in the database?")
        
        # Test 4: Delete Product
        await test_operation(dispatcher, "delete product television")
        
        # Test 5: Fetch All
        await test_operation(dispatcher, "show all products")

    finally:
        print("\nClosing MCP Connection...")
        # Note: MCP client usually handles cleanup, but we can exit gracefully
        pass

if __name__ == "__main__":
    asyncio.run(main())
