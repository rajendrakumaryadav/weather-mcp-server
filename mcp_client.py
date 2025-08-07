import asyncio

# The server uses FastMCP, so we should use the Client from the fastmcp library.
from fastmcp import Client

# The base URL where your FastMCP server is running, including the /mcp endpoint.
SERVER_BASE_URL = "http://127.0.0.1:8000/mcp"


async def main():
    """
    An example client to interact with the Weather MCP server.
    It demonstrates the correct usage of the FastMCP client with an
    async context manager and the call_tool method.
    """
    print(f"Connecting to Weather MCP server at {SERVER_BASE_URL}...")

    # Initialize the client with the server's base URL.
    client = Client(SERVER_BASE_URL)

    async with client:
        print(await client.list_tools())

    # Use the client as an async context manager to handle the connection.
    async with client:
        print("✅ Successfully connected to the server.")

        # --- 1. Call the root tool to get server info ---
        print("\n--- Calling root tool for server info ---")
        try:
            # Call the 'root' tool which describes the server's capabilities.
            root_response = await client.call_tool("root", {})
            print("✅ Server Info:")
            print(root_response.data)
        except Exception as e:
            print(f"❌ Error calling root: {e}")

        # --- 2. Call the health_check tool ---
        print("\n--- Calling health_check ---")
        try:
            health_response = await client.call_tool("health_check", {}, timeout=10)
            print(f"✅ Server Response: {health_response.data}")
        except Exception as e:
            print(f"❌ Error calling health_check: {e}")

        # --- 3. Call the get_alerts tool for California (CA) ---
        print("\n--- Calling get_alerts for California (CA) ---")
        try:
            alerts_response = await client.call_tool(
                "get_alerts", {"state": "CA"}, timeout=30
            )
            print("✅ Server Response:")
            print(alerts_response.data)
        except Exception as e:
            print(f"❌ Error calling get_alerts: {e}")

        # --- 4. Call the get_forecast tool for Los Angeles ---
        print("\n--- Calling get_forecast for Los Angeles (34.05, -118.24) ---")
        try:
            forecast_response = await client.call_tool(
                "get_forecast",
                {"latitude": 34.0522, "longitude": -118.2437},
                timeout=30,
            )
            print("✅ Server Response:")
            print(forecast_response.data)
        except Exception as e:
            print(f"❌ Error calling get_forecast: {e}")


if __name__ == "__main__":
    # Ensure you have the necessary libraries installed:
    # pip install "uagents[mcp]"
    # or if using uv:
    # uv pip install "uagents[mcp]"
    asyncio.run(main())
