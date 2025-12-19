const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

export async function startExam(examId, { num_questions, randomize } = {}) {
  const params = new URLSearchParams();
  if (num_questions) params.set("num_questions", num_questions);
  if (randomize !== undefined) params.set("randomize", randomize);
  const res = await fetch(`${API_BASE}/exams/${examId}/start?${params.toString()}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" }
  });
  return res.json();
}

export async function submitAttempt(attemptId, answers) {
  const res = await fetch(`${API_BASE}/attempts/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ attempt_id: attemptId, answers })
  });
  return res.json();
}

function startQuiz() {
    document.getElementById("start-btn").style.display = "none";
    loadQuestions();
    startTimer();
}


function loadQuiz() {
    fetch("http://127.0.0.1:8000/quiz/all")
        .then(res => res.json())
        .then(data => {
            let html = "<h2>Danh sách câu hỏi</h2>";
            data.forEach(q => {
                html += `
                    <div style="margin-bottom:10px; border-bottom:1px solid #ccc;">
                        <b>ID:</b> ${q.id}<br>
                        <b>Câu hỏi:</b> ${q.question}<br>
                        <b>A:</b> ${q.option1}<br>
                        <b>B:</b> ${q.option2}<br>
                        <b>C:</b> ${q.option3}<br>
                        <b>D:</b> ${q.option4}<br>
                        <b>Đáp án:</b> ${q.answer}
                    </div>
                `;
            });

            document.getElementById("quiz-list").innerHTML = html;
        });
}

function submitQuiz() {
    let score = 0;

    answers.forEach((ans, idx) => {
        if (ans === questions[idx].answer_key[0]) score++;
    });

    alert("Bạn được: " + score + "/20");
}

function nextQuestion() {
    if (currentIndex < questions.length - 1) {
        currentIndex++;
        showQuestion();
    }
}
