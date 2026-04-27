def format_response(response: dict) -> str:
    """
    Formats MCP tool response dicts into user-friendly Telegram messages.
    Telegram supports unicode emoji natively, so we use them here.
    """
    if not isinstance(response, dict):
        return str(response)

    # Error case
    if "error" in response and response.get("success") is False:
        return f"Error: {response['error']}"

    # RAG Response
    if response.get("mode") == "rag":
        answer = response.get("answer", "No answer generated.")
        source = response.get("source", "Unknown source")
        return f"{answer}\n\n[Source: {source}]"

    # Message response
    if "message" in response:
        msg = response["message"]
        return msg

    # Product list response
    if "products" in response:
        products = response["products"]
        if not products:
            return "No products found."

        lines = ["Available Products:\n"]
        for p in products:
            name = p.get("name", "Unknown")
            category = p.get("category", "Uncategorized")
            pid = p.get("id", "?")
            lines.append(f"  {pid}. {name} ({category})")

        return "\n".join(lines)

    # Role response
    if "role" in response:
        role = response["role"]
        return f"Your role: {role}"

    # Fallback
    return str(response)