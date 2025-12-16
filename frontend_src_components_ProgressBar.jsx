import React from "react";

export default function ProgressBar({ current, total }) {
  const pct = total ? Math.round((current / total) * 100) : 0;
  return (
    <div className="progress">
      <div className="progress-inner" style={{ width: `${pct}%`, background: "#4caf50", height: "8px" }} />
      <div className="progress-text">{current}/{total} ({pct}%)</div>
    </div>
  );
}