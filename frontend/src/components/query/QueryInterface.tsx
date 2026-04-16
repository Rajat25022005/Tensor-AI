import { useState } from "react";

function QueryInterface() {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    // TODO: dispatch to query store
    setQuery("");
  };

  return (
    <form onSubmit={handleSubmit} className="glass" style={{ padding: "var(--space-6)", borderRadius: "var(--radius-lg)" }}>
      <textarea
        id="query-input"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask anything about your data..."
        rows={3}
        style={{ width: "100%", resize: "vertical" }}
      />
      <button
        type="submit"
        id="query-submit"
        style={{
          marginTop: "var(--space-4)",
          padding: "var(--space-3) var(--space-6)",
          background: "var(--gradient-primary)",
          color: "white",
          borderRadius: "var(--radius-md)",
          fontWeight: 600,
        }}
      >
        Submit Query
      </button>
    </form>
  );
}

export default QueryInterface;
