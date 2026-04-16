import { useQueryStore } from "../stores/queryStore";
import QueryInterface from "../components/query/QueryInterface";
import ReasoningTrace from "../components/query/ReasoningTrace";
import { BrainCircuit } from "lucide-react";
import "./QueryPage.css";

function QueryPage() {
  const { answer, sources, reasoningTrace, error, isLoading } = useQueryStore();

  return (
    <div className="query-page">
      <div className="page-header">
        <h1 className="page-title"><BrainCircuit className="inline-icon" /> Autonomous Intelligence</h1>
        <p className="page-subtitle">Interact with the multi-agent reasoning engine.</p>
      </div>

      <div className="query-container">
        <QueryInterface />
        
        {error && (
          <div className="query-error glass">{error}</div>
        )}

        {isLoading && (
          <div className="query-loading">
            <div className="loading-spinner" style={{width: 30, height: 30}} />
            <span>Agentic simulation in progress...</span>
          </div>
        )}

        {answer && !isLoading && (
          <div className="query-results fade-in">
            <div className="answer-card glass">
              <h3>Synthesized Answer</h3>
              <div className="answer-content">{answer}</div>
              
              {sources.length > 0 && (
                <div className="answer-sources">
                  <strong>Sources verified:</strong>
                  <ul>
                    {sources.map((src, i) => (
                      <li key={i}>{src}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <ReasoningTrace steps={reasoningTrace} />
          </div>
        )}
      </div>
    </div>
  );
}

export default QueryPage;
