import type { ReasoningStep } from "../../types";
import "./ReasoningTrace.css";

interface Props {
  steps: ReasoningStep[];
}

function ReasoningTrace({ steps }: Props) {
  if (steps.length === 0) return null;

  return (
    <div className="reasoning-trace glass">
      <h3 className="reasoning-trace__title">Reasoning Trace</h3>
      <div className="reasoning-trace__list">
        {steps.map((step, i) => (
          <div key={i} className="reasoning-trace__step">
            <div className="reasoning-trace__agent">
              {step.agent} &rarr; {step.action}
            </div>
            <div className="reasoning-trace__summary">
              {step.output_summary}
            </div>
            <div className="reasoning-trace__duration">
              {step.duration_ms.toFixed(0)}ms
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ReasoningTrace;
