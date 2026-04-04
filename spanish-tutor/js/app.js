// Main Application Logic
// Coordinates lesson display, timer, progress, and unlock

let progressManager;
let practiceTimer;
let audioPlayer;
let unlockManager;
let currentLesson = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  progressManager = new ProgressManager();
  audioPlayer = new AudioPlayer();
  unlockManager = new UnlockManager();

  practiceTimer = new PracticeTimer(
    updateTimerDisplay,
    checkDailyGoal
  );

  // Try to restore timer state
  if (practiceTimer.loadState()) {
    updateTimerDisplay(practiceTimer.getTime());
  }

  // Load lesson from URL parameter or current lesson
  const urlParams = new URLSearchParams(window.location.search);
  const lessonId = parseInt(urlParams.get('lesson')) || progressManager.getProgress().currentLesson;

  loadLesson(lessonId);
  updateProgressBar();
  updateStreakDisplay();
});

// Load lesson JSON
async function loadLesson(lessonId) {
  try {
    const response = await fetch(`lessons/lesson-${lessonId.toString().padStart(2, '0')}.json`);
    if (!response.ok) {
      throw new Error('Lesson not found');
    }

    currentLesson = await response.json();
    renderLesson(currentLesson);
    practiceTimer.start();
  } catch (error) {
    console.error('Error loading lesson:', error);
    showError('Failed to load lesson. Please refresh the page.');
  }
}

// Render lesson content
function renderLesson(lesson) {
  document.getElementById('lesson-title').textContent = `Lesson ${lesson.id}: ${lesson.title}`;

  // Render vocabulary
  const vocabSection = document.getElementById('vocabulary-section');
  vocabSection.innerHTML = '<h2>Vocabulary</h2>';
  lesson.vocabulary.forEach(item => {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'vocab-item';
    itemDiv.innerHTML = `
      <div class="vocab-word">
        <span class="spanish">${item.spanish}</span>
        <button class="play-btn" onclick="playAudio('${item.audio}', this)">🔊</button>
      </div>
      <div class="vocab-translation">${item.english}</div>
    `;
    vocabSection.appendChild(itemDiv);
  });

  // Render phrases
  const phrasesSection = document.getElementById('phrases-section');
  phrasesSection.innerHTML = '<h2>Example Phrases</h2>';
  lesson.phrases.forEach(phrase => {
    const phraseDiv = document.createElement('div');
    phraseDiv.className = 'phrase-item';
    phraseDiv.innerHTML = `
      <div class="phrase-spanish">
        <span>${phrase.spanish}</span>
        <button class="play-btn" onclick="playAudio('${phrase.audio}', this)">🔊</button>
      </div>
      <div class="phrase-translation">${phrase.english}</div>
    `;
    phrasesSection.appendChild(phraseDiv);
  });

  // Render dialogue
  const dialogueSection = document.getElementById('dialogue-section');
  dialogueSection.innerHTML = `<h2>Dialogue: ${lesson.dialogue.context}</h2>`;
  const dialogueDiv = document.createElement('div');
  dialogueDiv.className = 'dialogue';
  lesson.dialogue.lines.forEach(line => {
    const lineDiv = document.createElement('div');
    lineDiv.className = `dialogue-line speaker-${line.speaker.toLowerCase()}`;
    lineDiv.innerHTML = `
      <div class="speaker">Speaker ${line.speaker}:</div>
      <div class="line-content">
        <div class="line-spanish">${line.spanish}</div>
        <div class="line-english">${line.english}</div>
      </div>
    `;
    dialogueDiv.appendChild(lineDiv);
  });
  dialogueSection.appendChild(dialogueDiv);

  // Render quiz
  renderQuiz(lesson.quiz);

  // Update lesson navigation
  updateLessonNavigation(lesson.id);
}

// Render quiz section
function renderQuiz(quiz) {
  const quizSection = document.getElementById('quiz-section');
  quizSection.innerHTML = '<h2>Quick Quiz</h2>';

  quiz.forEach((question, index) => {
    const questionDiv = document.createElement('div');
    questionDiv.className = 'quiz-question';
    questionDiv.innerHTML = `
      <p class="question-text">${index + 1}. ${question.question}</p>
      <div class="quiz-options">
        ${question.options.map((option, optIndex) => `
          <button class="quiz-option" onclick="checkAnswer(${index}, ${optIndex}, ${question.correct})">
            ${option}
          </button>
        `).join('')}
      </div>
      <div class="quiz-feedback" id="feedback-${index}"></div>
    `;
    quizSection.appendChild(questionDiv);
  });
}

