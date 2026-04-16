import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useEffect } from "react";
import Layout from "./components/layout/Layout";
import Dashboard from "./pages/Dashboard";
import QueryPage from "./pages/QueryPage";
import GraphExplorer from "./pages/GraphExplorer";
import IngestionPage from "./pages/IngestionPage";
import SettingsPage from "./pages/SettingsPage";
import LoginPage from "./pages/LoginPage";
import ErrorBoundary from "./components/common/ErrorBoundary";
import { useAuthStore } from "./stores/authStore";

function App() {
  const { checkSession, isAuthenticated } = useAuthStore();

  useEffect(() => {
    checkSession();
  }, [checkSession]);

  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={isAuthenticated ? <Navigate to="/" replace /> : <LoginPage />} />
          
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="query" element={<QueryPage />} />
            <Route path="graph" element={<GraphExplorer />} />
            <Route path="ingest" element={<IngestionPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
