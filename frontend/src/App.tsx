import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/layout/Layout";
import Dashboard from "./pages/Dashboard";
import QueryPage from "./pages/QueryPage";
import GraphExplorer from "./pages/GraphExplorer";
import IngestionPage from "./pages/IngestionPage";
import SettingsPage from "./pages/SettingsPage";
import ErrorBoundary from "./components/common/ErrorBoundary";

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="query" element={<QueryPage />} />
            <Route path="graph" element={<GraphExplorer />} />
            <Route path="ingest" element={<IngestionPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;

