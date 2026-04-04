// Audio Player
// Handles playback of vocabulary and phrase audio

class AudioPlayer {
  constructor() {
    this.audio = new Audio();
    this.isPlaying = false;
    this.currentFile = null;

    this.audio.addEventListener('ended', () => {
      this.isPlaying = false;
      this.updatePlayButton(null);
    });

    this.audio.addEventListener('error', (e) => {
      console.error('Audio playback error:', e);
      this.isPlaying = false;
      this.updatePlayButton(null);
    });
  }

  play(audioFile, buttonElement) {
    // If same file and playing, pause it
    if (this.currentFile === audioFile && this.isPlaying) {
      this.pause();
      return;
    }

    // Stop current playback
    if (this.isPlaying) {
      this.audio.pause();
      this.audio.currentTime = 0;
    }

    // Play new file
    this.currentFile = audioFile;
    this.audio.src = audioFile;
    this.audio.play()
      .then(() => {
        this.isPlaying = true;
        this.updatePlayButton(buttonElement);
      })
      .catch(err => {
        console.error('Error playing audio:', err);
        this.showError('Audio playback failed. Please check your connection.');
      });
  }

  pause() {
    this.audio.pause();
    this.isPlaying = false;
    this.updatePlayButton(null);
  }

  updatePlayButton(activeButton) {
    // Reset all play buttons
    document.querySelectorAll('.play-btn').forEach(btn => {
      btn.textContent = '🔊';
      btn.classList.remove('playing');
    });

    // Mark active button
    if (activeButton && this.isPlaying) {
      activeButton.textContent = '⏸️';
      activeButton.classList.add('playing');
    }
  }

  showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'audio-error';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);

    setTimeout(() => {
      errorDiv.remove();
    }, 3000);
  }

  // Play a sequence of audio files (for dialogues)
  async playSequence(audioFiles, delay = 1000) {
    for (const file of audioFiles) {
      await this.playFile(file);
      await this.wait(delay);
    }
  }

  playFile(audioFile) {
    return new Promise((resolve, reject) => {
      this.audio.src = audioFile;
      this.audio.onended = resolve;
      this.audio.onerror = reject;
      this.audio.play().catch(reject);
    });
  }

  wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AudioPlayer;
}
