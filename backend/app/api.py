from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TableTwo API",
    description="backend api for tabletwo restaurant recommendations"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

from fastapi import FastAPI

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

        restaurant_vibes = []

        category_vibes = {
            "sports bars": ["sports", "lively", "casual"],
            "cocktail bars": ["upscale", "romantic", "lively"],
            "wine bars": ["romantic", "upscale", "chill"],
            "lounges": ["romantic", "upscale", "chill"],
            "bars": ["lively", "casual", "chill"],
            "cafes": ["chill", "casual", "cozy"],
            "desserts": ["romantic", "casual", "chill"]
        }

        for category in categories:
            if category in category_vibes:
                restaurant_vibes.extend(
                    category_vibes[category]
                )

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

        matched_vibe = False

        for group, related_words in vibe_groups.items():
            if any(
                word in vibe.lower()
                for word in related_words
            ):
                for restaurant_vibe in restaurant_vibes:
                    if restaurant_vibe in related_words:
                        matched_vibe = True
                        break

            if matched_vibe:
                break

        if matched_vibe:
            score += 3
            reasons.append("matches vibe")

        address = ", ".join(
            restaurant["location"]["display_address"]
        )

        result = {
            "name": restaurant["name"],
            "rating": rating,
            "price": price if price else "not listed",
            "score": score,
            "reasons": reasons,
            "address": address,
            "yelp_url": restaurant["url"]
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