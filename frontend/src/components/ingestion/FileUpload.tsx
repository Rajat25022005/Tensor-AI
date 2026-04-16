import { useState, useRef } from "react";
import { UploadCloud, FileType, CheckCircle2, AlertCircle } from "lucide-react";
import { api } from "../../services/api";
import "./FileUpload.css";

function FileUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File) => {
    const validTypes = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
    if (!validTypes.includes(file.type)) {
      throw new Error("Invalid file type. Supported: PDF, TXT, DOCX");
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
    
    // Create FormData simulation string since backend is stubbed
    // const formData = new FormData();
    // formData.append("file", file);
    
    try {
      // await api.post("/ingest/upload", formData, { headers: { "Content-Type": "multipart/form-data" }});
      await new Promise(r => setTimeout(r, 1500)); // Simulate network
      setStatus("success");
      setFile(null);
    } catch (err) {
      setStatus("error");
      setErrorMessage("Upload failed. Please try again.");
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
          accept=".pdf,.txt,.docx"
        />
        <UploadCloud className="upload-icon" size={48} />
        <p className="upload-text">
          Drag & drop files here, or <span className="upload-browse">browse</span>
        </p>
        <p className="upload-hint">Supported: PDF, TXT, DOCX (max 50MB)</p>
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
          {status === "uploading" && <span className="status-text text-primary">Uploading...</span>}
        </div>
      )}

      {status === "success" && (
        <div className="upload-alert success glass">
          <CheckCircle2 size={18} /> Document successfully queued for ingestion.
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
