function QueryPage() {
  return (
    <div id="query-page">
      <h1>Query Interface</h1>
      <p style={{ color: "var(--color-text-secondary)", marginTop: "var(--space-4)" }}>
        Ask questions about your indexed knowledge. The multi-agent pipeline will plan,
        retrieve, execute, and validate before responding.
      </p>
      {/* TODO: wire up QueryInterface component */}
    </div>
  );
}

export default QueryPage;
