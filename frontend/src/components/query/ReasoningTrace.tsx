import type { ReasoningStep } from "../../types";

interface Props {
  steps: ReasoningStep[];
}

function ReasoningTrace({ steps }: Props) {
  if (steps.length === 0) return null;

  return (
    <div className="glass" style={{ padding: "var(--space-6)", borderRadius: "var(--radius-lg)", marginTop: "var(--space-6)" }}>
      <h3 style={{ marginBottom: "var(--space-4)", fontSize: "var(--font-size-lg)" }}>
        Reasoning Trace
      </h3>
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
        {steps.map((step, i) => (
          <div
            key={i}
            style={{
              padding: "var(--space-4)",
              background: "var(--color-bg-secondary)",
              borderRadius: "var(--radius-md)",
              borderLeft: "3px solid var(--color-accent-purple)",
            }}
          >
            <div style={{ fontSize: "var(--font-size-xs)", color: "var(--color-accent-purple)", fontWeight: 600 }}>
              {step.agent} → {step.action}
            </div>
            <div style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", marginTop: "var(--space-1)" }}>
              {step.output_summary}
            </div>
            <div style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)", marginTop: "var(--space-1)" }}>
              {step.duration_ms.toFixed(0)}ms
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ReasoningTrace;
