interface ConfidenceBadgeProps {
  score: number; // 0–1
  showLabel?: boolean;
}

export default function ConfidenceBadge({ score, showLabel = true }: ConfidenceBadgeProps) {
  const pct = Math.round(score * 100);

  let color = "var(--pub-teal)";
  let bgColor = "#ECFDF5";
  let label = "High";

  if (pct < 50) {
    color = "var(--pub-danger)";
    bgColor = "var(--pub-danger-bg)";
    label = "Low";
  } else if (pct < 75) {
    color = "var(--pub-warn)";
    bgColor = "var(--pub-warn-bg)";
    label = "Medium";
  }

  return (
    <span
      className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium"
      style={{ color, background: bgColor }}
      title={`Confidence score: ${pct}%`}
      aria-label={`${label} confidence — ${pct}%`}
    >
      {/* Mini bar */}
      <span
        className="inline-block rounded-full"
        style={{
          width: "28px",
          height: "4px",
          background: "currentColor",
          opacity: 0.25,
          position: "relative",
        }}
        aria-hidden="true"
      >
        <span
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            height: "100%",
            width: `${pct}%`,
            background: color,
            opacity: 1,
            borderRadius: "inherit",
          }}
        />
      </span>
      {showLabel && `${pct}%`}
    </span>
  );
}
