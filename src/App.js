import { useState } from "react";

function App() {
  const [ticker, setTicker] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchPSG = async () => {
    setLoading(true);
    setError("");
    setData(null);
    try {
      const res = await fetch(`https://your-render-app-url.onrender.com/psg/${ticker.toUpperCase()}`);
      if (!res.ok) {
        throw new Error("Ticker not found or data missing");
      }
      const json = await res.json();
      setData(json);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-6">PSG Ratio Checker</h1>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          placeholder="Enter ticker (e.g. AAPL)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          className="p-2 rounded border border-gray-300"
        />
        <button
          onClick={fetchPSG}
          className="bg-blue-600 text-white px-4 rounded hover:bg-blue-700"
          disabled={!ticker || loading}
        >
          {loading ? "Loading..." : "Get PSG"}
        </button>
      </div>

      {error && <p className="text-red-600">{error}</p>}

      {data && (
        <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
          <h2 className="text-2xl font-semibold mb-4">{data.ticker} PSG Data</h2>
          <p><strong>Price/Sales (P/S):</strong> {data["p/s"].toFixed(2)}</p>
          <p><strong>Sales Growth %:</strong> {data.sales_growth_pct.toFixed(2)}%</p>
          <p><strong>PSG Ratio:</strong> {data.psg.toFixed(3)}</p>
        </div>
      )}
    </div>
  );
}

export default App;