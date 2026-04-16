import { useEffect } from "react";
import { useSettingsStore } from "../stores/settingsStore";
import ConnectorCard from "../components/settings/ConnectorCard";
import LLMConfig from "../components/settings/LLMConfig";
import { Settings, Cable } from "lucide-react";
import "./SettingsPage.css";

function SettingsPage() {
  const { connectors, llmConfig, fetchConnectors, toggleConnectorStatus, updateLLMConfig, isLoading } = useSettingsStore();

  useEffect(() => {
    fetchConnectors();
  }, [fetchConnectors]);

  return (
    <div className="settings-page">
      <div className="page-header">
        <h1 className="page-title"><Settings className="inline-icon" /> System Settings</h1>
        <p className="page-subtitle">Configure enterprise integrations and AI behavior.</p>
      </div>

      <div className="settings-container">
        <div className="settings-section" id="connectors">
          <div className="section-header">
            <Cable className="section-icon" />
            <h2>Data Connectors</h2>
          </div>
          <p className="section-desc">Manage connections to your internal data sources. Only active connectors will be analyzed during the nightly bulk ingestion job.</p>
          
          <div className="connectors-grid">
            {connectors.map(connector => (
              <ConnectorCard 
                key={connector.id} 
                connector={connector} 
                onToggle={toggleConnectorStatus}
                isLoading={isLoading}
              />
            ))}
          </div>
        </div>

        <div className="settings-section" id="llm-config">
          <LLMConfig 
            config={llmConfig} 
            onSave={updateLLMConfig} 
            isLoading={isLoading} 
          />
        </div>
      </div>
    </div>
  );
}

export default SettingsPage;
