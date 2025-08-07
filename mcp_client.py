import asyncio

# The server uses FastMCP, so we should use the Client from the fastmcp library.
from fastmcp import Client

# The base URL where your FastMCP server is running
SERVER_BASE_URL = "http://127.0.0.1:8000/mcp"


async def main():
    """
    An example client to interact with the Weather MCP server.
    It demonstrates the correct usage of the FastMCP client with an
    async context manager and the call_tool method.
    """
    print(f"Connecting to Weather MCP server at {SERVER_BASE_URL}...")

    # Initialize the client with the server's base URL.
    async with Client(SERVER_BASE_URL) as client:
        # Attempt to connect to the server.
        if client.is_connected():
            print("✅ Successfully connected to the server.")
        else:
            print("❌ Failed to connect to the server.")
            return
        # Ensure the client is connected to the server.
        data = await client.list_resources()
        print("✅ Connected to server. Available resources:")
        for resource in data:
            print(f" - {resource}")


if __name__ == "__main__":
    asyncio.run(main())
