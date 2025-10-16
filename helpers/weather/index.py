from typing import Any
import httpx


async def make_weather_request(url: str) -> dict[str, Any] | None:
    """Make a request to the  TOMORROW IO API with proper error handling"""

    headers = {"accept": "application/json", "accept-encoding": "deflate, gzip, br"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
