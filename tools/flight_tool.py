import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")


def extract_city(query):

    supported_cities = [
        "delhi",
        "mumbai",
        "patna",
        "tokyo",
        "paris",
        "dubai",
        "bangkok",
        "rome",
        "london",
        "new york",
    ]

    query_lower = query.lower()

    matched = []

    for city in supported_cities:
        if city in query_lower:
            matched.append(city)

    return matched


def format_flight_card(
    airline,
    departure,
    arrival,
    status
):

    return f"""
✈️ Airline: {airline}

🛫 Departure: {departure}

🛬 Arrival: {arrival}

📌 Status: {status}

━━━━━━━━━━━━━━━━━━
"""


def search_flights(query):

    url = "http://api.aviationstack.com/v1/flights"

    params = {
        "access_key": API_KEY,
        "limit": 15
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

    except Exception:

        return """
⚠️ Unable to fetch live flight data currently.

Please try again later.
"""

    if "data" not in data:
        return "⚠️ No flight data available."

    detected_cities = extract_city(query)

    flights = []

    seen_routes = set()

    for flight in data["data"]:

        airline = flight.get(
            "airline", {}
        ).get("name", "Unknown Airline")

        departure = flight.get(
            "departure", {}
        ).get("airport", "Unknown Departure")

        arrival = flight.get(
            "arrival", {}
        ).get("airport", "Unknown Arrival")

        status = flight.get(
            "flight_status",
            "Scheduled"
        )

        combined_text = f"""
        {departure}
        {arrival}
        """.lower()

        if detected_cities:

            matched = any(
                city in combined_text
                for city in detected_cities
            )

            if not matched:
                continue

        route_key = f"{departure}-{arrival}"

        if route_key in seen_routes:
            continue

        seen_routes.add(route_key)

        flights.append(
            format_flight_card(
                airline,
                departure,
                arrival,
                status
            )
        )

        if len(flights) >= 5:
            break

    if not flights:

        return """
⚠️ No relevant flights found for your route.

Try searching for major destinations like:
Delhi, Tokyo, Dubai, Paris, or Bangkok.
"""

    return "\n".join(flights)

