import { useState } from "react";

function App() {
  const [location, setLocation] = useState("");
  const [cuisine, setCuisine] = useState("");
  const [maxPrice, setMaxPrice] = useState("2");
  const [vibe, setVibe] = useState("");

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    console.log({
      location,
      cuisine,
      maxPrice,
      vibe,
    });
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
          />
        </div>

        <div>
          <label>food</label>
          <input
            type="text"
            value={cuisine}
            onChange={(event) => setCuisine(event.target.value)}
            placeholder="japanese"
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
          />
        </div>

        <button type="submit">find restaurants</button>
      </form>
    </main>
  );
}

export default App;