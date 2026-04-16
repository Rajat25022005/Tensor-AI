import { useMemo, useRef, useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import "./GraphViewer.css";

interface Props {
  nodes: { id: string; name: string; type: string }[];
  edges: { source: string; target: string; label: string }[];
  onNodeClick?: (node: any) => void;
}

function GraphViewer({ nodes, edges, onNodeClick }: Props) {
  const fgRef = useRef<any>();
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const { clientWidth, clientHeight } = containerRef.current;
    setDimensions({ width: clientWidth, height: clientHeight });
    
    const handleResize = () => {
      if (!containerRef.current) return;
      setDimensions({
        width: containerRef.current.clientWidth,
        height: containerRef.current.clientHeight
      });
    };
    
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const graphData = useMemo(() => ({ nodes, links: edges }), [nodes, edges]);

  const getNodeColor = (type: string) => {
    switch (type) {
      case "COMPANY": return "#B0E4CC";
      case "VENDOR": return "#408A71";
      case "FINANCE": return "#10b981";
      case "LEGAL": return "#3b82f6";
      default: return "#408A71";
    }
  };

  return (
    <div className="graph-container glass" ref={containerRef}>
      {dimensions.width > 0 && (
        <ForceGraph2D
          ref={fgRef}
          width={dimensions.width}
          height={dimensions.height}
          graphData={graphData}
          nodeLabel="name"
          nodeColor={(node: any) => getNodeColor(node.type)}
          nodeRelSize={6}
          linkColor={() => "rgba(176, 228, 204, 0.25)"}
          linkWidth={1}
          linkDirectionalArrowLength={3.5}
          linkDirectionalArrowRelPos={1}
          onNodeClick={onNodeClick}
          cooldownTicks={100}
        />
      )}
    </div>
  );
}

export default GraphViewer;
