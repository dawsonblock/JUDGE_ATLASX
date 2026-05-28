"use client";

import Link from "next/link";

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-xl font-bold text-slate-900">
              Crime & Law Explorer
            </Link>
            <nav className="flex gap-6">
              <Link href="/public/map" className="text-slate-700 hover:text-slate-900">
                Map
              </Link>
              <Link href="/public/statutes" className="text-slate-700 hover:text-slate-900">
                Laws
              </Link>
              <Link href="/public/about" className="text-blue-600 font-semibold">
                About
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold text-slate-900 mb-8">
          About Crime & Law Explorer
        </h1>

        {/* Mission Section */}
        <section className="bg-white rounded-lg border border-slate-200 p-8 mb-8">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">
            Our Mission
          </h2>
          <p className="text-slate-700 leading-relaxed mb-4">
            Crime & Law Explorer is a civic education platform that helps Canadian
            citizens understand their legal system. We believe that transparency
            about crimes, laws, and their relationship strengthens democratic
            institutions and public trust.
          </p>
          <p className="text-slate-700 leading-relaxed">
            By connecting real crime incidents to the laws that govern them, we
            empower citizens to engage meaningfully with their legal system.
          </p>
        </section>

        {/* Data Sources Section */}
        <section className="bg-white rounded-lg border border-slate-200 p-8 mb-8">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">
            Data Sources
          </h2>
          <p className="text-slate-700 mb-6">
            All crime data comes from official Canadian sources:
          </p>
          <ul className="space-y-3 text-slate-700 ml-6">
            <li className="list-disc">
              <strong>Canadian Courts:</strong> Court records and judicial proceedings
            </li>
            <li className="list-disc">
              <strong>Law Enforcement:</strong> Official police and law enforcement data
            </li>
            <li className="list-disc">
              <strong>News Archives:</strong> Verified news coverage from Canadian publications
            </li>
            <li className="list-disc">
              <strong>Public Records:</strong> Publicly available government data
            </li>
          </ul>
          <p className="text-slate-700 mt-6">
            Canadian statutes are sourced from the Department of Justice Canada and
            are current as of the last update of this database.
          </p>
        </section>

        {/* How It Works Section */}
        <section className="bg-white rounded-lg border border-slate-200 p-8 mb-8">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">
            How It Works
          </h2>
          <div className="space-y-6">
            <div>
              <h3 className="font-bold text-slate-900 mb-2">
                1. Crime Data Ingestion
              </h3>
              <p className="text-slate-700">
                We ingest crime incidents from official Canadian sources and verify
                their accuracy through multiple reviews.
              </p>
            </div>
            <div>
              <h3 className="font-bold text-slate-900 mb-2">
                2. AI-Powered Legal Linking
              </h3>
              <p className="text-slate-700">
                Using Claude AI, we identify which Canadian federal statutes are
                relevant to each crime. Our AI provides confidence scores for each
                match and explains the relevance.
              </p>
            </div>
            <div>
              <h3 className="font-bold text-slate-900 mb-2">
                3. Human Review
              </h3>
              <p className="text-slate-700">
                Our team reviews AI suggestions before they appear on the platform,
                ensuring accuracy and preventing errors.
              </p>
            </div>
            <div>
              <h3 className="font-bold text-slate-900 mb-2">
                4. Public Education
              </h3>
              <p className="text-slate-700">
                Citizens can explore incidents on our map, read AI-generated
                explanations of why crimes relate to laws, and access news coverage.
              </p>
            </div>
          </div>
        </section>

        {/* Limitations Section */}
        <section className="bg-amber-50 border border-amber-200 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">
            Important Limitations
          </h2>
          <ul className="space-y-3 text-slate-700 ml-6">
            <li className="list-disc">
              <strong>Not Legal Advice:</strong> This platform is educational only.
              If you need legal advice, consult a qualified lawyer.
            </li>
            <li className="list-disc">
              <strong>AI-Generated Content:</strong> Explanations are generated by AI
              and may contain errors. Always verify with official sources.
            </li>
            <li className="list-disc">
              <strong>Incomplete Data:</strong> Not all crimes are reported or included
              in official records. This is not a complete picture of crime.
            </li>
            <li className="list-disc">
              <strong>Historical Data Only:</strong> This platform shows past incidents,
              not current investigations or ongoing cases.
            </li>
            <li className="list-disc">
              <strong>Privacy:</strong> Individual privacy is protected. Where possible,
              personal identifiers are anonymized or omitted.
            </li>
          </ul>
        </section>

        {/* Privacy Section */}
        <section className="bg-white rounded-lg border border-slate-200 p-8 mb-8">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">
            Privacy & No Tracking
          </h2>
          <p className="text-slate-700 mb-4">
            Crime & Law Explorer respects your privacy:
          </p>
          <ul className="space-y-2 text-slate-700 ml-6">
            <li className="list-disc">No user accounts required</li>
            <li className="list-disc">No cookies or tracking pixels</li>
            <li className="list-disc">No data collection or sale</li>
            <li className="list-disc">All searches are anonymous</li>
          </ul>
        </section>

        {/* Contact Section */}
        <section className="bg-blue-50 border border-blue-200 rounded-lg p-8">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">
            Questions?
          </h2>
          <p className="text-slate-700 mb-4">
            Have questions or feedback about this platform? We&apos;d love to hear from you.
          </p>
          <p className="text-slate-700">
            Contact us at:{" "}
            <a href="mailto:info@crimeandlawexplorer.ca" className="text-blue-600 hover:text-blue-700 underline">
              info@crimeandlawexplorer.ca
            </a>
          </p>
        </section>

        {/* Footer CTA */}
        <div className="text-center mt-12">
          <Link
            href="/public/map"
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Back to Map
          </Link>
        </div>
      </div>
    </div>
  );
}
