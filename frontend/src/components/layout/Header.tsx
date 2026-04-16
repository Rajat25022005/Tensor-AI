import "./Header.css";

function Header() {
  return (
    <header className="header glass">
      <div className="header__search">
        <input
          type="text"
          placeholder="Search knowledge base..."
          className="header__search-input"
          id="global-search"
        />
      </div>
      <div className="header__actions">
        <div className="header__status">
          <span className="header__status-dot header__status-dot--active" />
          <span className="header__status-label">Ollama Connected</span>
        </div>
      </div>
    </header>
  );
}

export default Header;
