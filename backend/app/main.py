from yelp_api import search_restaurants
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

vibe_groups = {
    "chill": ["chill", "casual", "relaxed", "laid back", "cozy"],
    "romantic": ["romantic", "intimate", "cozy", "date night"],
    "upscale": ["upscale", "fancy", "elegant", "classy"],
    "lively": ["lively", "fun", "energetic", "social"],
    "sports": ["sports", "game", "bar", "lively", "casual"]
}

def score_restaurant(restaurant, preferred_cuisine, max_price, preferred_vibe):
    score = 0
    reasons = []

    if restaurant["cuisine"].lower() == preferred_cuisine.lower():
        score += 5
        reasons.append("matches cuisine")

    if restaurant["price"] <= max_price:
        score += 2
        reasons.append("within budget")

    matched_vibe = False

    for group, related_words in vibe_groups.items():
        if preferred_vibe.lower() in related_words:
            for restaurant_vibe in restaurant["vibes"]:
                if restaurant_vibe in related_words:
                    matched_vibe = True
                    break

        if matched_vibe:
            break

    if matched_vibe:
        score += 3
        reasons.append("matches vibe")

    if restaurant["rating"] >= 4.5:
        score += 2
        reasons.append("high rating")

    return score, reasons


def recommend_restaurants(preferred_cuisine, max_price, preferred_vibe):
    recommendations = []

    for restaurant in restaurants:

        # skip restaurants that are over the user's budget
        if restaurant["price"] > max_price:
            continue

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


location = input("what city are you looking in? ")

preferred_cuisine = input("what type of food do you want? ")

while True:
    try:
        max_price = int(
            input("what is your max price level? enter 1, 2, or 3: ")
        )

        if max_price in [1, 2, 3]:
            break

        print("please enter 1, 2, or 3.")

    except ValueError:
        print("please enter a number.")

preferred_vibe = input("what kind of vibe do you want? ")

real_restaurants = search_restaurants(
    location,
    preferred_cuisine
)

converted_restaurants = []

for restaurant in real_restaurants:
    converted_restaurant = {
        "name": restaurant["name"],
        "rating": restaurant["rating"],
        "price": restaurant.get("price", "not listed"),
        "price_level": len(restaurant.get("price", "")),
        "categories": [
            category["title"].lower()
            for category in restaurant["categories"]
        ],
        "address": ", ".join(
            restaurant["location"]["display_address"]
        ),
        "url": restaurant["url"]
    }

    converted_restaurants.append(converted_restaurant)
    filtered_restaurants = []

for restaurant in converted_restaurants:
    price_level = restaurant["price_level"]

    if price_level == 0:
        filtered_restaurants.append(restaurant)

    elif price_level <= max_price:
        filtered_restaurants.append(restaurant)


print("\nrestaurants found:\n")

for restaurant in filtered_restaurants:
    print(
        restaurant["name"],
        "- rating:",
        restaurant["rating"],
        "- price:",
        restaurant["price"]
    )
