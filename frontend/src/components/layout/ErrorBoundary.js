import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // You can log error info here if needed
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div role="alert" className="error-boundary-container">
          <div className="error-icon" aria-hidden="true">⚠️</div>
          <h2>Something went wrong.</h2>
          <pre className="error-message">{this.state.error?.toString()}</pre>
          {this.props.fallback || null}
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary; 