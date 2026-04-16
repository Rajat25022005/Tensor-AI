function GraphViewer() {
  return (
    <div
      id="graph-viewer"
      className="glass"
      style={{
        width: "100%",
        height: "500px",
        borderRadius: "var(--radius-lg)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "var(--color-text-muted)",
      }}
    >
      {/* TODO: integrate react-force-graph-2d */}
      Graph visualization will render here
    </div>
  );
}

export default GraphViewer;
