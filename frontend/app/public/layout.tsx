import type { Metadata } from "next";
import "../globals.css";

export const metadata: Metadata = {
  title: "Crime & Law Explorer - Canada",
  description:
    "Explore where crimes occur in Canada, which laws apply, and understand your legal system. Educational platform powered by evidence.",
};

export default function PublicLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-slate-50">{children}</body>
    </html>
  );
}
