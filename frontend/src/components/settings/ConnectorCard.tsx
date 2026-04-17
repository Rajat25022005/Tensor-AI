import { Mail, Slack, FileText, Database, Loader2, Plug } from "lucide-react";
import type { ConnectorConfig } from "../../types";
import "./ConnectorCard.css";

interface Props {
  connector: ConnectorConfig;
  onToggle: (id: string) => Promise<void>;
  isLoading: boolean;
}

function ConnectorCard({ connector, onToggle, isLoading }: Props) {
  const getIcon = () => {
    switch (connector.type) {
      case "gmail": return <Mail size={24} />;
      case "slack": return <Slack size={24} />;
      case "pdf": return <FileText size={24} />;
      case "sql": return <Database size={24} />;
      default: return <Plug size={24} />;
    }
  };

  const isConnected = connector.status === "connected";

  return (
    <div className={`connector-card glass ${isConnected ? 'connected' : ''}`}>
      <div className="connector-card__header">
        <div className={`connector-icon ${isConnected ? 'active' : ''}`}>
          {getIcon()}
        </div>
        <div className="connector-switch">
          <label className="switch">
            <input 
              type="checkbox" 
              checked={isConnected} 
              onChange={() => onToggle(connector.id)} 
              disabled={isLoading}
            />
            <span className="slider round">
              {isLoading && <Loader2 size={14} className="spin loader-icon" />}
            </span>
          </label>
        </div>
      </div>
      
      <div className="connector-card__body">
        <h3 className="connector-title">{connector.name}</h3>
        <p className="connector-type">Type: {connector.type.toUpperCase()}</p>
        
        {isConnected && connector.lastSync && (
          <p className="connector-sync">Last sync: {new Date(connector.lastSync).toLocaleDateString()}</p>
        )}
      </div>
      
      <div className="connector-card__footer">
        <span className={`status-badge ${connector.status}`}>
          {connector.status}
        </span>
        {isConnected && (
          <button className="btn-config">Configure</button>
        )}
      </div>
    </div>
  );
}

export default ConnectorCard;
