import asyncio
from bot.mcp_client import MCPClient


async def test():
    """Quick test to verify MCP server connection and tool listing."""

    client = MCPClient()

    print("Connecting to MCP server...")
    await client.connect()
    print("Connected!")

    # Test: fetch products
    print("\nTesting fetch_products...")
    result = await client.call_tool("fetch_products", {"telegram_id": 0})
    print(f"Result: {result}")

    # Test: register a test user
    print("\nTesting register_user...")
    result = await client.call_tool("register_user", {
        "telegram_id": 999999,
        "name": "TestUser"
    })
    print(f"Result: {result}")

    # Test: get user role
    print("\nTesting get_user_role...")
    result = await client.call_tool("get_user_role", {
        "telegram_id": 999999
    })
    print(f"Result: {result}")

    await client.close()
    print("\nAll tests passed!")


if __name__ == "__main__":
    asyncio.run(test())