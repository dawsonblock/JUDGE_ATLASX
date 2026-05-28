import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Crime & Law in Canada — Civic Education Platform",
  description:
    "Understand where crimes happen, what laws apply, and why. Evidence-backed, publicly available data from official Canadian sources.",
};

const FEATURES = [
  {
    heading: "Where crimes happen",
    body: "Interactive map of Canada showing verified crime incidents. Filter by location, date, and offence type to understand patterns in your area.",
    href: "/public/map",
    cta: "Open map",
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <path
          d="M10 2C6.686 2 4 4.686 4 8c0 4.418 6 10 6 10s6-5.582 6-10c0-3.314-2.686-6-6-6zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"
          fill="currentColor"
        />
      </svg>
    ),
  },
  {
    heading: "Which laws apply",
    body: "Each incident is cross-referenced with relevant sections of the Criminal Code and other Canadian federal statutes, with an AI-generated explanation of relevance.",
    href: "/public/statutes",
    cta: "Browse statutes",
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <rect x="3" y="2" width="14" height="16" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M7 7h6M7 10h6M7 13h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    heading: "Context and coverage",
    body: "Related news coverage and a plain-language explanation of why each crime matters in the context of Canadian law — educational, not alarmist.",
    href: "/public/map",
    cta: "Explore incidents",
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <rect x="2" y="4" width="16" height="12" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M2 8h16" stroke="currentColor" strokeWidth="1.5" />
        <path d="M6 12h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
  },
];

const TRUST_ITEMS = [
  {
    label: "Official sources only",
    detail: "All data sourced from government and verified public records.",
  },
  {
    label: "Confidence-scored links",
    detail: "Every statute link carries an AI confidence score so you can judge reliability.",
  },
  {
    label: "Educational, not legal advice",
    detail: "Explanations are for civic understanding. Consult a lawyer for legal guidance.",
  },
  {
    label: "No login required",
    detail: "Fully public. No tracking, no account needed.",
  },
];

const STAT_ITEMS = [
  { value: "26", label: "Active sources" },
  { value: "13", label: "Provinces & territories" },
  { value: "100+", label: "Federal statutes indexed" },
  { value: "Public", label: "Always free, no login" },
];

