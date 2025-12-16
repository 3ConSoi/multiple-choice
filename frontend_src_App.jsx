import React, { useState } from "react";
import Quiz from "./components/Quiz";
import { startExam } from "./api";

export default function App() {
  const [attempt, setAttempt] = useState(null);

  const begin = async () => {
    // for demo, exam id 1
    const res = await startExam(1, { num_questions: 10, randomize: true });
    setAttempt(res);
  };

  return (
    <div>
      <h1>Multiple-choice Quiz</h1>
      {!attempt ? <button onClick={begin}>Start Exam</button> : <Quiz attempt={attempt} />}
    </div>
  );
}