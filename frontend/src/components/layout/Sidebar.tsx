import { NavLink } from "react-router-dom";
import { LayoutDashboard, Network, Brain, FileText, Settings, Plug } from "lucide-react";
import "./Sidebar.css";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <div className="sidebar__logo">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#091413" strokeWidth="3">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
          </svg>
        </div>
        <span className="sidebar__title">TensorAI</span>
      </div>

      <div className="sidebar__section">
        <div className="sidebar__label">Core View</div>
        <nav className="sidebar__nav">
          <NavLink to="/" end className={({ isActive }) => `sidebar__link ${isActive ? "sidebar__link--active" : ""}`}>
            <LayoutDashboard className="sidebar__icon" />
            <span className="sidebar__link-label">Dashboard</span>
          </NavLink>
          <NavLink to="/graph" className={({ isActive }) => `sidebar__link ${isActive ? "sidebar__link--active" : ""}`}>
            <Network className="sidebar__icon" />
            <span className="sidebar__link-label">Knowledge Graph</span>
          </NavLink>
          <NavLink to="/query" className={({ isActive }) => `sidebar__link ${isActive ? "sidebar__link--active" : ""}`}>
            <Brain className="sidebar__icon" />
            <span className="sidebar__link-label">Intelligence</span>
          </NavLink>
        </nav>
      </div>

      <div className="sidebar__section">
        <div className="sidebar__label">Management</div>
        <nav className="sidebar__nav">
          <NavLink to="/ingest" className={({ isActive }) => `sidebar__link ${isActive ? "sidebar__link--active" : ""}`}>
            <FileText className="sidebar__icon" />
            <span className="sidebar__link-label">Documents</span>
          </NavLink>
          <NavLink to="/settings#connectors" className={({ isActive }) => `sidebar__link ${isActive ? "sidebar__link--active" : ""}`}>
            <Plug className="sidebar__icon" />
            <span className="sidebar__link-label">Connectors</span>
          </NavLink>
          <NavLink to="/settings" end className={({ isActive }) => `sidebar__link ${isActive ? "sidebar__link--active" : ""}`}>
            <Settings className="sidebar__icon" />
            <span className="sidebar__link-label">System Settings</span>
          </NavLink>
        </nav>
      </div>
    </aside>
  );
}

export default Sidebar;
