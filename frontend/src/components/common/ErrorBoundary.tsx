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
          background: 'var(--color-bg-secondary)',
          borderRadius: 'var(--radius-lg)',
          margin: '2rem',
          border: '1px solid var(--color-accent-red)'
        }}>
          <h1 style={{ color: 'var(--color-accent-red)', marginBottom: '1rem' }}>Something went wrong</h1>
          <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1.5rem' }}>
            We've encountered an unexpected error. Please try refreshing the page.
          </p>
          <button
            onClick={() => window.location.reload()}
            style={{
              padding: '0.75rem 1.5rem',
              background: 'var(--gradient-primary)',
              color: 'white',
              borderRadius: 'var(--radius-md)',
              fontWeight: 600
            }}
          >
            Refresh Page
          </button>
          {this.state.error && (
            <pre style={{
              marginTop: '2rem',
              padding: '1rem',
              background: 'black',
              color: '#ff5555',
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

    return this.children;
  }
}

export default ErrorBoundary;
