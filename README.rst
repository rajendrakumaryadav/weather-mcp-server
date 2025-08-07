
Weather MCP Server
==================

A Model Context Protocol (MCP) server that provides real-time weather alerts and forecasts for US locations using the National Weather Service (NWS) API.

Features
--------

- **Weather Alerts**: Get active weather alerts for any US state (e.g., severe weather, flood warnings, fire weather, etc.).
- **Weather Forecasts**: Retrieve detailed weather forecasts for any latitude/longitude in the US (up to 5 periods ahead).
- **Health Check**: Simple tool to verify the server is running.
- **MCP Root Tool**: Describes the server and available tools for easy discovery.

Requirements
------------

- Python 3.13+
- `uv <https://github.com/astral-sh/uv>`_ (for fast dependency management)
- fastmcp>=2.11.0
- httpx>=0.28.1
- mcp[cli]>=1.12.3

Installation
------------

1. **Clone the repository:**

   .. code-block:: bash

      git clone https://github.com/rajendrakumaryadav/weather-mcp-server.git
      cd weather-mcp-server


Interact with the Server Using the Example Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The repository includes an example async client in ``mcp_client.py`` that demonstrates how to connect to the server and call its tools:

.. code-block:: bash

   uv run mcp_client.py

The client will:

- List available tools
- Call the ``root`` tool to get server info
- Call the ``health_check`` tool
- Call the ``get_alerts`` tool for California (CA)
- Call the ``get_forecast`` tool for Los Angeles (34.0522, -118.2437)

You should see output similar to:

.. code-block:: text

   Connecting to Weather MCP server at http://127.0.0.1:8000/mcp...
   [Tool(name='root', ...), Tool(name='health_check', ...), Tool(name='get_alerts', ...), Tool(name='get_forecast', ...)]
   ✅ Successfully connected to the server.

   --- Calling root tool for server info ---
   ✅ Server Info:
   rootOutput(result='Weather MCP Server: Provides weather alerts and forecasts for US locations.\nAvailable tools:\n- get_alerts(state: str): Get weather alerts for a US state.\n- get_forecast(latitude: float, longitude: float): Get weather forecast for a location.\n- health_check(): Check if the server is running.\n')

   --- Calling health_check ---
   ✅ Server Response: health_checkOutput(result='Weather MCP server is running.')

   --- Calling get_alerts for California (CA) ---
   ✅ Server Response:
   get_alertsOutput(result='\nEvent: Extreme Heat Warning\nArea: San Gorgonio Pass Near Banning\nSeverity: Severe\nDescription: * WHAT...Dangerously hot conditions with temperatures up to 114.\n...\n')

   --- Calling get_forecast for Los Angeles (34.05, -118.24) ---
   ✅ Server Response:
   get_forecastOutput(result='\nToday:\nTemperature: 91°F\nWind: 5 to 10 mph SW\nForecast: Patchy fog before 11am. Mostly sunny, with a high near 91. Southwest wind 5 to 10 mph.\n...\n')

Available Tools
~~~~~~~~~~~~~~~

- ``get_alerts(state: str)``
  - Get weather alerts for a US state (e.g., ``CA``, ``NY``, ``AL``).
- ``get_forecast(latitude: float, longitude: float)``
  - Get weather forecast for a specific location (e.g., San Francisco: ``37.7749, -122.4194``).
- ``health_check()``
  - Check if the server is running.
- ``root()``
  - Describe the server and its available tools.

API Reference
-------------

.. list-table::
   :header-rows: 1

   * - Tool
     - Arguments
     - Returns
   * - get_alerts
     - state: str
     - Formatted weather alerts for the given US state code
   * - get_forecast
     - latitude: float, longitude: float
     - Formatted weather forecast for the given coordinates (next 5 periods)
   * - health_check
     - None
     - Simple message indicating the server is running
   * - root
     - None
     - Describes the server and lists available tools

Walkthrough: How to Use and Configure
-------------------------------------

Below is a visual of running the MCP client:

.. figure:: resources/preview-mcp-client.png
   :alt: Connecting to the Weather MCP Server with MCP Client
   :width: 600

   **Running MCP with MCP client**

   This image shows how to set up and run the MCP client from the command line.

License
-------

MIT License. See ``LICENSE`` for details.

Acknowledgments
---------------

- `National Weather Service API <https://www.weather.gov/documentation/services-web-api>`_
- `fastmcp <https://gofastmcp.com/getting-started/welcome>`_
- `httpx <https://www.python-httpx.org/>`_
- `MCP Protocol <https://modelcontextprotocol.io/overview>`_
- `Build an MCP Server <https://modelcontextprotocol.io/quickstart/server>`_