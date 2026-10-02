from yelp_api import search_restaurants


def get_price_level(price):
    if not price:
        return 1

    return len(price)


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

    name = restaurant.get(
        "name",
        ""
    ).lower()

    categories = restaurant.get(
        "categories",
        []
    )

    category_names = [
        category.get(
            "title",
            ""
        ).lower()
        for category in categories
    ]

    category_text = " ".join(
        category_names
    )

    rating = restaurant.get(
        "rating",
        0
    )

    price = restaurant.get(
        "price",
        "$"
    )

    price_level = get_price_level(
        price
    )


    if cuisine_one in category_text or cuisine_one in name:
        score += 2
        reasons.append(
            f"matches person 1's {cuisine_one} preference"
        )


    if cuisine_two in category_text or cuisine_two in name:
        score += 2
        reasons.append(
            f"matches person 2's {cuisine_two} preference"
        )


    if rating >= 4.5:
        score += 3
        reasons.append(
            "highly rated"
        )

    elif rating >= 4.0:
        score += 2
        reasons.append(
            "good rating"
        )

    elif rating >= 3.5:
        score += 1


    if price_level <= max_price:
        score += 2
        reasons.append(
            "fits your budget"
        )


    vibe_text = (
        name
        + " "
        + category_text
    )


    if vibe_one in vibe_text:
        score += 1
        reasons.append(
            f"fits person 1's {vibe_one} vibe"
        )


    if vibe_two in vibe_text:
        score += 1
        reasons.append(
            f"fits person 2's {vibe_two} vibe"
        )


    return score, reasons


def recommend_restaurants(
    location,
    cuisine_one,
    cuisine_two,
    vibe_one,
    vibe_two,
    max_price
):

    restaurants_one = search_restaurants(
        location,
        cuisine_one,
        10
    )

    restaurants_two = search_restaurants(
        location,
        cuisine_two,
        10
    )


    combined = {}

    for restaurant in (
        restaurants_one
        + restaurants_two
    ):
        restaurant_id = restaurant.get(
            "id"
        )

        if restaurant_id:
            combined[
                restaurant_id
            ] = restaurant


    results = []


    for restaurant in combined.values():

        price = restaurant.get(
            "price",
            "$"
        )

        price_level = get_price_level(
            price
        )


        if price_level > max_price:
            continue


        score, reasons = calculate_score(
            restaurant,
            cuisine_one,
            cuisine_two,
            vibe_one,
            vibe_two,
            max_price
        )


        results.append(
            {
                "name": restaurant.get(
                    "name",
                    "Unknown restaurant"
                ),

                "rating": restaurant.get(
                    "rating",
                    "N/A"
                ),

                "price": restaurant.get(
                    "price",
                    "N/A"
                ),

                "url": restaurant.get(
                    "url",
                    ""
                ),

                "score": score,

                "reasons": reasons
            }
        )


    results.sort(
        key=lambda restaurant: (
            restaurant["score"],
            restaurant["rating"]
            if isinstance(
                restaurant["rating"],
                (
                    int,
                    float
                )
            )
            else 0
        ),
        reverse=True
    )


    return results