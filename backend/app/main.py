restaurants = [
    {
        "name": "prato",
        "city": "orlando",
        "cuisine": "italian",
        "price": 3,
        "rating": 4.7,
        "vibes": ["romantic", "upscale", "chill"]
    },
    {
        "name": "kabooki sushi",
        "city": "orlando",
        "cuisine": "japanese",
        "price": 3,
        "rating": 4.6,
        "vibes": ["upscale", "romantic"]
    },
    {
        "name": "hawkers",
        "city": "orlando",
        "cuisine": "asian",
        "price": 2,
        "rating": 4.5,
        "vibes": ["casual", "chill", "lively"]
    }
]

def score_restaurant(restaurant, preferred_cuisine, max_price, preferred_vibe):
    score = 0
    reasons = []

    if restaurant["cuisine"].lower() == preferred_cuisine.lower():
        score += 5
        reasons.append("matches cuisine")

    if restaurant["price"] <= max_price:
        score += 2
        reasons.append("within budget")

    if preferred_vibe.lower() in restaurant["vibes"]:
        score += 3
        reasons.append("matches vibe")

    if restaurant["rating"] >= 4.5:
        score += 2
        reasons.append("high rating")

    return score, reasons


def recommend_restaurants(preferred_cuisine, max_price, preferred_vibe):
    recommendations = []

    for restaurant in restaurants:
        score, reasons = score_restaurant(
            restaurant,
            preferred_cuisine,
            max_price,
            preferred_vibe
        )

        restaurant_result = restaurant.copy()
        restaurant_result["score"] = score
        restaurant_result["reasons"] = reasons

        recommendations.append(restaurant_result)

    recommendations.sort(
        key=lambda restaurant: restaurant["score"],
        reverse=True
    )

    return recommendations


preferred_cuisine = input("what type of food do you want? ")
max_price = int(input("what is your max price level? enter 1, 2, or 3: "))
preferred_vibe = input("what kind of vibe do you want? ")

results = recommend_restaurants(
    preferred_cuisine,
    max_price,
    preferred_vibe
)

print("\nrecommended restaurants:\n")

for restaurant in results:
    print(
        restaurant["name"],
        "- score:",
        restaurant["score"]
    )

    for reason in restaurant["reasons"]:
        print("  -", reason)

    print()

