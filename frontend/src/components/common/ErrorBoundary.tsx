import { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: '2rem',
          textAlign: 'center',
          background: 'var(--surface-glass)',
          borderRadius: 'var(--radius-lg)',
          margin: '2rem',
          border: '1px solid #ef4444'
        }}>
          <h1 style={{ color: '#ef4444', marginBottom: '1rem' }}>Something went wrong</h1>
          <p style={{ color: 'var(--text-dim)', marginBottom: '1.5rem' }}>
            We've encountered an unexpected error. Please try refreshing the page.
          </p>
          <button
            onClick={() => window.location.reload()}
            style={{
              padding: '0.75rem 1.5rem',
              background: 'var(--gradient-primary)',
              color: 'var(--color-bg)',
              borderRadius: 'var(--radius-md)',
              fontWeight: 600,
              border: 'none',
              cursor: 'pointer'
            }}
          >
            Refresh Page
          </button>
          {this.state.error && (
            <pre style={{
              marginTop: '2rem',
              padding: '1rem',
              background: 'rgba(0,0,0,0.3)',
              color: '#ef4444',
              fontSize: '0.75rem',
              textAlign: 'left',
              overflowX: 'auto',
              borderRadius: 'var(--radius-sm)'
            }}>
              {this.state.error.toString()}
            </pre>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
