import { useState } from "react";
import { Cpu, Settings2, Save } from "lucide-react";
import "./LLMConfig.css";

interface LLMState {
  model: string;
  temperature: number;
  maxTokens: number;
}

interface Props {
  config: LLMState;
  onSave: (config: LLMState) => Promise<void>;
  isLoading: boolean;
}

function LLMConfig({ config, onSave, isLoading }: Props) {
  const [localConfig, setLocalConfig] = useState<LLMState>(config);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(localConfig);
  };

  return (
    <div className="llm-config glass panel">
      <div className="llm-config__header">
        <Cpu className="llm-icon" />
        <h2 className="llm-title">Local LLM Interface</h2>
      </div>

      <form onSubmit={handleSubmit} className="llm-form">
        <div className="form-group">
          <label>Active Model</label>
          <select 
            value={localConfig.model}
            onChange={(e) => setLocalConfig({...localConfig, model: e.target.value})}
            disabled={isLoading}
          >
            <option value="mistral">Mistral 7B (Ollama)</option>
            <option value="llama3">LLaMA 3 8B (Ollama)</option>
            <option value="gemma2">Gemma 2 9B (Ollama)</option>
          </select>
        </div>

        <div className="form-group">
          <label>
            Temperature
            <span className="val-display">{localConfig.temperature}</span>
          </label>
          <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.1" 
            className="config-slider"
            value={localConfig.temperature}
            onChange={(e) => setLocalConfig({...localConfig, temperature: parseFloat(e.target.value)})}
            disabled={isLoading}
          />
          <span className="hint-text">Lower values make responses more deterministic.</span>
        </div>

        <div className="form-group">
          <label>
            Max Context Tokens
            <span className="val-display">{localConfig.maxTokens}</span>
          </label>
          <input 
            type="range" 
            min="512" 
            max="8192" 
            step="512" 
            className="config-slider"
            value={localConfig.maxTokens}
            onChange={(e) => setLocalConfig({...localConfig, maxTokens: parseInt(e.target.value)})}
            disabled={isLoading}
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-save" disabled={isLoading}>
            <Save size={16} /> Save Configuration
          </button>
        </div>
      </form>
    </div>
  );
}

export default LLMConfig;
