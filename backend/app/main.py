restaurants = [
    {
        "name": "prato",
        "city": "orlando",
        "cuisine": "italian",
        "price": 3,
        "rating": 4.7,
        "vibe": "romantic"
    },
    {
        "name": "kabooki sushi",
        "city": "orlando",
        "cuisine": "japanese",
        "price": 3,
        "rating": 4.6,
        "vibe": "upscale"
    },
    {
        "name": "hawkers",
        "city": "orlando",
        "cuisine": "asian",
        "price": 2,
        "rating": 4.5,
        "vibe": "casual"
    }
]

def find_restaurants(cuisine, max_price):
    matches = []

    for restaurant in restaurants:
        if (
            restaurant["cuisine"].lower() == cuisine.lower()
            and restaurant["price"] <= max_price
        ):
            matches.append(restaurant)

    return matches


results = find_restaurants("italian", 3)

print(results)