
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

VIBE_QUERIES = {
    "romantic": "romantic date night intimate dining",
    "upscale": "upscale fine dining elegant",
    "chill": "cozy quiet relaxed dining",
    "lively": "lively fun energetic dining",
    "casual": "casual laid back dining",
}


@st.cache_data(ttl=1800, show_spinner=False)
def search_restaurants(
    location,
    cuisine,
    limit=20,
    vibe=None,
    restaurant_type="all restaurants"
):
    api_key = st.secrets["GOOGLE_PLACES_API_KEY"]

    location = location.strip()
    cuisine = cuisine.strip().lower()
    vibe = (vibe or "").strip().lower()

    if restaurant_type == "fast food / quick bites":
        query = f"{cuisine} fast food quick bites in {location}"
    else:
        mood = VIBE_QUERIES.get(vibe, "")
        query = f"{mood} {cuisine} restaurants in {location}"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": (
            "places.id,places.displayName,places.rating,"
            "places.userRatingCount,places.priceLevel,"
            "places.types,places.primaryType,"
            "places.googleMapsUri,places.businessStatus"
        ),
    }

    body = {
        "textQuery": query,
        "pageSize": min(max(limit, 1), 20),
        "minRating": 4.0,
    }

    response = requests.post(
        GOOGLE_URL,
        headers=headers,
        json=body,
        timeout=20
    )

    if not response.ok:
        raise RuntimeError(
            f"Google Places search failed ({response.status_code}). "
            "Check your API configuration and quotas."
        )

    restaurants = []

    for place in response.json().get("places", []):
        if place.get("businessStatus") == "CLOSED_PERMANENTLY":
            continue

        types = place.get("types", [])

        categories = [
            {
                "alias": category,
                "title": category.replace("_", " ")
            }
            for category in types
        ]

        restaurants.append({
            "id": place.get("id"),
            "name": place.get(
                "displayName", {}
            ).get("text", "Unknown restaurant"),
            "rating": place.get("rating", 0),
            "rating_count": place.get("userRatingCount", 0),
            "price": PRICE_LEVELS.get(
                place.get("priceLevel"), ""
            ),
            "categories": categories,
            "primary_type": place.get("primaryType", ""),
            "url": place.get("googleMapsUri", ""),
            "search_vibes": [vibe] if vibe else [],
            "search_cuisines": [cuisine],
        })

    return restaurants
