const API_BASE = "https://multiple-choice-qcf5.onrender.com";

let questions = [];
let currentIndex = 0;

/* ================= LOAD QUESTIONS ================= */
async function loadQuestions() {
  try {
    const res = await fetch(`${API_BASE}/api/random`);
    questions = await res.json();

    if (!questions || questions.length === 0) {
      alert("Không có câu hỏi trong database");
      return;
    }

    showQuestion();
  } catch (err) {
    console.error("Lỗi load câu hỏi:", err);
  }
}

/* ================= SHOW QUESTION ================= */
function showQuestion() {
  const q = questions[currentIndex];
  const quizDiv = document.getElementById("quiz");

  quizDiv.innerHTML = `
    <h3>Câu ${currentIndex + 1}/${questions.length}</h3>
    <p>${q.question}</p>

    <label><input type="radio" name="answer" value="A"> ${q.option1}</label><br>
    <label><input type="radio" name="answer" value="B"> ${q.option2}</label><br>
    <label><input type="radio" name="answer" value="C"> ${q.option3}</label><br>
    <label><input type="radio" name="answer" value="D"> ${q.option4}</label><br>

    <br>
    <button onclick="nextQuestion()">Câu tiếp theo</button>
  `;
}

/* ================= NEXT ================= */
function nextQuestion() {
  currentIndex++;
  if (currentIndex < questions.length) {
    showQuestion();
  } else {
    document.getElementById("quiz").innerHTML =
      "<h2>🎉 Hoàn thành bài thi!</h2>";
  }
}

/* ================= START ================= */
function startQuiz() {
  document.getElementById("start-btn").style.display = "none";
  loadQuestions();
}