export default function LandingPage() {
  return (
    <div className="flex flex-col">
      {/* ── Hero ─────────────────────────────────────────── */}
      <section
        className="px-6 py-20 md:py-28"
        style={{ background: "var(--pub-navy)" }}
      >
        <div className="max-w-3xl mx-auto text-center">
          <p
            className="text-xs font-semibold uppercase tracking-widest mb-5 inline-block px-3 py-1 rounded-full"
            style={{
              background: "rgba(255,255,255,0.12)",
              color: "rgba(255,255,255,0.85)",
            }}
          >
            Civic Education Platform — Canada
          </p>
          <h1
            className="text-4xl md:text-5xl font-bold leading-tight mb-5 text-balance"
            style={{ color: "#fff", letterSpacing: "-0.02em" }}
          >
            Understand crime and law
            <br className="hidden md:block" /> in Canada
          </h1>
          <p
            className="text-lg leading-relaxed mb-10 text-pretty mx-auto"
            style={{ color: "rgba(255,255,255,0.72)", maxWidth: "560px" }}
          >
            Explore where incidents occur, which statutes apply, and why crimes
            matter in the context of Canadian federal law. Evidence-backed,
            always free.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link
              href="/public/map"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded font-semibold text-sm transition-opacity hover:opacity-90"
              style={{ background: "#fff", color: "var(--pub-navy)" }}
            >
              Open Crime Map
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                <path
                  d="M3 7h8M8 4l3 3-3 3"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </Link>
            <Link
              href="/public/statutes"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded font-semibold text-sm transition-opacity hover:opacity-90"
              style={{
                background: "rgba(255,255,255,0.1)",
                color: "#fff",
                border: "1px solid rgba(255,255,255,0.22)",
              }}
            >
              Browse Statutes
            </Link>
          </div>
        </div>
      </section>

      {/* ── Stats bar ────────────────────────────────────── */}
      <div
        className="border-b"
        style={{
          background: "var(--pub-surface)",
          borderColor: "var(--pub-border)",
        }}
      >
        <div className="max-w-5xl mx-auto px-6 py-5 grid grid-cols-2 md:grid-cols-4 divide-x"
          style={{ divideColor: "var(--pub-border)" }}
        >
          {STAT_ITEMS.map(({ value, label }) => (
            <div key={label} className="text-center px-4 first:pl-0 last:pr-0">
              <p
                className="text-2xl font-bold"
                style={{ color: "var(--pub-navy)" }}
              >
                {value}
              </p>
              <p className="text-xs mt-0.5" style={{ color: "var(--pub-muted)" }}>
                {label}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* ── Features ─────────────────────────────────────── */}
      <section className="px-6 py-16" style={{ background: "var(--pub-bg)" }}>
        <div className="max-w-5xl mx-auto">
          <h2
            className="text-2xl font-bold mb-1 text-balance"
            style={{ color: "var(--pub-ink)", letterSpacing: "-0.01em" }}
          >
            What you can explore
          </h2>
          <p className="text-sm mb-10" style={{ color: "var(--pub-muted)" }}>
            Three interconnected lenses on Canadian crime and law.
          </p>
          <div className="grid md:grid-cols-3 gap-5">
            {FEATURES.map(({ heading, body, href, cta, icon }) => (
              <div
                key={heading}
                className="rounded-lg p-6 flex flex-col gap-4"
                style={{
                  background: "var(--pub-surface)",
                  border: "1px solid var(--pub-border)",
                }}
              >
                <div
                  className="w-9 h-9 rounded flex items-center justify-center flex-shrink-0"
                  style={{
                    background: "rgba(15,76,117,0.08)",
                    color: "var(--pub-navy)",
                  }}
                >
                  {icon}
                </div>
                <div className="flex-1">
                  <h3
                    className="font-semibold mb-2 text-base"
                    style={{ color: "var(--pub-ink)" }}
                  >
                    {heading}
                  </h3>
                  <p
                    className="text-sm leading-relaxed"
                    style={{ color: "var(--pub-muted)" }}
                  >
                    {body}
                  </p>
                </div>
                <Link
                  href={href}
                  className="text-sm font-medium hover:underline inline-flex items-center gap-1"
                  style={{ color: "var(--pub-navy)" }}
                >
                  {cta}
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                    <path
                      d="M2 6h8M7 3l3 3-3 3"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Trust section ────────────────────────────────── */}
      <section
        className="px-6 py-14"
        style={{
          background: "var(--pub-surface)",
          borderTop: "1px solid var(--pub-border)",
          borderBottom: "1px solid var(--pub-border)",
        }}
      >
        <div className="max-w-5xl mx-auto">
          <h2
            className="text-xl font-bold mb-8 text-balance"
            style={{ color: "var(--pub-ink)", letterSpacing: "-0.01em" }}
          >
            Built for transparency
          </h2>
          <div className="grid sm:grid-cols-2 gap-6">
            {TRUST_ITEMS.map(({ label, detail }) => (
              <div key={label} className="flex items-start gap-3">
                <span
                  className="mt-0.5 flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center"
                  style={{
                    background: "rgba(27,138,90,0.1)",
                    color: "var(--pub-teal)",
                  }}
                  aria-hidden="true"
                >
                  <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                    <path
                      d="M2 5l2.5 2.5L8 3"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </span>
                <div>
                  <p
                    className="text-sm font-semibold mb-0.5"
                    style={{ color: "var(--pub-ink)" }}
                  >
                    {label}
                  </p>
                  <p className="text-sm" style={{ color: "var(--pub-muted)" }}>
                    {detail}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────── */}
      <section className="px-6 py-16 text-center" style={{ background: "var(--pub-bg)" }}>
        <div className="max-w-xl mx-auto">
          <h2
            className="text-2xl font-bold mb-3 text-balance"
            style={{ color: "var(--pub-ink)", letterSpacing: "-0.01em" }}
          >
            Start exploring now
          </h2>
          <p className="text-sm mb-8" style={{ color: "var(--pub-muted)" }}>
            No account needed. All data is public and free.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link
              href="/public/map"
              className="inline-flex items-center justify-center px-6 py-3 rounded font-semibold text-sm transition-opacity hover:opacity-90"
              style={{ background: "var(--pub-navy)", color: "#fff" }}
            >
              View Crime Map
            </Link>
            <Link
              href="/public/statutes"
              className="inline-flex items-center justify-center px-6 py-3 rounded font-semibold text-sm transition-colors hover:underline"
              style={{
                background: "var(--pub-surface)",
                color: "var(--pub-navy)",
                border: "1px solid var(--pub-border-md)",
              }}
            >
              Browse Laws
            </Link>
          </div>
        </div>
      </section>

      {/* ── Disclaimer strip ─────────────────────────────── */}
      <div
        className="px-6 py-3 text-center text-xs"
        style={{
          background: "var(--pub-warn-bg)",
          borderTop: "1px solid #FDE68A",
          color: "var(--pub-warn)",
        }}
      >
        This platform is for{" "}
        <strong>educational purposes only</strong> and does not constitute legal
        advice. Data may be incomplete. Always consult official sources.
      </div>
    </div>
  );
}
