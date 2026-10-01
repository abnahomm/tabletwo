import os

import requests
from dotenv import load_dotenv


from pathlib import Path
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("YELP_API_KEY")

URL = "https://api.yelp.com/v3/businesses/search"


def search_restaurants(location, cuisine):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {
    "location": location,
    "term": f"{cuisine} restaurants",
    "limit": 10
}

    response = requests.get(
        URL,
        headers=headers,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        print("yelp error:", response.status_code)
        print(response.text)
    if response.status_code != 200:
        raise Exception(
            f"Yelp error {response.status_code}: {response.text}"
    )

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