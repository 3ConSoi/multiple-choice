import React, { useEffect, useState } from "react";

export default function Timer({ seconds, onExpire }) {
  const [remaining, setRemaining] = useState(seconds);

  useEffect(() => {
    setRemaining(seconds);
  }, [seconds]);

  useEffect(() => {
    if (remaining <= 0) {
      onExpire();
      return;
    }
    const t = setTimeout(() => setRemaining(r => r - 1)000);
    return () => clearTimeout(t);
  }, [remaining, onExpire]);

  const mm = String(Math.floor(remaining / 60)).padStart(2, "0");
  const ss = String(remaining % 60).padStart(2, "0");
  return <div className="timer">Time left: {mm}:{ss}</div>;
}