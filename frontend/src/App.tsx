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
  function getMatchLabel(score: number) {
  if (score >= 10) return "great match";
  if (score >= 7) return "good match";
  return "possible match";
}
  const [mode, setMode] = useState<"single" | "couple">("single");
  const [missionOpen, setMissionOpen] = useState(false);

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

    setLoading(true);
    setError("");
    setRestaurants([]);
    setHasSearched(true);

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
      setError("couldn't load restaurants right now. try again in a second.");
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
    <main className="app-shell">
      <section className="hero">
        <div className="background-scene" />
        <div className="scene-overlay" />
        <div className="water-motion" />
        <div className="stars stars-one" />
        <div className="stars stars-two" />
        <div className="city-lights lights-one" />
        <div className="city-lights lights-two" />
        <div className="candle-glow candle-glow-one" />
        <div className="candle-glow candle-glow-two" />

        <div className="hero-ui">
          <header className="top-bar">
            <div className="brand-mini">tabletwo</div>

            <button
              type="button"
              className="mission-button"
              onClick={() => setMissionOpen(!missionOpen)}
            >
              mission
            </button>
          </header>

          {missionOpen && (
            <div className="mission-card">
              <p className="mission-label">mission</p>
              <p className="mission-text">
                for couples who spend 20 minutes tryna figure out what to eat, use tabletwo.
              </p>
            </div>
          )}

          <div className="hero-content">
            <p className="eyebrow"></p>

            <h1>tabletwo</h1>

            <p className="subtitle">
            find the spot and go.
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

            <form className="search-panel" onSubmit={handleSubmit}>
              <div className="field">
                <label>where</label>
                <input
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
                      value={cuisine}
                      onChange={(event) => setCuisine(event.target.value)}
                      placeholder="japanese"
                      required
                    />
                  </div>

                  <div className="field">
                    <label>vibe</label>
                    <input
                      value={vibe}
                      onChange={(event) => setVibe(event.target.value)}
                      placeholder="romantic, chill..."
                      required
                    />
                  </div>
                </>
              ) : (
                <>
                  <div className="field">
                    <label>person 1 food</label>
                    <input
                      value={cuisineOne}
                      onChange={(event) => setCuisineOne(event.target.value)}
                      placeholder="italian"
                      required
                    />
                  </div>

                  <div className="field">
                    <label>person 1 vibe</label>
                    <input
                      value={vibeOne}
                      onChange={(event) => setVibeOne(event.target.value)}
                      placeholder="romantic"
                      required
                    />
                  </div>

                  <div className="field">
                    <label>person 2 food</label>
                    <input
                      value={cuisineTwo}
                      onChange={(event) => setCuisineTwo(event.target.value)}
                      placeholder="japanese"
                      required
                    />
                  </div>

                  <div className="field">
                    <label>person 2 vibe</label>
                    <input
                      value={vibeTwo}
                      onChange={(event) => setVibeTwo(event.target.value)}
                      placeholder="chill"
                      required
                    />
                  </div>
                </>
              )}

              <div className="field budget">
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
                  ? "finding..."
                  : mode === "single"
                  ? "find a spot"
                  : "pick for us"}
              </button>
            </form>

            {error && <p className="error">{error}</p>}
          </div>
        </div>
      </section>

      {hasSearched && (
        <section className="results-section">
          {restaurants.length > 0 && (
            <>
              <div className="results-header">
                <div>
                  <p>your night</p>
                  <h2>best matches</h2>
                </div>

                <span>{restaurants.length} places</span>
              </div>

              <div className="restaurant-list">
                {restaurants.map((restaurant, index) => (
                  <article className="restaurant-row" key={restaurant.yelp_url}>
                    <div className="rank">
                      {String(index + 1).padStart(2, "0")}
                    </div>

                    <div className="restaurant-info">
                      <div className="restaurant-title">
                        <h3>{restaurant.name}</h3>
                        <span className="match-score">
                          {getMatchLabel(restaurant.score)} 
                        </span>
                      </div>

                      <p className="restaurant-meta">
                        {restaurant.rating} ★
                        <span> · </span>
                        {restaurant.price}
                      </p>

                      <p className="address">{restaurant.address}</p>

                      <div className="reasons">
                        {restaurant.reasons.map((reason) => (
                          <span key={reason}>{reason}</span>
                        ))}
                      </div>
                    </div>

                    <div className="links">
                      <a href={restaurant.yelp_url} target="_blank" rel="noreferrer">
                        yelp ↗
                      </a>

                      <a href={restaurant.maps_url} target="_blank" rel="noreferrer">
                        maps ↗
                      </a>

                      <a href={restaurant.tiktok_url} target="_blank" rel="noreferrer">
                        tiktok ↗
                      </a>
                    </div>
                  </article>
                ))}
              </div>
            </>
          )}

          {!loading && !error && restaurants.length === 0 && (
            <div className="no-results">
              <p>nothing good came up.</p>
              <span>try changing the food, vibe, or budget.</span>
            </div>
          )}
        </section>
      )}
    </main>
  );
}

export default App;