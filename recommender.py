from yelp_api import search_restaurants


VIBE_GROUPS = {
    "romantic": [
        "wine bars",
        "cocktail bars",
        "lounges",
        "italian",
        "french"
    ],
    "chill": [
        "cafes",
        "coffee & tea",
        "lounges",
        "bars"
    ],
    "lively": [
        "bars",
        "sports bars",
        "cocktail bars",
        "pubs"
    ],
    "upscale": [
        "steakhouses",
        "wine bars",
        "french",
        "seafood",
        "cocktail bars"
    ],
    "casual": [
        "burgers",
        "pizza",
        "tacos",
        "sandwiches",
        "cafes"
    ]
}


def get_categories(restaurant):
    return [
        category["title"].lower()
        for category in restaurant.get("categories", [])
    ]


def matches_vibe(restaurant, preferred_vibe):
    preferred_vibe = preferred_vibe.lower()

    if preferred_vibe not in VIBE_GROUPS:
        return False

    categories = get_categories(restaurant)

    matching_categories = VIBE_GROUPS[preferred_vibe]

    return any(
        category in matching_categories
        for category in categories
    )


def combine_restaurants(
    first_results,
    second_results,
    cuisine_one,
    cuisine_two
):
    combined = {}

    for restaurant in first_results:
        restaurant_id = restaurant["id"]

        combined[restaurant_id] = {
            "restaurant": restaurant,
            "food_matches": {cuisine_one}
        }

    for restaurant in second_results:
        restaurant_id = restaurant["id"]

        if restaurant_id in combined:
            combined[restaurant_id]["food_matches"].add(
                cuisine_two
            )
        else:
            combined[restaurant_id] = {
                "restaurant": restaurant,
                "food_matches": {cuisine_two}
            }

    return list(combined.values())


def score_restaurant(
    restaurant,
    food_matches,
    cuisine_one,
    cuisine_two,
    vibe_one,
    vibe_two,
    max_price
):
    score = 0
    reasons = []

    rating = restaurant.get("rating", 0)

    if rating >= 4.5:
        score += 3
        reasons.append("high rating")

    elif rating >= 4.0:
        score += 2
        reasons.append("good rating")

    price = restaurant.get("price", "")
    price_level = len(price)

    if price_level > 0 and price_level > max_price:
        return None

    if price_level == max_price:
        score += 1
        reasons.append("matches budget")

    if cuisine_one in food_matches:
        score += 3
        reasons.append(f"matches {cuisine_one}")

    if cuisine_two in food_matches:
        score += 3
        reasons.append(f"matches {cuisine_two}")

    if matches_vibe(restaurant, vibe_one):
        score += 2
        reasons.append(f"matches {vibe_one} vibe")

    if matches_vibe(restaurant, vibe_two):
        score += 2
        reasons.append(f"matches {vibe_two} vibe")

    return {
        "name": restaurant["name"],
        "rating": rating,
        "price": price if price else "not listed",
        "score": score,
        "reasons": reasons
    }


def recommend_restaurants(
    location,
    cuisine_one,
    cuisine_two,
    vibe_one,
    vibe_two,
    max_price
):
    first_results = search_restaurants(
        location,
        cuisine_one
    )

    second_results = search_restaurants(
        location,
        cuisine_two
    )

    combined = combine_restaurants(
        first_results,
        second_results,
        cuisine_one,
        cuisine_two
    )

    recommendations = []

    for item in combined:
        result = score_restaurant(
            item["restaurant"],
            item["food_matches"],
            cuisine_one,
            cuisine_two,
            vibe_one,
            vibe_two,
            max_price
        )

        if result is not None:
            recommendations.append(result)

    recommendations.sort(
        key=lambda restaurant: restaurant["score"],
        reverse=True
    )

    return recommendations