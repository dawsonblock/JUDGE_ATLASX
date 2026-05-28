"use client";

import { useEffect } from "react";

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

/**
 * Global error page (Next.js App Router).
 *
 * Rendered when an unhandled error propagates up to the root layout boundary.
 * Logs the error and offers a retry button.
 */
export default function GlobalError({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    console.error("[ErrorPage] Unhandled app error:", error);
  }, [error]);

  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
        <div className="max-w-md w-full rounded-xl border border-red-200 bg-white shadow-sm p-8 text-center">
          <div className="text-4xl font-bold text-red-600 mb-2">Error</div>
          <h1 className="text-lg font-semibold text-slate-900 mb-2">
            Something went wrong
          </h1>
          <p className="text-sm text-slate-600 mb-4">
            An unexpected error occurred. If this persists, please contact your
            system administrator.
          </p>

          {error.digest && (
            <p className="text-xs text-slate-400 mb-4 font-mono">
              Error ID: {error.digest}
            </p>
          )}

          <button
            onClick={reset}
            className="rounded-lg px-5 py-2.5 text-sm font-medium bg-slate-900 text-white hover:bg-slate-700 transition-colors"
          >
            Try again
          </button>
        </div>
      </body>
    </html>
  );
}
