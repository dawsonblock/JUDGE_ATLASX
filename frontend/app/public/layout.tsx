import type { Metadata, Viewport } from "next";
import "../globals.css";
import PublicNav from "@/components/public/PublicNav";
import PublicFooter from "@/components/public/PublicFooter";

export const metadata: Metadata = {
  title: {
    default: "JUDGE AtlasX — Crime & Law in Canada",
    template: "%s | JUDGE AtlasX",
  },
  description:
    "Explore where crimes occur in Canada, which laws apply, and understand your legal system. Evidence-backed civic education platform.",
  keywords: ["Canadian law", "crime statistics", "Criminal Code", "civic education", "transparency"],
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  themeColor: "#0F4C75",
};

export default function PublicLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning className="public-theme">
      <body
        className="min-h-screen flex flex-col"
        style={{
          background: "var(--pub-bg)",
          color: "var(--pub-text)",
          fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif",
        }}
      >
        <PublicNav />
        <main className="flex-1 flex flex-col">{children}</main>
        <PublicFooter />
      </body>
    </html>
  );
}
