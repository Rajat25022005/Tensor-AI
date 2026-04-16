import { NavLink } from "react-router-dom";
import "./Sidebar.css";

const navItems = [
  { path: "/", label: "Dashboard", icon: "📊" },
  { path: "/query", label: "Query", icon: "💬" },
  { path: "/graph", label: "Graph Explorer", icon: "🔗" },
  { path: "/ingest", label: "Ingestion", icon: "📄" },
  { path: "/settings", label: "Settings", icon: "⚙️" },
];

function Sidebar() {
  return (
    <aside className="sidebar glass">
      <div className="sidebar__brand">
        <span className="sidebar__logo gradient-text">T</span>
        <h1 className="sidebar__title">TensorAI</h1>
      </div>

      <nav className="sidebar__nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              `sidebar__link ${isActive ? "sidebar__link--active" : ""}`
            }
          >
            <span className="sidebar__link-icon">{item.icon}</span>
            <span className="sidebar__link-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar__footer">
        <span className="sidebar__version">v0.1.0</span>
      </div>
    </aside>
  );
}

export default Sidebar;
