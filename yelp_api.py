
import requests
import streamlit as st

GOOGLE_URL = "https://places.googleapis.com/v1/places:searchText"

PRICE_LEVELS = {
    "PRICE_LEVEL_FREE": "$",
    "PRICE_LEVEL_INEXPENSIVE": "$",
    "PRICE_LEVEL_MODERATE": "$$",
    "PRICE_LEVEL_EXPENSIVE": "$$$",
    "PRICE_LEVEL_VERY_EXPENSIVE": "$$$$",
}

def search_restaurants(location, cuisine, limit=10):
    api_key = st.secrets["GOOGLE_PLACES_API_KEY"]

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": (
            "places.id,places.displayName,places.rating,"
            "places.priceLevel,places.types,"
            "places.googleMapsUri"
        ),
    }

    body = {
        "textQuery": f"{cuisine} restaurants in {location}",
        "pageSize": min(limit, 20),
    }

    response = requests.post(
        GOOGLE_URL,
        headers=headers,
        json=body,
        timeout=15,
    )

    if not response.ok:
        raise Exception(
            f"Google Places request failed: {response.status_code}"
        )

    restaurants = []

    for place in response.json().get("places", []):
        types = place.get("types", [])
        categories = [
            {
                "alias": t,
                "title": t.replace("_", " ")
            }
            for t in types
        ]

        if cuisine.lower() == "fast food":
            categories.append({
                "alias": "fastfood",
                "title": "fast food"
            })
        else:
            categories.append({
                "alias": cuisine.lower(),
                "title": cuisine.lower()
            })

        restaurant = {
            "id": place.get("id"),
            "name": place.get("displayName", {}).get("text", ""),
            "rating": place.get("rating", 0),
            "price": PRICE_LEVELS.get(
                place.get("priceLevel"), ""
            ),
            "categories": categories,
            "url": place.get("googleMapsUri", ""),
        }

        restaurants.append(restaurant)

    return restaurants
