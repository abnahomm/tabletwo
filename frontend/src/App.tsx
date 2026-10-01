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
};

function App() {
  const [location, setLocation] = useState("");
  const [cuisine, setCuisine] = useState("");
  const [maxPrice, setMaxPrice] = useState("2");
  const [vibe, setVibe] = useState("");

  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const params = new URLSearchParams({
        location,
        cuisine,
        max_price: maxPrice,
        vibe,
      });

      const response = await fetch(
        `http://127.0.0.1:8000/recommendations?${params.toString()}`
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

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">date night, simplified</p>

        <h1>tabletwo</h1>

        <p className="subtitle">
          find a place to eat without checking five different apps
        </p>

        <form className="search-form" onSubmit={handleSubmit}>
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

          <button type="submit" className="search-button">
            {loading ? "searching..." : "find restaurants"}
          </button>
        </form>

        {error && <p className="error">{error}</p>}
      </section>

      {restaurants.length > 0 && (
        <section className="results">
          <div className="results-heading">
            <h2>your matches</h2>
            <p>{restaurants.length} restaurants found</p>
          </div>

          <div className="restaurant-grid">
            {restaurants.map((restaurant) => (
              <article className="restaurant-card" key={restaurant.yelp_url}>
                <div className="card-top">
                  <div>
                    <h3>{restaurant.name}</h3>
                    <p className="meta">
                      {restaurant.rating} ★ · {restaurant.price}
                    </p>
                  </div>

                  <span className="score">{restaurant.score}</span>
                </div>

                <p className="address">{restaurant.address}</p>

                <div className="reasons">
                  {restaurant.reasons.map((reason) => (
                    <span key={reason}>{reason}</span>
                  ))}
                </div>

                <a
                  className="yelp-link"
                  href={restaurant.yelp_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  view on yelp
                </a>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}

export default App;