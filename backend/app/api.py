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


CATEGORY_VIBES = {
    "sports bars": ["sports", "lively", "casual"],
    "cocktail bars": ["upscale", "romantic", "lively"],
    "wine bars": ["romantic", "upscale", "chill"],
    "lounges": ["romantic", "upscale", "chill"],
    "bars": ["lively", "casual", "chill"],
    "cafes": ["chill", "casual", "cozy"],
    "desserts": ["romantic", "casual", "chill"]
}


VIBE_GROUPS = {
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


def get_categories(restaurant):
    return [
        category["title"].lower()
        for category in restaurant["categories"]
    ]


def get_restaurant_vibes(categories):
    restaurant_vibes = []

    for category in categories:
        if category in CATEGORY_VIBES:
            restaurant_vibes.extend(
                CATEGORY_VIBES[category]
            )

    return restaurant_vibes


def vibe_matches(
    preferred_vibe,
    restaurant_vibes,
    restaurant_text=""
):
    preferred_vibe = preferred_vibe.lower()
    restaurant_text = restaurant_text.lower()

    for related_words in VIBE_GROUPS.values():
        user_match = any(
            word in preferred_vibe
            for word in related_words
        )

        restaurant_vibe_match = any(
            vibe in related_words
            for vibe in restaurant_vibes
        )

        restaurant_text_match = any(
            word in restaurant_text
            for word in related_words
        )

        if user_match and (
            restaurant_vibe_match
            or restaurant_text_match
        ):
            return True

    return False


def score_basic_restaurant(restaurant, max_price):
    score = 0
    reasons = []

    rating = restaurant["rating"]
    price = restaurant.get("price", "")
    price_level = len(price)

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

    return score, reasons


def build_links(restaurant_name, address, location):
    maps_query = quote_plus(
        f"{restaurant_name} {address}"
    )

    tiktok_query = quote_plus(
        f"{restaurant_name} {location}"
    )

    maps_url = (
        "https://www.google.com/maps/search/"
        f"?api=1&query={maps_query}"
    )

    tiktok_url = (
        "https://www.tiktok.com/search"
        f"?q={tiktok_query}"
    )

    return maps_url, tiktok_url


def build_result(
    restaurant,
    location,
    score,
    reasons
):
    restaurant_name = restaurant["name"]

    address = ", ".join(
        restaurant["location"]["display_address"]
    )

    price = restaurant.get("price", "")

    maps_url, tiktok_url = build_links(
        restaurant_name,
        address,
        location
    )

    return {
        "name": restaurant_name,
        "rating": restaurant["rating"],
        "price": price if price else "not listed",
        "score": score,
        "reasons": reasons,
        "address": address,
        "yelp_url": restaurant["url"],
        "maps_url": maps_url,
        "tiktok_url": tiktok_url
    }


def is_over_budget(restaurant, max_price):
    price = restaurant.get("price", "")
    price_level = len(price)

    return (
        price_level > 0
        and price_level > max_price
    )


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

        if is_over_budget(restaurant, max_price):
            continue

        score, reasons = score_basic_restaurant(
            restaurant,
            max_price
        )

        categories = get_categories(restaurant)

        restaurant_text = " ".join(
            [
                restaurant["name"],
                *categories
            ]
        )

        restaurant_vibes = get_restaurant_vibes(
            categories
        )

        if vibe_matches(
            vibe,
            restaurant_vibes,
            restaurant_text
        ):
            score += 3
            reasons.append("matches vibe")

        result = build_result(
            restaurant,
            location,
            score,
            reasons
        )

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

        if is_over_budget(restaurant, max_price):
            continue

        score, reasons = score_basic_restaurant(
            restaurant,
            max_price
        )

        categories = get_categories(restaurant)
        category_text = " ".join(categories)

        restaurant_text = " ".join(
            [
                restaurant["name"],
                *categories
            ]
        )

        if cuisine_one.lower() in category_text:
            score += 3
            reasons.append("matches person 1 food")

        if cuisine_two.lower() in category_text:
            score += 3
            reasons.append("matches person 2 food")

        restaurant_vibes = get_restaurant_vibes(
            categories
        )

        if vibe_matches(
            vibe_one,
            restaurant_vibes,
            restaurant_text
        ):
            score += 2
            reasons.append("matches person 1 vibe")

        if vibe_matches(
            vibe_two,
            restaurant_vibes,
            restaurant_text
        ):
            score += 2
            reasons.append("matches person 2 vibe")

        result = build_result(
            restaurant,
            location,
            score,
            reasons
        )

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