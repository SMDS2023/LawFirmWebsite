// Timer with Pause Detection
// Tracks active practice time, pauses when tab inactive

class PracticeTimer {
  constructor(onUpdate, onThresholdMet) {
    this.seconds = 0;
    this.isRunning = false;
    this.interval = null;
    this.onUpdate = onUpdate;
    this.onThresholdMet = onThresholdMet;
    this.lastActivity = Date.now();
    this.inactiveThreshold = 30000; // 30 seconds

    // Setup visibility detection
    this.setupVisibilityDetection();
    this.setupActivityDetection();
  }

  setupVisibilityDetection() {
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.handleInactive();
      } else {
        this.handleActive();
      }
    });
  }

  setupActivityDetection() {
    // Track mouse/keyboard activity to detect engagement
    ['mousedown', 'keydown', 'scroll', 'touchstart'].forEach(event => {
      document.addEventListener(event, () => {
        this.lastActivity = Date.now();
      });
    });

    // Check for inactivity every 5 seconds
    setInterval(() => {
      if (this.isRunning && Date.now() - this.lastActivity > this.inactiveThreshold) {
        this.pause();
      }
    }, 5000);
  }

  start() {
    if (!this.isRunning) {
      this.isRunning = true;
      this.lastActivity = Date.now();
      this.interval = setInterval(() => {
        this.tick();
      }, 1000);
    }
  }

  pause() {
    if (this.isRunning) {
      this.isRunning = false;
      clearInterval(this.interval);
      this.saveState();
    }
  }

  stop() {
    this.pause();
    // Save final time to progress
    const minutes = Math.floor(this.seconds / 60);
    if (minutes > 0 && typeof progressManager !== 'undefined') {
      progressManager.addTime(minutes);
    }
  }

  tick() {
    this.seconds++;
    if (this.onUpdate) {
      this.onUpdate(this.seconds);
    }

    // Save state every 10 seconds
    if (this.seconds % 10 === 0) {
      this.saveState();
    }

    // Check threshold every minute
    if (this.seconds % 60 === 0) {
      const minutes = this.seconds / 60;
      if (this.onThresholdMet) {
        this.onThresholdMet(minutes);
      }
    }
  }

  handleInactive() {
    if (this.isRunning) {
      this.pause();
    }
  }

  handleActive() {
    // Auto-resume if user returns quickly (within 2 minutes)
    const timeSinceInactive = Date.now() - this.lastActivity;
    if (timeSinceInactive < 120000) {
      this.start();
    }
  }

  saveState() {
    sessionStorage.setItem('timer_state', JSON.stringify({
      seconds: this.seconds,
      timestamp: Date.now()
    }));
  }

  loadState() {
    const stored = sessionStorage.getItem('timer_state');
    if (stored) {
      const state = JSON.parse(stored);
      // Only restore if within last 5 minutes
      if (Date.now() - state.timestamp < 300000) {
        this.seconds = state.seconds;
        return true;
      }
    }
    return false;
  }

  reset() {
    this.pause();
    this.seconds = 0;
    sessionStorage.removeItem('timer_state');
    if (this.onUpdate) {
      this.onUpdate(0);
    }
  }

  getTime() {
    return this.seconds;
  }

  getFormattedTime() {
    const mins = Math.floor(this.seconds / 60);
    const secs = this.seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PracticeTimer;
}
