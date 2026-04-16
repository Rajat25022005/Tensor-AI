import "./Dashboard.css";

function Dashboard() {
  return (
    <div className="dashboard" id="dashboard-page">
      <h1 className="dashboard__title">
        Welcome to <span className="gradient-text">TensorAI</span>
      </h1>
      <p className="dashboard__subtitle">
        Your autonomous business intelligence platform
      </p>

      <div className="dashboard__grid">
        <div className="dashboard__card glass">
          <span className="dashboard__card-icon">📄</span>
          <h3 className="dashboard__card-title">Documents Indexed</h3>
          <p className="dashboard__card-value">—</p>
        </div>
        <div className="dashboard__card glass">
          <span className="dashboard__card-icon">🔗</span>
          <h3 className="dashboard__card-title">Graph Entities</h3>
          <p className="dashboard__card-value">—</p>
        </div>
        <div className="dashboard__card glass">
          <span className="dashboard__card-icon">💬</span>
          <h3 className="dashboard__card-title">Queries Processed</h3>
          <p className="dashboard__card-value">—</p>
        </div>
        <div className="dashboard__card glass">
          <span className="dashboard__card-icon">🧠</span>
          <h3 className="dashboard__card-title">Agent Accuracy</h3>
          <p className="dashboard__card-value">—</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
