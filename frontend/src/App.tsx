import { useState } from "react";

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
    <main>
      <h1>tabletwo</h1>

      <p>find a date night spot without checking five different apps</p>

      <form onSubmit={handleSubmit}>
        <div>
          <label>city</label>
          <input
            type="text"
            value={location}
            onChange={(event) => setLocation(event.target.value)}
            placeholder="orlando, fl"
            required
          />
        </div>

        <div>
          <label>food</label>
          <input
            type="text"
            value={cuisine}
            onChange={(event) => setCuisine(event.target.value)}
            placeholder="japanese"
            required
          />
        </div>

        <div>
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

        <div>
          <label>vibe</label>
          <input
            type="text"
            value={vibe}
            onChange={(event) => setVibe(event.target.value)}
            placeholder="romantic, chill, lively..."
            required
          />
        </div>

        <button type="submit">
          {loading ? "searching..." : "find restaurants"}
        </button>
      </form>

      {error && <p>{error}</p>}

      <section>
        {restaurants.map((restaurant) => (
          <article key={restaurant.yelp_url}>
            <h2>{restaurant.name}</h2>

            <p>
              {restaurant.rating} stars · {restaurant.price}
            </p>

            <p>{restaurant.address}</p>

            <p>match score: {restaurant.score}</p>

            <ul>
              {restaurant.reasons.map((reason) => (
                <li key={reason}>{reason}</li>
              ))}
            </ul>

            <a
              href={restaurant.yelp_url}
              target="_blank"
              rel="noreferrer"
            >
              view on yelp
            </a>
          </article>
        ))}
      </section>
    </main>
  );
}

export default App;