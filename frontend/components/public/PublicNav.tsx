"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

interface PublicNavProps {
  /** Hides the sticky border on pages where the hero provides separation */
  transparent?: boolean;
}

const NAV_LINKS = [
  { href: "/public/map", label: "Crime Map" },
  { href: "/public/statutes", label: "Laws" },
  { href: "/public/about", label: "About" },
];

export default function PublicNav({ transparent = false }: PublicNavProps) {
  const pathname = usePathname();

  return (
    <header
      className="sticky top-0 z-30 bg-white"
      style={{ borderBottom: transparent ? "none" : "1px solid var(--pub-border)" }}
    >
      <div className="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
        {/* Wordmark */}
        <Link
          href="/public"
          className="flex items-center gap-2.5 text-[var(--pub-navy)] hover:text-[var(--pub-navy-dark)] transition-colors"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
            <rect width="20" height="20" rx="4" fill="currentColor" opacity="0.12" />
            <path
              d="M4 14 L10 4 L16 14"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <line
              x1="6.5"
              y1="11"
              x2="13.5"
              y2="11"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
          </svg>
          <span
            className="font-semibold text-sm tracking-tight"
            style={{ color: "var(--pub-ink)" }}
          >
            JUDGE AtlasX
          </span>
          <span
            className="text-xs px-1.5 py-0.5 rounded font-medium"
            style={{
              background: "var(--pub-teal)",
              color: "#fff",
              fontSize: "10px",
              letterSpacing: "0.04em",
            }}
          >
            PUBLIC
          </span>
        </Link>

        {/* Nav links */}
        <nav className="flex items-center gap-1" aria-label="Public navigation">
          {NAV_LINKS.map(({ href, label }) => {
            const active = pathname === href || pathname.startsWith(href + "/");
            return (
              <Link
                key={href}
                href={href}
                className="px-3 py-1.5 rounded text-sm font-medium transition-colors"
                style={{
                  color: active ? "var(--pub-navy)" : "var(--pub-muted)",
                  background: active ? "rgba(15,76,117,0.07)" : "transparent",
                }}
              >
                {label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
