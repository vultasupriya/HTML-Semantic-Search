import React from "react";

export default function ResultCard({ item }) {
  return (
    <div className="result-card">
      <div className="meta-line">
        <strong>Source:</strong> {item.source || "N/A"} &nbsp; | &nbsp;
        <strong>Score:</strong> {item.score.toFixed(4)}
      </div>
      <div className="chunk-text">{item.text}</div>
    </div>
  );
}
