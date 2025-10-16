import json
import os
import sys
from typing import Any, Dict

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from helpers.weather.index import make_weather_request, weather_code_to_string

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
    """Get current weather for a location and format it into a descriptive string.

    Args:
        city: Name of the city to get weather for

    Returns:
        Dict[str, Any]: A formatted json with the weather information containing text and raw data or error message
    """
    url = (
        f"{TOMORROW_IO_BASE_URL}/realtime?location={city}&apikey={TOMORROW_IO_API_KEY}"
    )

    try:
        weather_data = await make_weather_request(url)
        values = weather_data["data"]["values"]

        temp_c = values.get("temperature", "N/A")
        code = values.get("weatherCode", 0)
        condition = weather_code_to_string(code)
        wind_speed = values.get("windSpeed", "N/A")
        humidity = values.get("humidity", "N/A")

        formatted_output = (
            f"The current weather in {city} is {condition}.\n"
            f"Temperature: {temp_c}°C.\n"
            f"Wind Speed: {wind_speed} m/s.\n"
            f"Humidity: {humidity}%."
        )

        return {
            "text": formatted_output,
            "raw": weather_data,
        }

    except KeyError as e:
        return f"ERROR: Weather data was retrieved but had an unexpected structure: {str(e)}"
    except Exception as e:
        return f"CRITICAL ERROR: Failed to process weather data: {type(e).__name__} - {str(e)}"
