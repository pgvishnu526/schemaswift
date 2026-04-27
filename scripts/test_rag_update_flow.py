import asyncio
import os
from app.config import settings
from bot.dispatcher import Dispatcher
from bot.formatter import format_response
from llm.intent_router import detect_intent
from rag.index_builder import update_user_embeddings

os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

async def test_flow():
    d = Dispatcher()
    await d.mcp_client.connect()
    
    print("\n1. Initializing embeddings...")
    update_user_embeddings()
    
    print("\n2. Initial RAG Query...")
    intent_rag1 = detect_intent("who are the current users", 123)
    res1 = await d.dispatch(intent_rag1)
    print(f"RAG Result 1: {format_response(res1)}")
    
    print("\n3. Inserting a product (triggers update_embeddings)...")
    intent_ins = {
        'action': 'insert_product',
        'parameters': {'product_name': 'test_product', 'category': 'Electronics'},
        'telegram_id': 5046300090,
        'message': 'add test_product'
    }
    res_ins = await d.dispatch(intent_ins)
    print(f"Insert Result: {format_response(res_ins)}")
    
    print("\n4. Second RAG Query (checking for stale collection)...")
    intent_rag2 = detect_intent("Summarize the system activity", 123)
    res2 = await d.dispatch(intent_rag2)
    print(f"RAG Result 2: {format_response(res2)}")

if __name__ == "__main__":
    asyncio.run(test_flow())