// Check quiz answer
function checkAnswer(questionIndex, selectedIndex, correctIndex) {
  const feedback = document.getElementById(`feedback-${questionIndex}`);
  const buttons = document.querySelectorAll(`#quiz-section .quiz-question:nth-child(${questionIndex + 2}) .quiz-option`);

  if (selectedIndex === correctIndex) {
    feedback.textContent = '✓ Correct!';
    feedback.className = 'quiz-feedback correct';
    buttons[selectedIndex].classList.add('correct');
  } else {
    feedback.textContent = '✗ Try again';
    feedback.className = 'quiz-feedback incorrect';
    buttons[selectedIndex].classList.add('incorrect');
  }

  // Disable all buttons after answer
  buttons.forEach(btn => btn.disabled = true);
}

// Complete lesson
function completeLesson() {
  if (!currentLesson) return;

  // Stop timer and save progress
  practiceTimer.stop();
  progressManager.completeLesson(currentLesson.id);

  // Show completion message
  showCompletionModal();
}

function showCompletionModal() {
  const progress = progressManager.getProgress();
  const modal = document.createElement('div');
  modal.className = 'completion-modal';

  let content = `
    <div class="modal-content">
      <h2>¡Bien hecho!</h2>
      <p>You've completed Lesson ${currentLesson.id}!</p>
      <div class="completion-stats">
        <p>Time practiced today: ${progress.dailyMinutes} minutes</p>
        <p>Current streak: ${progress.streak} days</p>
  `;

  if (progress.unlockCode) {
    content += `
        <div class="unlock-achieved">
          <p><strong>🎉 Phone Unlocked!</strong></p>
          <div class="code-display">${progress.unlockCode}</div>
        </div>
    `;
  } else {
    const remaining = progress.dailyGoal - progress.dailyMinutes;
    content += `
        <p>${remaining} more minutes until unlock</p>
    `;
  }

  content += `
      </div>
      <div class="modal-actions">
        <button onclick="loadLesson(${currentLesson.id + 1})">Next Lesson</button>
        <button onclick="location.href='index.html'">Back to Menu</button>
      </div>
    </div>
  `;

  modal.innerHTML = content;
  document.body.appendChild(modal);
}

// Audio playback
function playAudio(audioFile, buttonElement) {
  audioPlayer.play(audioFile, buttonElement);
}

// Timer display
function updateTimerDisplay(seconds) {
  const display = document.getElementById('timer-display');
  if (display) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    display.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
  }
}

// Check daily goal
function checkDailyGoal(minutes) {
  const progress = progressManager.getProgress();
  if (minutes >= progress.dailyGoal && !progress.unlockCode) {
    progressManager.addTime(0); // Trigger unlock code generation
    unlockManager.showUnlockNotification(progress.unlockCode);
  }
  updateProgressBar();
}

// Update progress bar
function updateProgressBar() {
  const progress = progressManager.getProgress();
  unlockManager.updateProgressDisplay(progress.dailyMinutes, progress.dailyGoal);
}

// Update streak display
function updateStreakDisplay() {
  const progress = progressManager.getProgress();
  const streakElement = document.getElementById('streak-display');
  if (streakElement) {
    streakElement.textContent = `🔥 ${progress.streak} day streak`;
  }
}

// Update lesson navigation
function updateLessonNavigation(currentId) {
  const prevBtn = document.getElementById('prev-lesson');
  const nextBtn = document.getElementById('next-lesson');

  if (prevBtn) {
    prevBtn.disabled = currentId <= 1;
    prevBtn.onclick = () => loadLesson(currentId - 1);
  }

  if (nextBtn) {
    nextBtn.onclick = () => completeLesson();
  }
}

// Error display
function showError(message) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.textContent = message;
  document.body.appendChild(errorDiv);

  setTimeout(() => {
    errorDiv.remove();
  }, 5000);
}

// Before page unload, save timer state
window.addEventListener('beforeunload', () => {
  if (practiceTimer && practiceTimer.isRunning) {
    practiceTimer.saveState();
  }
});
