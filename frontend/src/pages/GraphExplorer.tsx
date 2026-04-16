import { useEffect, useState } from "react";
import { useGraphStore } from "../stores/graphStore";
import GraphViewer from "../components/graph/GraphViewer";
import { Network, ZoomIn } from "lucide-react";
import "./GraphExplorer.css";

function GraphExplorer() {
  const { nodes, edges, fetchSubgraph, isLoading } = useGraphStore();
  const [selectedNodeDetails, setSelectedNodeDetails] = useState<any>(null);

  useEffect(() => {
    fetchSubgraph(); // fetch initial root subgraph
  }, [fetchSubgraph]);

  const handleNodeClick = (node: any) => {
    setSelectedNodeDetails(node);
  };

  return (
    <div className="graph-page">
      <div className="page-header">
        <h1 className="page-title"><Network className="inline-icon" /> Knowledge Graph Explorer</h1>
        <p className="page-subtitle">Interactive topology of your enterprise data entities and relationships.</p>
      </div>

      <div className="graph-layout">
        <div className="graph-main">
          {isLoading ? (
            <div className="graph-loading glass">Initializing Autonomous Force Graph...</div>
          ) : (
            <GraphViewer 
              nodes={nodes} 
              edges={edges} 
              onNodeClick={handleNodeClick} 
            />
          )}
        </div>
        
        <div className="graph-sidebar glass">
          <div className="sidebar-header">
            <ZoomIn size={18} />
            <h3>Entity Inspector</h3>
          </div>
          
          {selectedNodeDetails ? (
            <div className="entity-details fade-in">
              <div className="detail-group">
                <label>ID</label>
                <div className="detail-val mono">{selectedNodeDetails.id}</div>
              </div>
              <div className="detail-group">
                <label>Name</label>
                <div className="detail-val">{selectedNodeDetails.name}</div>
              </div>
              <div className="detail-group">
                <label>Type</label>
                <div className="detail-val type-badge">{selectedNodeDetails.type}</div>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              Click any node in the graph to inspect its properties and adjacent edges.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default GraphExplorer;
