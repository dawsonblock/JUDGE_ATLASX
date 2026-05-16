import { notFound } from "next/navigation";

export async function generateMetadata({ params }: { params: { id: string } }) {
  return {
    title: `Record ${params.id} | JUDGE`,
    description: "Publicly reviewed court record detail.",
  };
}

async function fetchRecord(id: string) {
  const apiBase =
    process.env.BACKEND_INTERNAL_URL ??
    process.env.NEXT_PUBLIC_API_BASE_URL ??
    process.env.NEXT_PUBLIC_API_URL ??
    "http://localhost:8000";
  const res = await fetch(
    `${apiBase}/api/v1/records/${encodeURIComponent(id)}`,
    {
      next: { revalidate: 60 },
    },
  );
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export default async function RecordDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const record = await fetchRecord(params.id).catch(() => null);

  if (!record) {
    notFound();
  }

  return (
    <main className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-xl font-semibold text-gray-900 mb-1">
        Public Record
      </h1>
      <p className="text-sm text-gray-500 mb-6">ID: {params.id}</p>

      <div className="rounded border border-gray-200 bg-white divide-y divide-gray-100 text-sm">
        {Object.entries(record as Record<string, unknown>).map(
          ([key, value]) => (
            <div key={key} className="flex gap-4 px-4 py-2">
              <span className="w-40 shrink-0 font-medium text-gray-600">
                {key}
              </span>
              <span className="text-gray-800 break-all">
                {value === null || value === undefined ? (
                  <span className="text-gray-400 italic">—</span>
                ) : (
                  String(value)
                )}
              </span>
            </div>
          ),
        )}
      </div>

      <p className="mt-6 text-xs text-gray-400">
        This page displays publicly available reviewed records only. Records are
        sourced from official public data. No inference about guilt,
        culpability, or misconduct is made or implied.
      </p>
    </main>
  );
}
