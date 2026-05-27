"use client";

import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Navigation */}
      <nav className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold text-slate-900">
            Crime & Law Explorer
          </div>
          <div className="flex gap-6">
            <Link href="/public/map" className="text-slate-700 hover:text-slate-900">
              Map
            </Link>
            <Link href="/public/statutes" className="text-slate-700 hover:text-slate-900">
              Laws
            </Link>
            <Link href="/public/about" className="text-slate-700 hover:text-slate-900">
              About
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 to-blue-800 text-white py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-6">
            Understand Crime & Law in Canada
          </h1>
          <p className="text-xl text-blue-100 mb-8">
            Explore where crimes occur, what laws apply, and why crime matters
            in the context of Canadian law. A platform for civic education and
            transparency.
          </p>
          <Link
            href="/public/map"
            className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition"
          >
            Explore the Map
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-6 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-8 rounded-lg border border-slate-200">
            <div className="text-4xl mb-4">📍</div>
            <h3 className="text-xl font-bold mb-3 text-slate-900">
              Where Crimes Happen
            </h3>
            <p className="text-slate-600">
              View crime incidents on an interactive map of Canada. Filter by
              location, date, and type to understand local crime patterns.
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg border border-slate-200">
            <div className="text-4xl mb-4">⚖️</div>
            <h3 className="text-xl font-bold mb-3 text-slate-900">
              Relevant Laws
            </h3>
            <p className="text-slate-600">
              Discover which Canadian federal laws apply to each incident.
              Understand the legal framework and why certain crimes matter.
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg border border-slate-200">
            <div className="text-4xl mb-4">📰</div>
            <h3 className="text-xl font-bold mb-3 text-slate-900">
              News Coverage
            </h3>
            <p className="text-slate-600">
              Read news articles about incidents. Verify facts through multiple
              sources and understand public context.
            </p>
          </div>
        </div>
      </section>

      {/* Educational Note */}
      <section className="bg-blue-50 border-t border-b border-blue-200 py-12 px-6 my-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">
            Civic Education Platform
          </h2>
          <p className="text-slate-700 mb-3">
            This platform exists to help Canadian citizens understand their legal
            system and how it applies to real-world incidents.
          </p>
          <ul className="space-y-2 text-slate-700">
            <li>✓ Evidence-based: All incidents verified and sourced</li>
            <li>✓ Transparent: See exactly why crimes link to laws</li>
            <li>✓ Educational: Plain-language explanations of complex law</li>
            <li>✓ Always free: No login required, no tracking</li>
          </ul>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-6 text-center">
        <h2 className="text-3xl font-bold text-slate-900 mb-6">
          Start exploring now
        </h2>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/public/map"
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            View Crime Map
          </Link>
          <Link
            href="/public/statutes"
            className="bg-slate-200 text-slate-900 px-8 py-3 rounded-lg font-semibold hover:bg-slate-300 transition"
          >
            Browse Laws
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-300 py-12 px-6 mt-16">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8 mb-8">
            <div>
              <h4 className="font-bold text-white mb-4">Platform</h4>
              <ul className="space-y-2">
                <li>
                  <Link href="/public/map" className="hover:text-white">
                    Crime Map
                  </Link>
                </li>
                <li>
                  <Link href="/public/statutes" className="hover:text-white">
                    Statutes
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-white mb-4">About</h4>
              <ul className="space-y-2">
                <li>
                  <Link href="/public/about" className="hover:text-white">
                    About This Project
                  </Link>
                </li>
                <li>
                  <Link href="/public/methodology" className="hover:text-white">
                    Methodology
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-white mb-4">Data</h4>
              <p className="text-sm">
                All data comes from official Canadian sources and public records.
              </p>
            </div>
          </div>
          <div className="border-t border-slate-800 pt-8 text-center text-sm">
            <p>
              © 2026 Crime & Law Explorer. Educational use only. Not legal
              advice.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
