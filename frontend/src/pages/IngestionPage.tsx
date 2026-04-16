import FileUpload from "../components/ingestion/FileUpload";
import { DatabaseBackup, FolderSync } from "lucide-react";
import "./IngestionPage.css";

function IngestionPage() {
  return (
    <div className="ingestion-page">
      <div className="page-header">
        <h1 className="page-title"><DatabaseBackup className="inline-icon" /> Data Ingestion</h1>
        <p className="page-subtitle">Feed documents into the intelligent routing layer for graph synthesis.</p>
      </div>

      <div className="ingestion-layout">
        <div className="ingestion-main">
          <FileUpload />
        </div>
        
        <div className="ingestion-sidebar glass">
          <div className="sidebar-header">
            <FolderSync size={18} />
            <h3>Processing Pipeline</h3>
          </div>
          
          <div className="pipeline-steps">
            <div className="pipeline-step active">
              <div className="step-num">1</div>
              <div className="step-details">
                <h4>Document Parsing</h4>
                <p>Extracting raw text from supported formats.</p>
              </div>
            </div>
            
            <div className="pipeline-step pending">
              <div className="step-num">2</div>
              <div className="step-details">
                <h4>Chunking & Embedding</h4>
                <p>Semantic segmentation via BGE-m3.</p>
              </div>
            </div>
            
            <div className="pipeline-step pending">
              <div className="step-num">3</div>
              <div className="step-details">
                <h4>Entity Extraction</h4>
                <p>Agent-based NER and relation extraction.</p>
              </div>
            </div>
            
            <div className="pipeline-step pending">
              <div className="step-num">4</div>
              <div className="step-details">
                <h4>Graph Synthesis</h4>
                <p>Merging into existing Neo4j topology.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default IngestionPage;
