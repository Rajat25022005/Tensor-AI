import type { ReasoningStep } from "../../types";
import "./ReasoningLog.css";

interface Props {
  logs: ReasoningStep[];
}

function ReasoningLog({ logs }: Props) {
  // Mock timestamp generator for demo purposes
  const getDemoTime = (index: number, total: number) => {
    const base = new Date();
    base.setMinutes(base.getMinutes() - (total - index));
    return base.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  return (
    <div className="panel col-4">
      <div className="panel__header">
        <span className="panel__title">REASONING_TRACE</span>
      </div>
      <div className="log-list">
        {logs.map((log, index) => {
          const isLast = index === logs.length - 1;
          const isDone = log.agent === "DONE";
          
          return (
            <div key={index} className={`log-entry ${isDone ? 'log-entry--done' : ''}`}>
              <span className="log-tag">[{log.agent}]</span>
              <span className="log-message">{log.output_summary}</span>
              <span className="log-time">{getDemoTime(index, logs.length)}</span>
            </div>
          );
        })}
        {logs.length === 0 && (
          <div className="log-empty">No reasoning logs available</div>
        )}
      </div>
    </div>
  );
}

export default ReasoningLog;
