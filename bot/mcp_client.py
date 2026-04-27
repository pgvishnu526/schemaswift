import sys
import json
import os
from contextlib import AsyncExitStack
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class MCPClient:

    def __init__(self):
        self.session = None
        self._exit_stack = AsyncExitStack()

    async def connect(self):
        """
        Connect to MCP server using stdio transport.
        Spawns the MCP server as a subprocess.
        """
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_server.run_server"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            env=None
        )

        # stdio_client is an async context manager that yields (read, write) streams
        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        self._read_stream, self._write_stream = stdio_transport

        # Create and initialize the session
        self.session = await self._exit_stack.enter_async_context(
            ClientSession(self._read_stream, self._write_stream)
        )

        await self.session.initialize()

        # List available tools for verification
        tools_result = await self.session.list_tools()
        tool_names = [t.name for t in tools_result.tools]
        print(f"MCP connected. Available tools: {tool_names}")

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """
        Execute an MCP tool and return parsed result.
        MCP tools return CallToolResult with content items.
        """
        if not self.session:
            raise RuntimeError("MCP session not initialized. Call connect() first.")

        try:
            result = await self.session.call_tool(
                tool_name,
                arguments=arguments
            )

            # result is a CallToolResult with .content list
            # Each content item has .text for TextContent
            if result.content:
                text = result.content[0].text
                try:
                    return json.loads(text)
                except (json.JSONDecodeError, TypeError):
                    return {"message": text}
            else:
                return {"message": "Tool executed successfully (no output)."}

        except Exception as e:
            return {"error": str(e), "success": False}

    async def close(self):
        """
        Gracefully close MCP session and subprocess.
        """
        await self._exit_stack.aclose()