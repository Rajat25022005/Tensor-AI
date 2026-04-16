import "./StatPanel.css";

interface Props {
  title: string;
  value: string | number;
  metaHtml?: React.ReactNode;
  colSpan?: 4 | 6 | 8 | 12;
}

function StatPanel({ title, value, metaHtml, colSpan = 4 }: Props) {
  return (
    <div className={`panel col-${colSpan}`}>
      <div className="panel__header">
        <span className="panel__title">{title}</span>
      </div>
      <div className="panel__value">{value.toLocaleString()}</div>
      {metaHtml && <div className="panel__meta">{metaHtml}</div>}
    </div>
  );
}

export default StatPanel;
