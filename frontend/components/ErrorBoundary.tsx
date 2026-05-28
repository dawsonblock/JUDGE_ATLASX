"use client";

import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

/**
 * ErrorBoundary
 *
 * Wraps subtrees that may throw during rendering. Renders a fallback UI
 * instead of crashing the whole app. Use around data-heavy admin panels or
 * third-party map components that can throw on bad data.
 *
 * Usage:
 *   <ErrorBoundary>
 *     <MyWidget />
 *   </ErrorBoundary>
 *
 *   <ErrorBoundary fallback={<p>Custom error</p>}>
 *     <RiskyComponent />
 *   </ErrorBoundary>
 */
export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({ errorInfo });
    // Log to console in development; in production this would go to a
    // structured error tracking service (Sentry, etc.)
    console.error("[ErrorBoundary] Caught unhandled render error:", error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div
          role="alert"
          className="rounded-lg border border-red-200 bg-red-50 p-6 text-sm"
        >
          <h2 className="font-semibold text-red-800 mb-1">Something went wrong</h2>
          <p className="text-red-700 mb-3">
            This component encountered an unexpected error and could not render.
          </p>
          {this.state.error && (
            <pre className="text-xs text-red-600 bg-red-100 rounded p-3 overflow-auto mb-3 max-h-40">
              {this.state.error.message}
            </pre>
          )}
          <button
            onClick={this.handleReset}
            className="rounded px-3 py-1.5 text-xs font-medium bg-red-700 text-white hover:bg-red-800 transition-colors"
          >
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
