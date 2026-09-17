const questions = window.SPEEDDATE_QUESTIONS;

const setupScreen = document.querySelector("#setup-screen");
const gameScreen = document.querySelector("#game-screen");
const setupForm = document.querySelector("#setup-form");
const minutesInput = document.querySelector("#minutes");
const secondsInput = document.querySelector("#seconds");
const formError = document.querySelector("#form-error");
const questionElement = document.querySelector("#question");
const roundLabel = document.querySelector("#round-label");
const progressLabel = document.querySelector("#progress-label");
const timerArea = document.querySelector("#timer-area");
const timerElement = document.querySelector("#timer");
const timerStatus = document.querySelector("#timer-status");
const nextButton = document.querySelector("#next-button");
const settingsButton = document.querySelector("#settings-button");
const fullscreenButton = document.querySelector("#fullscreen-button");

let durationSeconds = 70;
let questionQueue = [];
let round = 0;
let questionNumber = 0;
let deadline = 0;
let timerInterval = null;
let audioContext = null;
let lastQuestion = null;

function shuffled(items) {
  const result = [...items];
  for (let index = result.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));
    [result[index], result[randomIndex]] = [result[randomIndex], result[index]];
  }
  return result;
}

function refillQuestionQueue() {
  questionQueue = shuffled(questions);

  // Avoid the same question directly after moving to a new round.
  if (questionQueue.length > 1 && questionQueue[0] === lastQuestion) {
    [questionQueue[0], questionQueue[1]] = [questionQueue[1], questionQueue[0]];
  }

  round += 1;
  questionNumber = 0;
}

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function showTime(secondsRemaining) {
  timerElement.textContent = formatTime(secondsRemaining);
  timerArea.classList.toggle("almost-done", secondsRemaining <= 10 && secondsRemaining > 0);
  document.title = `${formatTime(secondsRemaining)} · Speeddate`;
}

function stopTimer() {
  window.clearInterval(timerInterval);
  timerInterval = null;
}

function beep() {
  if (!audioContext) return;

  const start = audioContext.currentTime;
  [0, 0.28].forEach((delay) => {
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();
    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime(880, start + delay);
    gain.gain.setValueAtTime(0.0001, start + delay);
    gain.gain.exponentialRampToValueAtTime(0.35, start + delay + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, start + delay + 0.2);
    oscillator.connect(gain).connect(audioContext.destination);
    oscillator.start(start + delay);
    oscillator.stop(start + delay + 0.21);
  });
}

function finishTimer() {
  stopTimer();
  showTime(0);
  timerArea.classList.remove("almost-done");
  timerArea.classList.add("finished");
  timerStatus.textContent = "Time to switch!";
  beep();
}

function updateTimer() {
  const remaining = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
  showTime(remaining);
  if (remaining === 0) finishTimer();
}

function startTimer() {
  stopTimer();
  timerArea.classList.remove("finished", "almost-done");
  timerStatus.textContent = "Time is running";
  deadline = Date.now() + durationSeconds * 1000;
  showTime(durationSeconds);
  timerInterval = window.setInterval(updateTimer, 200);
}

function showNextQuestion() {
  if (questionQueue.length === 0) refillQuestionQueue();

  lastQuestion = questionQueue.shift();
  questionNumber += 1;
  questionElement.textContent = lastQuestion;
  roundLabel.textContent = `Round ${round}`;
  progressLabel.textContent = `Question ${questionNumber} of ${questions.length}`;
  startTimer();
}

function enableAudio() {
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  if (!AudioContext) return;
  if (!audioContext) audioContext = new AudioContext();
  if (audioContext.state === "suspended") audioContext.resume();
}

function startGame(event) {
  event.preventDefault();
  const minutes = Number.parseInt(minutesInput.value, 10) || 0;
  const seconds = Number.parseInt(secondsInput.value, 10) || 0;
  const totalSeconds = minutes * 60 + seconds;

  if (totalSeconds < 1) {
    formError.textContent = "Set a time of at least one second.";
    return;
  }

  formError.textContent = "";
  durationSeconds = totalSeconds;
  questionQueue = [];
  round = 0;
  questionNumber = 0;
  lastQuestion = null;
  enableAudio();
  setupScreen.classList.add("hidden");
  gameScreen.classList.remove("hidden");
  showNextQuestion();
}

setupForm.addEventListener("submit", startGame);

nextButton.addEventListener("click", () => {
  enableAudio();
  showNextQuestion();
});

settingsButton.addEventListener("click", () => {
  stopTimer();
  document.title = "Speeddate";
  gameScreen.classList.add("hidden");
  setupScreen.classList.remove("hidden");
});

fullscreenButton.addEventListener("click", async () => {
  if (document.fullscreenElement) {
    await document.exitFullscreen();
  } else {
    await document.documentElement.requestFullscreen();
  }
});

document.addEventListener("keydown", (event) => {
  if (gameScreen.classList.contains("hidden") || event.repeat) return;
  if (event.code === "Space" || event.code === "ArrowRight") {
    event.preventDefault();
    enableAudio();
    showNextQuestion();
  }
});
