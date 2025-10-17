from typing import Any
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

RAPID_BASE_URL = os.getenv("RAPID_BASE_URL")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")


async def make_cheap_flight_request(
    from_city: str,
    to_city: str,
    depart_date: str,
    return_date: str,
    adults: int,
    infants: int,
    sort: str = "cheapest_first",
) -> dict[str, Any] | None:
    """Faz a requisição POST à API Google Flights com body JSON."""

    querystring = {
        "fromEntityId": f"{from_city}",
        "toEntityId": f"{to_city}",
        "departDate": f"{depart_date}",
        "returnDate": f"{return_date}",
        "adults": adults,
        "infants": infants,
        "sort": sort,
    }

    headers = {
        "x-rapidapi-key": "51f6508ab6mshc64a8ac071d5af2p1c120djsneac5d4d2fe4a",
        "x-rapidapi-host": "flights-search3.p.rapidapi.com",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(
                RAPID_BASE_URL, headers=headers, params=querystring
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Flight API request failed: {e}")
        return None
