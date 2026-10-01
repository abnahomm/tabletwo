import { useState } from "react";
import "./App.css";

type Restaurant = {
  name: string;
  rating: number;
  price: string;
  score: number;
  reasons: string[];
  address: string;
  yelp_url: string;
  maps_url: string;
  tiktok_url: string;
};

function App() {
  const [mode, setMode] = useState<"single" | "couple">("single");

  const [location, setLocation] = useState("");
  const [maxPrice, setMaxPrice] = useState("2");

  const [cuisine, setCuisine] = useState("");
  const [vibe, setVibe] = useState("");

  const [cuisineOne, setCuisineOne] = useState("");
  const [vibeOne, setVibeOne] = useState("");

  const [cuisineTwo, setCuisineTwo] = useState("");
  const [vibeTwo, setVibeTwo] = useState("");

  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    setHasSearched(true);
    setLoading(true);
    setError("");
    setRestaurants([]);

    try {
      let params;

      if (mode === "single") {
        params = new URLSearchParams({
          location,
          cuisine,
          max_price: maxPrice,
          vibe,
        });
      } else {
        params = new URLSearchParams({
          location,
          cuisine_one: cuisineOne,
          vibe_one: vibeOne,
          cuisine_two: cuisineTwo,
          vibe_two: vibeTwo,
          max_price: maxPrice,
        });
      }

      const endpoint =
        mode === "single"
          ? "recommendations"
          : "couple-recommendations";

      const response = await fetch(
        `http://127.0.0.1:8000/${endpoint}?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error("failed to get recommendations");
      }

      const data = await response.json();

      setRestaurants(data.restaurants);
    } catch {
      setError("something went wrong while finding restaurants");
    } finally {
      setLoading(false);
    }
  }

  function switchMode(newMode: "single" | "couple") {
    setMode(newMode);
    setRestaurants([]);
    setError("");
    setHasSearched(false);
  }

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">date night, simplified</p>

        <h1>tabletwo</h1>

        <p className="subtitle">
          find somewhere to eat without checking five different apps
        </p>

        <div className="mode-switch">
          <button
            type="button"
            className={mode === "single" ? "active" : ""}
            onClick={() => switchMode("single")}
          >
            find a spot
          </button>

          <button
            type="button"
            className={mode === "couple" ? "active" : ""}
            onClick={() => switchMode("couple")}
          >
            pick for us
          </button>
        </div>

        <form
          className={`search-form ${
            mode === "couple" ? "couple-form" : ""
          }`}
          onSubmit={handleSubmit}
        >
          <div className="field">
            <label>city</label>
            <input
              type="text"
              value={location}
              onChange={(event) => setLocation(event.target.value)}
              placeholder="orlando, fl"
              required
            />
          </div>

          {mode === "single" ? (
            <>
              <div className="field">
                <label>food</label>
                <input
                  type="text"
                  value={cuisine}
                  onChange={(event) => setCuisine(event.target.value)}
                  placeholder="japanese"
                  required
                />
              </div>

              <div className="field">
                <label>vibe</label>
                <input
                  type="text"
                  value={vibe}
                  onChange={(event) => setVibe(event.target.value)}
                  placeholder="romantic, chill, lively..."
                  required
                />
              </div>
            </>
          ) : (
            <>
              <div className="field">
                <label>person 1 food</label>
                <input
                  type="text"
                  value={cuisineOne}
                  onChange={(event) => setCuisineOne(event.target.value)}
                  placeholder="italian"
                  required
                />
              </div>

              <div className="field">
                <label>person 1 vibe</label>
                <input
                  type="text"
                  value={vibeOne}
                  onChange={(event) => setVibeOne(event.target.value)}
                  placeholder="romantic"
                  required
                />
              </div>

              <div className="field">
                <label>person 2 food</label>
                <input
                  type="text"
                  value={cuisineTwo}
                  onChange={(event) => setCuisineTwo(event.target.value)}
                  placeholder="japanese"
                  required
                />
              </div>

              <div className="field">
                <label>person 2 vibe</label>
                <input
                  type="text"
                  value={vibeTwo}
                  onChange={(event) => setVibeTwo(event.target.value)}
                  placeholder="chill"
                  required
                />
              </div>
            </>
          )}

          <div className="field budget-field">
            <label>budget</label>
            <select
              value={maxPrice}
              onChange={(event) => setMaxPrice(event.target.value)}
            >
              <option value="1">$</option>
              <option value="2">$$</option>
              <option value="3">$$$</option>
            </select>
          </div>

          <button className="search-button" type="submit" disabled={loading}>
            {loading
              ? "searching..."
              : mode === "single"
              ? "find restaurants"
              : "pick for us"}
          </button>
        </form>

        {error && <p className="error">{error}</p>}
      </section>

      {restaurants.length > 0 && (
        <section className="results">
          <div className="results-heading">
            <div>
              <p className="results-label">recommendations</p>
              <h2>your matches</h2>
            </div>

            <p>
              {restaurants.length}{" "}
              {restaurants.length === 1 ? "restaurant" : "restaurants"} found
            </p>
          </div>

          <div className="restaurant-grid">
            {restaurants.map((restaurant, index) => (
              <article className="restaurant-card" key={restaurant.yelp_url}>
                <div className="card-top">
                  <div>
                    <p className="ranking">#{index + 1}</p>
                    <h3>{restaurant.name}</h3>

                    <p className="meta">
                      {restaurant.rating} ★
                      <span>·</span>
                      {restaurant.price}
                    </p>
                  </div>

                  <div className="score">
                    <span>{restaurant.score}</span>
                    <small>match</small>
                  </div>
                </div>

                <p className="address">{restaurant.address}</p>

                {restaurant.reasons.length > 0 && (
                  <div className="reasons">
                    {restaurant.reasons.map((reason) => (
                      <span key={reason}>{reason}</span>
                    ))}
                  </div>
                )}

                <div className="restaurant-links">
                  <a
                    href={restaurant.yelp_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    yelp
                  </a>

                  <a
                    href={restaurant.maps_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    maps
                  </a>

                  <a
                    href={restaurant.tiktok_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    tiktok
                  </a>
                </div>
              </article>
            ))}
          </div>
        </section>
      )}

      {!loading && !error && restaurants.length === 0 && !hasSearched && (
        <p className="empty-state">
          tell us what you're looking for and we'll narrow it down.
        </p>
      )}

      {!loading && !error && restaurants.length === 0 && hasSearched && (
        <div className="no-results">
          <h2>no matches yet</h2>
          <p>
            try a different cuisine, budget, or vibe and we'll search again.
          </p>
        </div>
      )}
    </main>
  );
}

export default App;