import "./LoadingSpinner.css";

interface Props {
  size?: "sm" | "md" | "lg";
  label?: string;
  fullScreen?: boolean;
}

function LoadingSpinner({ size = "md", label, fullScreen = false }: Props) {
  const containerClass = `loading-spinner-container ${fullScreen ? 'loading-spinner-container--fullscreen' : ''}`;
  const spinnerClass = `loading-spinner loading-spinner--${size}`;

  return (
    <div className={containerClass}>
      <div className={spinnerClass}></div>
      {label && <p className="loading-spinner-label">{label}</p>}
    </div>
  );
}

export default LoadingSpinner;
