import { Link } from "react-router-dom";
import "./GraphTopology.css";

function GraphTopology() {
  return (
    <div className="panel col-8">
      <div className="panel__header">
        <span className="panel__title">AUTONOMOUS_GRAPH_TOPOLOGY</span>
        <Link to="/graph" className="graph-explore-link">EXPLORE_DEEP &rarr;</Link>
      </div>
      <div className="graph-viz">
        {/* Node placements (simulated for dashboard) */}
        <div className="node-circle" style={{ left: "50%", top: "45%", width: "16px", height: "16px" }}></div>
        <div className="node-label" style={{ left: "50%", top: "45%", transform: "translateX(-50%)" }}>CENTRAL_ID_CORP</div>

        <div className="node-circle" style={{ left: "30%", top: "30%" }}></div>
        <div className="node-label" style={{ left: "30%", top: "30%" }}>VENDOR_RISK</div>

        <div className="node-circle" style={{ left: "70%", top: "25%" }}></div>
        <div className="node-label" style={{ left: "70%", top: "25%" }}>COMPLIANCE_2025</div>

        <div className="node-circle" style={{ left: "25%", top: "70%" }}></div>
        <div className="node-label" style={{ left: "25%", top: "70%" }}>Q4_REVENUE</div>

        <div className="node-circle" style={{ left: "75%", top: "75%" }}></div>
        <div className="node-label" style={{ left: "75%", top: "75%" }}>LEGAL_CONTRACTS</div>

        {/* Vector lines simulated */}
        <svg width="100%" height="100%" className="graph-edges">
          <line x1="50%" y1="45%" x2="30%" y2="30%" />
          <line x1="50%" y1="45%" x2="70%" y2="25%" />
          <line x1="50%" y1="45%" x2="25%" y2="70%" />
          <line x1="50%" y1="45%" x2="75%" y2="75%" />
          <line x1="30%" y1="30%" x2="70%" y2="25%" />
        </svg>
      </div>
    </div>
  );
}

export default GraphTopology;
