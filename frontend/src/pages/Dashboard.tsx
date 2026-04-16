import { useEffect } from "react";
import { useDashboardStore } from "../stores/dashboardStore";
import StatPanel from "../components/dashboard/StatPanel";
import GraphTopology from "../components/dashboard/GraphTopology";
import ReasoningLog from "../components/dashboard/ReasoningLog";
import "./Dashboard.css";

function Dashboard() {
  const { stats, recentLogs, fetchDashboardData } = useDashboardStore();

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1 className="page-title">Executive Overview</h1>
      </div>

      {stats && (
        <div className="dashboard-grid">
          <StatPanel 
            title="TOTAL_GRAPH_NODES" 
            value={stats.graphNodes} 
            metaHtml={<><span style={{color: 'var(--color-primary)'}}>+{stats.graphNodesTrend}</span> vs last week</>} 
          />
          <StatPanel 
            title="AGENT_CONFIDENCE" 
            value={`${stats.agentConfidence}%`} 
          />
          <StatPanel 
            title="VALIDATED_TRACES" 
            value={stats.validatedTraces} 
          />

          {/* Lower section spanning multiple columns */}
          <GraphTopology />
          <ReasoningLog logs={recentLogs} />
        </div>
      )}
    </div>
  );
}

export default Dashboard;
