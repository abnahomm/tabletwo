from urllib.parse import quote_plus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.yelp_api import search_restaurants


app = FastAPI(
    title="TableTwo API",
    description="backend api for tabletwo restaurant recommendations"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


category_vibes = {
    "sports bars": ["sports", "lively", "casual"],
    "cocktail bars": ["upscale", "romantic", "lively"],
    "wine bars": ["romantic", "upscale", "chill"],
    "lounges": ["romantic", "upscale", "chill"],
    "bars": ["lively", "casual", "chill"],
    "cafes": ["chill", "casual", "cozy"],
    "desserts": ["romantic", "casual", "chill"]
}


vibe_groups = {
    "chill": [
        "chill",
        "casual",
        "relaxed",
        "laid back",
        "lowkey",
        "cozy"
    ],
    "romantic": [
        "romantic",
        "intimate",
        "date night",
        "cute",
        "cozy",
        "first date"
    ],
    "upscale": [
        "upscale",
        "fancy",
        "elegant",
        "classy",
        "nice",
        "luxury"
    ],
    "lively": [
        "lively",
        "fun",
        "energetic",
        "social",
        "busy",
        "exciting"
    ],
    "sports": [
        "sports",
        "game",
        "watch the game",
        "sports bar",
        "bar",
        "casual"
    ]
}


def get_restaurant_vibes(categories):
    restaurant_vibes = []

    for category in categories:
        if category in category_vibes:
            restaurant_vibes.extend(category_vibes[category])

    return restaurant_vibes


def vibe_matches(preferred_vibe, restaurant_vibes):
    for group, related_words in vibe_groups.items():
        if any(
            word in preferred_vibe.lower()
            for word in related_words
        ):
            for restaurant_vibe in restaurant_vibes:
                if restaurant_vibe in related_words:
                    return True

    return False


def build_links(restaurant_name, address, location):
    maps_query = quote_plus(
        f"{restaurant_name} {address}"
    )

    tiktok_query = quote_plus(
        f"{restaurant_name} {location}"
    )

    return {
        "maps_url": (
            "https://www.google.com/maps/search/"
            f"?api=1&query={maps_query}"
        ),
        "tiktok_url": (
            "https://www.tiktok.com/search"
            f"?q={tiktok_query}"
        )
    }


@app.get("/")
def home():
    return {
        "message": "tabletwo api is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/recommendations")
def get_recommendations(
    location: str,
    cuisine: str,
    max_price: int,
    vibe: str
):
    restaurants = search_restaurants(
        location,
        cuisine
    )

    results = []

    for restaurant in restaurants:
        price = restaurant.get("price", "")
        price_level = len(price)

        if price_level > 0 and price_level > max_price:
            continue

        score = 0
        reasons = []

        rating = restaurant["rating"]

        if rating >= 4.5:
            score += 4
            reasons.append("high rating")
        elif rating >= 4.0:
            score += 2
            reasons.append("good rating")

        if price_level > 0:
            score += 1
            reasons.append("price listed")

        if price_level == max_price:
            score += 2
            reasons.append("matches budget")

        categories = [
            category["title"].lower()
            for category in restaurant["categories"]
        ]

        restaurant_vibes = get_restaurant_vibes(categories)

        if vibe_matches(vibe, restaurant_vibes):
            score += 3
            reasons.append("matches vibe")

        address = ", ".join(
            restaurant["location"]["display_address"]
        )

        restaurant_name = restaurant["name"]

        links = build_links(
            restaurant_name,
            address,
            location
        )

        result = {
            "name": restaurant_name,
            "rating": rating,
            "price": price if price else "not listed",
            "score": score,
            "reasons": reasons,
            "address": address,
            "yelp_url": restaurant["url"],
            "maps_url": links["maps_url"],
            "tiktok_url": links["tiktok_url"]
        }

        results.append(result)

    results.sort(
        key=lambda restaurant: restaurant["score"],
        reverse=True
    )

    return {
        "location": location,
        "cuisine": cuisine,
        "max_price": max_price,
        "vibe": vibe,
        "restaurants": results
    }


@app.get("/couple-recommendations")
def get_couple_recommendations(
    location: str,
    cuisine_one: str,
    vibe_one: str,
    cuisine_two: str,
    vibe_two: str,
    max_price: int
):
    search_term = f"{cuisine_one} {cuisine_two}"

    restaurants = search_restaurants(
        location,
        search_term
    )

    results = []

    for restaurant in restaurants:
        price = restaurant.get("price", "")
        price_level = len(price)

        if price_level > 0 and price_level > max_price:
            continue

        score = 0
        reasons = []

        rating = restaurant["rating"]

        if rating >= 4.5:
            score += 4
            reasons.append("high rating")
        elif rating >= 4.0:
            score += 2
            reasons.append("good rating")

        if price_level > 0:
            score += 1
            reasons.append("price listed")

        if price_level == max_price:
            score += 2
            reasons.append("matches budget")

        categories = [
            category["title"].lower()
            for category in restaurant["categories"]
        ]

        category_text = " ".join(categories)

        if cuisine_one.lower() in category_text:
            score += 3
            reasons.append("matches person 1 food")

        if cuisine_two.lower() in category_text:
            score += 3
            reasons.append("matches person 2 food")

        restaurant_vibes = get_restaurant_vibes(categories)

        if vibe_matches(vibe_one, restaurant_vibes):
            score += 2
            reasons.append("matches person 1 vibe")

        if vibe_matches(vibe_two, restaurant_vibes):
            score += 2
            reasons.append("matches person 2 vibe")

        address = ", ".join(
            restaurant["location"]["display_address"]
        )

        restaurant_name = restaurant["name"]

        links = build_links(
            restaurant_name,
            address,
            location
        )

        result = {
            "name": restaurant_name,
            "rating": rating,
            "price": price if price else "not listed",
            "score": score,
            "reasons": reasons,
            "address": address,
            "yelp_url": restaurant["url"],
            "maps_url": links["maps_url"],
            "tiktok_url": links["tiktok_url"]
        }

        results.append(result)

    results.sort(
        key=lambda restaurant: restaurant["score"],
        reverse=True
    )

    return {
        "location": location,
        "person_one": {
            "cuisine": cuisine_one,
            "vibe": vibe_one
        },
        "person_two": {
            "cuisine": cuisine_two,
            "vibe": vibe_two
        },
        "max_price": max_price,
        "restaurants": results
    }