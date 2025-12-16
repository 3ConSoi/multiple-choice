import React, { useState } from "react";
import Timer from "./Timer";
import ProgressBar from "./ProgressBar";
import { submitAttempt } from "../api";

export default function Quiz({ attempt }) {
  const [answers, setAnswers] = useState({});
  const [finished, setFinished] = useState(false);
  const [result, setResult] = useState(null);

  const handleChoose = (qid, choiceId) => {
    setAnswers(prev => ({ ...prev, [qid]: [choiceId] })); // single choice; extend for multi
  };

  const onExpire = () => {
    handleSubmit();
  };

  const handleSubmit = async () => {
    if (finished) return;
    const res = await submitAttempt(attempt.attempt_id, answers);
    setResult(res);
    setFinished(true);
  };

  return (
    <div>
      <Timer seconds={attempt.duration_sec} onExpire={onExpire} />
      <ProgressBar current={Object.keys(answers).length} total={attempt.questions.length} />
      {attempt.questions.map(q => (
        <div key={q.id} className="question">
          <h4>{q.text}</h4>
          {q.choices.map(c => (
            <div key={c.id}>
              <label>
                <input type="radio" name={`q-${q.id}`} onChange={() => handleChoose(q.id, c.id)} />
                {c.label}
              </label>
            </div>
          ))}
        </div>
      ))}
      <button onClick={handleSubmit} disabled={finished}>Submit</button>

      {result && (
        <div className="result">
          <h3>Score: {result.score}%</h3>
          <div>Passed: {result.passed ? "Yes" : "No"}</div>
        </div>
      )}
    </div>
  );
}