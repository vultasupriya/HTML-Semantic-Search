import React, { useState } from "react";
import { searchUrl, indexUrl } from "./api";
import ResultCard from "./ResultCard";

function App() {
  const [url, setUrl] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSearch = async (e) => {
    e && e.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      const res = await searchUrl(url, query);
      setResults(res);
      if (!res || res.length === 0) setMessage("No matches found.");
    } catch (err) {
      console.error(err);
      setMessage(err.response?.data?.detail || "Search failed. See console.");
    } finally {
      setLoading(false);
    }
  };

  const handleIndex = async () => {
    setLoading(true);
    setMessage("");
    try {
      const resp = await indexUrl(url, query);
      setMessage(`Indexed: ${resp.chunks_added} chunks`);
    } catch (err) {
      setMessage(err.response?.data?.detail || "Indexing failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h2>HTML Semantic Search</h2>
        <div className="small">Enter a website URL and a search query. Top 10 matching HTML chunks are returned.</div>
      </div>

      <form className="form" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Website URL (e.g., https://example.com)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Search query (e.g., contact info, installation)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>Search</button>
        <button type="button" className="secondary" onClick={handleIndex} disabled={loading}>Index URL</button>
      </form>

      {loading && <div className="small">Working...</div>}
      {message && <div className="small">{message}</div>}

      <div className="results">
        {results && results.length > 0 ? (
          results.map((r, i) => <ResultCard item={r} key={i} />)
        ) : null}
      </div>
    </div>
  );
}

export default App;
