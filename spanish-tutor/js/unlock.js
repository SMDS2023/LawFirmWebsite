// Unlock Code Generator
// Generates daily unlock codes based on time threshold

class UnlockManager {
  constructor() {
    this.storageKey = 'unlock_settings';
    this.load();
  }

  load() {
    const stored = localStorage.getItem(this.storageKey);
    if (stored) {
      this.settings = JSON.parse(stored);
    } else {
      this.settings = {
        dailyGoalMinutes: 15,
        adminOverrideEnabled: false
      };
      this.save();
    }
  }

  save() {
    localStorage.setItem(this.storageKey, JSON.stringify(this.settings));
  }

  setDailyGoal(minutes) {
    this.settings.dailyGoalMinutes = minutes;
    this.save();
  }

  getDailyGoal() {
    return this.settings.dailyGoalMinutes;
  }

  // Verify unlock code (used in admin dashboard)
  verifyCode(enteredCode, actualCode) {
    return enteredCode === actualCode;
  }

  // Generate admin override code (static, for parent use)
  getAdminOverrideCode() {
    // Static override code - parent should set this in admin.html
    return this.settings.adminOverrideCode || '9999';
  }

  setAdminOverrideCode(code) {
    this.settings.adminOverrideCode = code;
    this.save();
  }

  // Display unlock notification
  showUnlockNotification(code) {
    const notification = document.createElement('div');
    notification.className = 'unlock-notification';
    notification.innerHTML = `
      <div class="unlock-content">
        <h2>¡Excelente! 🎉</h2>
        <p>You've completed your daily practice!</p>
        <div class="unlock-code">
          <label>Phone Unlock Code:</label>
          <div class="code-display">${code}</div>
        </div>
        <p class="code-note">This code is valid until midnight</p>
        <button onclick="this.parentElement.parentElement.remove()">Got it!</button>
      </div>
    `;
    document.body.appendChild(notification);
  }

  // Check if daily goal met
  checkGoalMet(dailyMinutes) {
    return dailyMinutes >= this.settings.dailyGoalMinutes;
  }

  // Update progress display
  updateProgressDisplay(dailyMinutes, goalMinutes) {
    const percentage = Math.min((dailyMinutes / goalMinutes) * 100, 100);
    const progressBar = document.querySelector('.progress-bar-fill');
    const progressText = document.querySelector('.progress-text');

    if (progressBar) {
      progressBar.style.width = `${percentage}%`;
    }

    if (progressText) {
      const remaining = Math.max(goalMinutes - dailyMinutes, 0);
      if (remaining > 0) {
        progressText.textContent = `${remaining} minutes until unlock`;
      } else {
        progressText.textContent = `Goal reached! ✓`;
        progressText.classList.add('goal-met');
      }
    }
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = UnlockManager;
}
