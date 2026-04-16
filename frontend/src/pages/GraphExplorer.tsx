function GraphExplorer() {
  return (
    <div id="graph-explorer-page">
      <h1>Graph Explorer</h1>
      <p style={{ color: "var(--color-text-secondary)", marginTop: "var(--space-4)" }}>
        Visualize and explore the knowledge graph. Click on entities to see their relationships.
      </p>
      {/* TODO: wire up GraphViewer component with react-force-graph-2d */}
    </div>
  );
}

export default GraphExplorer;
