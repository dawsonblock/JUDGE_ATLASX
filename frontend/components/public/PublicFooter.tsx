import Link from "next/link";

export default function PublicFooter() {
  return (
    <footer
      className="mt-auto"
      style={{ borderTop: "1px solid var(--pub-border)", background: "var(--pub-surface)" }}
    >
      <div className="max-w-7xl mx-auto px-6 py-10">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1">
            <p
              className="font-semibold text-sm mb-2"
              style={{ color: "var(--pub-ink)" }}
            >
              JUDGE AtlasX
            </p>
            <p className="text-xs leading-relaxed" style={{ color: "var(--pub-muted)" }}>
              A civic education platform for understanding crime and law in Canada.
              Not legal advice.
            </p>
          </div>

          {/* Explore */}
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider mb-3" style={{ color: "var(--pub-muted)" }}>
              Explore
            </p>
            <ul className="space-y-2">
              {[
                { href: "/public/map", label: "Crime Map" },
                { href: "/public/statutes", label: "Statute Browser" },
              ].map(({ href, label }) => (
                <li key={href}>
                  <Link
                    href={href}
                    className="text-sm hover:underline"
                    style={{ color: "var(--pub-text)" }}
                  >
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Platform */}
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider mb-3" style={{ color: "var(--pub-muted)" }}>
              Platform
            </p>
            <ul className="space-y-2">
              {[
                { href: "/public/about", label: "About" },
                { href: "/public/about#methodology", label: "Methodology" },
                { href: "/public/about#limitations", label: "Limitations" },
              ].map(({ href, label }) => (
                <li key={href}>
                  <Link
                    href={href}
                    className="text-sm hover:underline"
                    style={{ color: "var(--pub-text)" }}
                  >
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Data */}
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider mb-3" style={{ color: "var(--pub-muted)" }}>
              Data
            </p>
            <p className="text-sm" style={{ color: "var(--pub-muted)" }}>
              Sourced from official Canadian government records and public datasets.
              Updated regularly.
            </p>
          </div>
        </div>

        <div
          className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs"
          style={{ borderTop: "1px solid var(--pub-border)", color: "var(--pub-muted)" }}
        >
          <p>&copy; 2026 JUDGE AtlasX. Educational use only.</p>
          <p>Not affiliated with any government body. Data is provided as-is.</p>
        </div>
      </div>
    </footer>
  );
}
