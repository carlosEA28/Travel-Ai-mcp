import json
import os
import sys
from typing import Any, Dict
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from helpers.weather.index import make_weather_request

load_dotenv()

TOMORROW_IO_BASE_URL = os.getenv("TOMORROW_IO_BASE_URL")
TOMORROW_IO_API_KEY = os.getenv("TOMORROW_IO_API_KEY")


if not TOMORROW_IO_BASE_URL or not TOMORROW_IO_API_KEY:
    print(
        "FATAL ERROR: Environment variables TOMORROW_IO_BASE_URL and/or TOMORROW_IO_API_KEY are not set in the .env file."
    )
    print("Please check your .env file.")
    sys.exit(1)


weather_mcp = FastMCP(
    "Weather Server",
    stateless_http=True,
)


@weather_mcp.tool()
async def get_current_location_weather(city: str) -> Dict[str, Any]:
    """Get current weather for a location."""

    url = (
        f"{TOMORROW_IO_BASE_URL}/realtime?location={city}&apikey={TOMORROW_IO_API_KEY}"
    )

    try:
        weather_data = await make_weather_request(url)
    except Exception as e:

        print(f"Error fetching weather data for {city}: {e}", file=sys.stderr)

        return {"error": f"Internal API request failed: {type(e).__name__}"}

    if not weather_data:
        return {"error": "Unable to fetch the current weather or received empty data"}

    return json.loads(json.dumps(weather_data))
