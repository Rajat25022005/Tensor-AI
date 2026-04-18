import { useState, useRef } from "react";
import { UploadCloud, FileType, CheckCircle2, AlertCircle } from "lucide-react";
import { api } from "../../services/api";
import type { IngestResponse } from "../../types";
import "./FileUpload.css";

function FileUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [resultMessage, setResultMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File) => {
    const validExtensions = [".pdf", ".txt", ".md", ".csv", ".json"];
    const ext = "." + file.name.split(".").pop()?.toLowerCase();
    if (!validExtensions.includes(ext)) {
      throw new Error(`Invalid file type. Supported: ${validExtensions.join(", ")}`);
    }
    if (file.size > 50 * 1024 * 1024) {
      throw new Error("File exceeds 50MB limit");
    }
  };

  const handleFile = (newFile: File) => {
    try {
      validateFile(newFile);
      setFile(newFile);
      setStatus("idle");
      setErrorMessage("");
      setResultMessage("");
    } catch (err) {
      setStatus("error");
      setErrorMessage((err as Error).message);
    }
  };

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = () => setIsDragging(false);

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const res = await api.post<IngestResponse>("/ingest/upload", formData, { 
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 120000, // 2 min timeout for large files
      });
      
      const data = res.data;
      
      if (data.status === "completed") {
        setStatus("success");
        const parts = [];
        if (data.chunks_created) parts.push(`${data.chunks_created} chunks`);
        if (data.entities_extracted) parts.push(`${data.entities_extracted} entities`);
        setResultMessage(
          `${data.filename} processed successfully.` + 
          (parts.length ? ` Created ${parts.join(", ")}.` : "")
        );
      } else if (data.status === "queued") {
        setStatus("success");
        setResultMessage(`${data.filename} queued for background processing.`);
      } else {
        setStatus("error");
        setErrorMessage(data.message || "Ingestion failed.");
      }
      
      setFile(null);
    } catch (err: any) {
      setStatus("error");
      const detail = err.response?.data?.detail || "Upload failed. Is the backend running?";
      setErrorMessage(detail);
    }
  };

  return (
    <div className="file-upload-container">
      <div
        className={`file-upload-dropzone glass ${isDragging ? "dragging" : ""}`}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])} 
          style={{ display: "none" }} 
          accept=".pdf,.txt,.md,.csv,.json"
        />
        <UploadCloud className="upload-icon" size={48} />
        <p className="upload-text">
          Drag & drop files here, or <span className="upload-browse">browse</span>
        </p>
        <p className="upload-hint">Supported: PDF, TXT, MD, CSV, JSON (max 50MB)</p>
      </div>

      {file && (
        <div className="file-preview glass">
          <FileType className="file-icon" size={24} />
          <div className="file-details">
            <span className="file-name">{file.name}</span>
            <span className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
          </div>
          {status === "idle" && (
            <button className="btn-upload" onClick={handleUpload}>Confirm Upload</button>
          )}
          {status === "uploading" && <span className="status-text text-primary">Uploading & Processing...</span>}
        </div>
      )}

      {status === "success" && (
        <div className="upload-alert success glass">
          <CheckCircle2 size={18} /> {resultMessage || "Document successfully ingested."}
        </div>
      )}

      {status === "error" && (
        <div className="upload-alert error glass">
          <AlertCircle size={18} /> {errorMessage}
        </div>
      )}
    </div>
  );
}

export default FileUpload;
