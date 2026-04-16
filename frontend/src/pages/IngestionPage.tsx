function IngestionPage() {
  return (
    <div id="ingestion-page">
      <h1>Document Ingestion</h1>
      <p style={{ color: "var(--color-text-secondary)", marginTop: "var(--space-4)" }}>
        Upload documents to build your knowledge graph. Supported formats: PDF, TXT, DOCX.
      </p>
      {/* TODO: wire up FileUpload component */}
    </div>
  );
}

export default IngestionPage;
