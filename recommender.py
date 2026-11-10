
from yelp_api import search_restaurants


FAST_FOOD_TYPES = {
    "fast_food_restaurant",
    "hamburger_restaurant",
    "meal_takeaway",
    "sandwich_shop",
}

FAST_FOOD_NAMES = {
    "mcdonald", "burger king", "wendy",
    "taco bell", "chipotle", "subway",
    "popeyes", "chick-fil-a", "kfc",
    "five guys", "skyline chili",
    "checkers", "arby", "sonic drive"
}


def get_price_level(price):
    if not price or price not in ("$", "$$", "$$$", "$$$$"):
        return None
    return len(price)


def is_fast_food(restaurant):
    name = restaurant.get("name", "").lower()
    types = {
        category.get("alias", "").lower()
        for category in restaurant.get("categories", [])
    }

    if types.intersection(FAST_FOOD_TYPES):
        return True

    return any(chain in name for chain in FAST_FOOD_NAMES)


def matches_restaurant_type(restaurant, restaurant_type):
    if restaurant_type == "fast food / quick bites":
        return (
            is_fast_food(restaurant)
            or "fast food" in restaurant.get(
                "name", ""
            ).lower()
        )

    if restaurant_type == "sit-down restaurants":
        return not is_fast_food(restaurant)

    return True


def calculate_score(
    restaurant,
    cuisine_one,
    cuisine_two,
    vibe_one,
    vibe_two,
    max_price
):
    score = 0
    reasons = []

    rating = restaurant.get("rating") or 0
    rating_count = restaurant.get("rating_count") or 0

    price = restaurant.get("price", "")
    price_level = get_price_level(price)

    found_cuisines = set(
        restaurant.get("search_cuisines", [])
    )
    found_vibes = set(
        restaurant.get("search_vibes", [])
    )

    name = restaurant.get("name", "").lower()

    categories = restaurant.get("categories", [])
    category_text = " ".join(
        category.get("title", "").lower()
        for category in categories
    )

    searchable = name + " " + category_text

    # CUISINE COMPATIBILITY
    # Search relevance is a signal, not proof of menu items.
    for person, cuisine in [
        (1, cuisine_one),
        (2, cuisine_two)
    ]:
        if cuisine in found_cuisines:
            score += 3
            reasons.append(
                f"appeared in person {person}'s "
                f"{cuisine} cuisine search"
            )
        elif cuisine in searchable:
            score += 2
            reasons.append(
                f"category matches person {person}'s cuisine"
            )

    # VIBE COMPATIBILITY
    # Reward appearances in mood-specific searches.
    for person, vibe in [
        (1, vibe_one),
        (2, vibe_two)
    ]:
        if not vibe:
            continue

        if vibe in found_vibes:
            score += 4
            reasons.append(
                f"recommended by search for "
                f"person {person}'s {vibe} vibe"
            )

    # RESTAURANT RATINGS
    if rating >= 4.7:
        score += 4
        reasons.append("excellent Google rating")
    elif rating >= 4.5:
        score += 3
        reasons.append("highly rated")
    elif rating >= 4.2:
        score += 2
        reasons.append("good customer rating")
    elif rating >= 4.0:
        score += 1

    # REVIEW CONFIDENCE
    if rating_count >= 500:
        score += 2
        reasons.append("hundreds of customer reviews")
    elif rating_count >= 100:
        score += 1

    # BUDGET
    if price_level is None:
        score -= 2
        reasons.append("price not verified")
    elif price_level <= max_price:
        score += 2
        reasons.append("fits your selected budget")

    # MOOD-SPECIFIC QUALITY ADJUSTMENTS
    selected_vibes = {v for v in [vibe_one, vibe_two] if v}

    if "upscale" in selected_vibes:
        if price_level is not None and price_level >= 3:
            score += 3
            reasons.append("higher-end price category")
        elif price_level == 1:
            score -= 5

    if "romantic" in selected_vibes:
        if is_fast_food(restaurant):
            score -= 8
        elif price_level is not None and price_level >= 2:
            score += 1

    if "casual" in selected_vibes:
        if price_level is not None and price_level <= 2:
            score += 2

    if "chill" in selected_vibes:
        if price_level == 2:
            score += 1

    # PREFER RESTAURANTS FOUND IN BOTH SEARCHES
    if restaurant.get("matched_both_searches"):
        score += 3
        reasons.append("appeared in both people's searches")

    return score, reasons


def recommend_restaurants(
    location,
    cuisine_one,
    cuisine_two,
    vibe_one,
    vibe_two,
    max_price,
    restaurant_type="all restaurants"
):
    cuisine_one = cuisine_one.strip().lower()
    cuisine_two = cuisine_two.strip().lower()

    fast_mode = (
        restaurant_type == "fast food / quick bites"
    )

    if fast_mode:
        vibe_one = None
        vibe_two = None

    restaurants_one = search_restaurants(
        location,
        cuisine_one,
        20,
        vibe_one,
        restaurant_type
    )

    restaurants_two = search_restaurants(
        location,
        cuisine_two,
        20,
        vibe_two,
        restaurant_type
    )

    combined = {}

    for person, restaurants in [
        (1, restaurants_one),
        (2, restaurants_two)
    ]:
        for restaurant in restaurants:
            restaurant_id = restaurant.get("id")

            if not restaurant_id:
                continue

            if restaurant_id not in combined:
                combined[restaurant_id] = {
                    **restaurant,
                    "search_vibes": set(),
                    "search_cuisines": set(),
                    "found_by": set(),
                }

            stored = combined[restaurant_id]

            stored["found_by"].add(person)

            stored["search_vibes"].update(
                restaurant.get("search_vibes", [])
            )

            stored["search_cuisines"].update(
                restaurant.get("search_cuisines", [])
            )

    results = []

    for restaurant in combined.values():
        restaurant["matched_both_searches"] = (
            len(restaurant["found_by"]) == 2
        )

        if not matches_restaurant_type(
            restaurant,
            restaurant_type
        ):
            continue

        # Prevent fast food from dominating
        # romantic or upscale recommendations.
        if not fast_mode and is_fast_food(restaurant):
            if vibe_one in ("romantic", "upscale") or \
               vibe_two in ("romantic", "upscale"):
                continue

        price = restaurant.get("price", "")
        price_level = get_price_level(price)

        # Exclude known over-budget restaurants.
        # Unknown prices remain eligible but are penalized.
        if price_level is not None and price_level > max_price:
            continue

        score, reasons = calculate_score(
            restaurant,
            cuisine_one,
            cuisine_two,
            vibe_one,
            vibe_two,
            max_price
        )

        if fast_mode:
            reasons = [
                r for r in reasons
                if "vibe" not in r
            ]
            reasons.append("quick-bite option")

        results.append({
            "name": restaurant.get(
                "name", "Unknown restaurant"
            ),
            "rating": restaurant.get("rating") or "N/A",
            "price": price or "N/A",
            "url": restaurant.get("url", ""),
            "score": score,
            "reasons": reasons,
            "rating_count": restaurant.get(
                "rating_count", 0
            )
        })

    results.sort(
        key=lambda r: (
            r["score"],
            r["rating_count"],
            r["rating"] if isinstance(
                r["rating"], (float, int)
            ) else 0
        ),
        reverse=True
    )

    return results
