// Progress Management
// Tracks learning progress, streaks, and unlock status

class ProgressManager {
  constructor() {
    this.storageKey = 'spanish_tutor_progress';
    this.load();
  }

  load() {
    const stored = localStorage.getItem(this.storageKey);
    if (stored) {
      this.data = JSON.parse(stored);
      this.checkDateRollover();
    } else {
      this.reset();
    }
  }

  reset() {
    this.data = {
      dailyMinutes: 0,
      lastPractice: this.getTodayDate(),
      streak: 0,
      completedLessons: [],
      currentLesson: 1,
      totalMinutes: 0,
      unlockCode: null,
      dailyGoal: 15, // Default 15 minutes
      lastUnlockDate: null
    };
    this.save();
  }

  save() {
    localStorage.setItem(this.storageKey, JSON.stringify(this.data));
  }

  getTodayDate() {
    return new Date().toISOString().split('T')[0];
  }

  checkDateRollover() {
    const today = this.getTodayDate();
    if (this.data.lastPractice !== today) {
      // Check if streak should continue (practiced yesterday)
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = yesterday.toISOString().split('T')[0];

      if (this.data.lastPractice === yesterdayStr) {
        // Streak continues
        this.data.streak++;
      } else if (this.data.dailyMinutes >= this.data.dailyGoal) {
        // They met goal on last practice, but missed days - reset streak
        this.data.streak = 1;
      } else {
        // Didn't meet goal, streak broken
        this.data.streak = 0;
      }

      // Reset daily counters
      this.data.dailyMinutes = 0;
      this.data.unlockCode = null;
      this.data.lastPractice = today;
      this.save();
    }
  }

  addTime(minutes) {
    this.checkDateRollover();
    this.data.dailyMinutes += minutes;
    this.data.totalMinutes += minutes;

    // Check if unlock threshold met
    if (this.data.dailyMinutes >= this.data.dailyGoal && !this.data.unlockCode) {
      this.generateUnlockCode();
    }

    this.save();
  }

  generateUnlockCode() {
    // Generate 4-digit code based on date (changes daily)
    const today = this.getTodayDate();
    const seed = today.split('-').join('');
    let hash = 0;
    for (let i = 0; i < seed.length; i++) {
      hash = ((hash << 5) - hash) + seed.charCodeAt(i);
      hash = hash & hash;
    }
    this.data.unlockCode = Math.abs(hash % 10000).toString().padStart(4, '0');
    this.data.lastUnlockDate = today;
    this.save();
  }

  completeLesson(lessonId) {
    if (!this.data.completedLessons.includes(lessonId)) {
      this.data.completedLessons.push(lessonId);
      if (lessonId === this.data.currentLesson) {
        this.data.currentLesson++;
      }
      this.save();
    }
  }

  isLessonCompleted(lessonId) {
    return this.data.completedLessons.includes(lessonId);
  }

  getProgress() {
    return this.data;
  }

  setDailyGoal(minutes) {
    this.data.dailyGoal = minutes;
    this.save();
  }

  // Admin override - generates today's code without time requirement
  adminUnlock() {
    const today = this.getTodayDate();
    if (this.data.lastUnlockDate !== today) {
      this.generateUnlockCode();
    }
    return this.data.unlockCode;
  }

  getTotalVocabulary() {
    // Each lesson averages 10 vocabulary items
    return this.data.completedLessons.length * 10;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ProgressManager;
}
