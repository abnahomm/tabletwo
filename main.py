from recommender import recommend_restaurants


def get_budget():
    while True:
        try:
            budget = int(
                input(
                    "\nmax budget "
                    "(1 = $, 2 = $$, 3 = $$$): "
                )
            )

            if budget in [1, 2, 3]:
                return budget

            print("please enter 1, 2, or 3")

        except ValueError:
            print("please enter a number")


def main():
    print("\n======================")
    print("       TABLETWO")
    print("======================")

    print(
        "\nfind a restaurant that works "
        "for both of you.\n"
    )

    location = input(
        "where are you eating? "
    ).strip()

    print("\nperson 1")
    cuisine_one = input(
        "food preference: "
    ).strip().lower()

    vibe_one = input(
        "vibe (romantic/chill/lively/upscale/casual): "
    ).strip().lower()

    print("\nperson 2")
    cuisine_two = input(
        "food preference: "
    ).strip().lower()

    vibe_two = input(
        "vibe (romantic/chill/lively/upscale/casual): "
    ).strip().lower()

    max_price = get_budget()

    print("\nfinding restaurants...\n")

    try:
        restaurants = recommend_restaurants(
            location,
            cuisine_one,
            cuisine_two,
            vibe_one,
            vibe_two,
            max_price
        )

    except Exception as error:
        print(f"something went wrong: {error}")
        return

    if not restaurants:
        print("no restaurants matched your search.")
        return

    print("======================")
    print("   TABLETWO RESULTS")
    print("======================\n")

    for index, restaurant in enumerate(
        restaurants[:5],
        start=1
    ):
        print(
            f"{index}. {restaurant['name']}"
        )

        print(
            f"   rating: {restaurant['rating']}"
        )

        print(
            f"   price: {restaurant['price']}"
        )

        if restaurant["score"] >= 9:
            match = "great match"
        elif restaurant["score"] >= 6:
            match = "good match"
        else:
            match = "possible match"

        print(
            f"   result: {match}"
        )

        print(
            "   why: "
            + ", ".join(restaurant["reasons"])
        )

        print()


if __name__ == "__main__":
    main()