import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("YELP_API_KEY")

URL = "https://api.yelp.com/v3/businesses/search"


def search_restaurants(location, cuisine):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {
        "location": location,
        "term": f"{cuisine} restaurants",
        "categories": "restaurants",
        "limit": 10
    }

    response = requests.get(
        URL,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["businesses"]


if __name__ == "__main__":
    restaurants = search_restaurants(
        "orlando, fl",
        "italian"
    )

    for restaurant in restaurants:
        print(
            restaurant["name"],
            "- rating:",
            restaurant["rating"]
        )