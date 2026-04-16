import { Search, LogOut } from "lucide-react";
import { useAuthStore } from "../../stores/authStore";
import { useNavigate } from "react-router-dom";
import "./Header.css";

function Header() {
  const { logout, user } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <header className="header glass">
      <div className="header__search-form">
        <Search className="header__search-icon" />
        <input
          type="text"
          className="header__search-input"
          placeholder="Query knowledge base (e.g. 'Compare Q3 vs Q4 liabilities')"
        />
      </div>
      <div className="header__actions">
        <div className="header__status-badge">
          <div className="header__status-dot"></div>
          NODE_ACTIVE: OLLAMA_L3
        </div>
        <button className="header__logout" onClick={handleLogout} title="Logout">
          <LogOut size={16} />
        </button>
      </div>
    </header>
  );
}

export default Header;
