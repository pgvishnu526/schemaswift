from bot.mcp_client import MCPClient
from llm.rag_response import generate_rag_response


class Dispatcher:
    """
    Routes parsed intents to MCP tool calls.
    """

    def __init__(self):
        self.mcp_client = MCPClient()

    async def dispatch(self, intent: dict) -> dict:
        """
        Takes an intent dict from the LLM and calls the appropriate MCP tool.
        """
        action = intent.get("action")

        if action == "help":
            return {"message": "You can ask me to:\n"
                               "- 'Show all products'\n"
                               "- 'Add laptop to electronics'\n"
                               "- 'Delete product 3'\n"
                               "- 'Register me as John'\n"
                               "- 'What is my role?'\n"
                               "- 'I want admin access'"}

        if action == "rag_query":
            message = intent.get("message", "")
            return generate_rag_response(message)

        # Build arguments: extract from 'parameters' if present, otherwise root, and ensure telegram_id is included
        arguments = intent.get("parameters", {})

        # Add telegram_id explicitly since it's added at root in intent_router
        if "telegram_id" in intent:
            arguments["telegram_id"] = intent["telegram_id"]
        
        # Add name explicitly for access requests
        if "name" in intent:
            arguments["name"] = intent["name"]

        result = await self.mcp_client.call_tool(action, arguments)

        return result