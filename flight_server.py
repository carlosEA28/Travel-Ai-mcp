import os
import sys
from typing import List, Dict, Any

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from helpers.flight.index import make_cheap_flight_request

load_dotenv()

RAPID_BASE_URL = os.getenv("RAPID_BASE_URL")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

if not RAPID_BASE_URL or not RAPID_API_KEY:
    print(
        "FATAL ERROR: Environment variables RAPID_BASE_URL and/or RAPID_API_KEY are not set in the .env file."
    )
    print("Please check your .env file.")
    sys.exit(1)

flight_mcp = FastMCP(
    "Flight Server",
    stateless_http=True,
)


@flight_mcp.tool()
async def get_flight_info(
    from_city: str,
    to_city: str,
    depart_date: str,
    return_date: str,
    adults: int,
    infants: int,
    sort: str = "cheapest_first",
):
    """Get flight info for a location and format it into a descriptive string."""
    try:
        flight_data = await make_cheap_flight_request(
            from_city,
            to_city,
            depart_date,
            return_date,
            adults,
            infants,
            sort,
        )

        if not flight_data:
            return "CRITICAL ERROR: No data returned from the flight API."

        if "data" not in flight_data or "itineraries" not in flight_data["data"]:
            return f"CRITICAL ERROR: Unexpected API response structure: {flight_data}"

        itineraries = flight_data["data"]["itineraries"]
        results = [f"Here are the flights from {from_city} to {to_city}:\n"]

        for itinerary in itineraries:
            price = itinerary.get("price", {}).get("formatted", "N/A")
            for leg in itinerary.get("legs", []):
                origin = leg["origin"]["city"]
                dest = leg["destination"]["city"]
                depart = leg["departure"]
                arrive = leg["arrival"]
                stops = leg.get("stopCount", 0)
                carriers = ", ".join(
                    [c["name"] for c in leg.get("carriers", {}).get("marketing", [])]
                )

                results.append(
                    f"- Flight from {origin} to {dest}, "
                    f"Departure: {depart}, Arrival: {arrive}, "
                    f"Stops: {stops}, Airlines: {carriers}, Price: {price}"
                )

        return "\n".join(results)

    except Exception as e:
        return f"CRITICAL ERROR: Failed to process flight data: {type(e).__name__} - {str(e)}"
