function FileUpload() {
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    // TODO: handle file upload via ingestion API
  };

  return (
    <div
      id="file-upload"
      className="glass"
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      style={{
        padding: "var(--space-12)",
        borderRadius: "var(--radius-lg)",
        textAlign: "center",
        cursor: "pointer",
        border: "2px dashed var(--color-border)",
        transition: "border-color var(--transition-fast)",
      }}
    >
      <p style={{ fontSize: "var(--font-size-2xl)", marginBottom: "var(--space-3)" }}>📄</p>
      <p style={{ color: "var(--color-text-secondary)" }}>
        Drag & drop files here, or <span style={{ color: "var(--color-accent-purple)", fontWeight: 600 }}>browse</span>
      </p>
      <p style={{ color: "var(--color-text-muted)", fontSize: "var(--font-size-xs)", marginTop: "var(--space-2)" }}>
        Supported: PDF, TXT, DOCX (max 50MB)
      </p>
    </div>
  );
}

export default FileUpload;
