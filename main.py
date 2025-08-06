from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

"""
Weather MCP Server
------------------
Provides weather alerts and forecasts for US locations using the National Weather Service API.
Tools:
  - get_alerts(state: str): Get weather alerts for a US state.
  - get_forecast(latitude: float, longitude: float): Get weather forecast for a location.
  - health_check(): Check if the server is running.
  - root(): Describe the server and available tools.
"""


mcp = FastMCP("weather")


@mcp.tool()
def root() -> str:
    """Describe the Weather MCP server and its available tools."""
    return (
        "Weather MCP Server: Provides weather alerts and forecasts for US locations.\n"
        "Available tools:\n"
        "- get_alerts(state: str): Get weather alerts for a US state.\n"
        "- get_forecast(latitude: float, longitude: float): Get weather forecast for a location.\n"
        "- health_check(): Check if the server is running.\n"
    )


@mcp.tool()
def health_check() -> str:
    """Check if the Weather MCP server is running."""
    return "Weather MCP server is running."


NWS_API_BASE_URL: str = "https://api.weather.gov"
USER_AGENT: str = "weather-app/v1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a US state.

    Args:
        state (str): Two-letter US state code (e.g. CA, NY)
    Returns:
        str: Formatted weather alerts or a message if none found.
    """
    url = f"{NWS_API_BASE_URL}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get weather forecast for a location.

    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location
    Returns:
        str: Formatted weather forecast for the next 5 periods.
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE_URL}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


if __name__ == "__main__":
    mcp.run(transport="stdio")
