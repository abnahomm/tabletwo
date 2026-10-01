from fastapi import FastAPI

app = FastAPI(
    title="TableTwo API",
    description="backend api for tabletwo restaurant recommendations"
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

        result = {
            "name": restaurant["name"],
            "rating": restaurant["rating"],
            "price": price if price else "not listed",
            "address": ", ".join(
                restaurant["location"]["display_address"]
            ),
            "yelp_url": restaurant["url"]
        }

        results.append(result)

    return {
        "location": location,
        "cuisine": cuisine,
        "max_price": max_price,
        "vibe": vibe,
        "restaurants": results
    }