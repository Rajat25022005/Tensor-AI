import { useState } from "react";
import { useAuthStore } from "../stores/authStore";
import { useNavigate, useLocation } from "react-router-dom";
import { Loader2 } from "lucide-react";
import "./LoginPage.css";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [localError, setLocalError] = useState("");
  const { login, isLoading, error } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || "/";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError("");
    
    if (!email || !password) {
      setLocalError("Please enter both email and password.");
      return;
    }

    const success = await login({ email, password });
    if (success) {
      navigate(from, { replace: true });
    }
  };

  return (
    <div className="login-page">
      <div className="login-card glass">
        <div className="login-header">
          <div className="login-logo">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#091413" strokeWidth="3">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
            </svg>
          </div>
          <h1>TensorAI</h1>
          <p>Login to Enterprise Intelligence</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {(error || localError) && (
            <div className="login-error">{error || localError}</div>
          )}
          
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@tensorai.dev"
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              disabled={isLoading}
            />
          </div>

          <button type="submit" className="login-btn" disabled={isLoading}>
            {isLoading ? <Loader2 className="spin" size={20} /> : "Authenticate"}
          </button>
        </form>
        
        <div className="login-footer">
          <p>Default: admin@tensorai.dev / admin1234</p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
