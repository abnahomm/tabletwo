import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("YELP_API_KEY")
YELP_URL = "https://api.yelp.com/v3/businesses/search"


def search_restaurants(location, cuisine, limit=10):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {
        "location": location,
        "term": f"{cuisine} restaurants",
        "limit": limit
    }

    response = requests.get(
        YELP_URL,
        headers=headers,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(
            f"Yelp request failed: {response.status_code} - {response.text}"
        )

    data = response.json()

    return data.get("businesses", [])