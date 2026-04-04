# Spanish Learning Program - Pickleball Theme

## Overview

A Spanish learning web app designed for high school students (ages 14-17) with a pickleball theme. The program uses daily practice requirements (15-30 minutes) as a phone unlock incentive.

## Features

### Phase 1: MVP (Current)
- **10 Core Lessons**: Progression from pickleball scoring to general conversation
- **Audio Playback**: Google Cloud TTS pronunciation for all vocabulary
- **Time Tracking**: Monitors practice time with pause detection
- **Unlock System**: Generates daily code when time threshold met
- **Progress Persistence**: LocalStorage tracks lessons completed, streak, total time
- **Parent Dashboard**: Admin view for monitoring progress and overrides

### Phase 2: Enhanced Progress (Future)
- Streak calendar visualization
- Badges and achievements
- Optional cloud sync (Firebase/D1)

### Phase 3: Voice Tutor (Future)
- ElevenLabs or Gemini Live integration
- "Coach Miguel" conversational AI
- Context-aware practice based on completed lessons

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript (mobile-first)
- **Hosting**: Cloudflare Pages
- **Audio**: Google Cloud Text-to-Speech API
- **Storage**: LocalStorage (Phase 1), optional cloud backend (Phase 2+)

## File Structure

```
spanish-tutor/
├── index.html              # Main lesson interface
├── admin.html              # Parent dashboard
├── lessons/                # Lesson JSON files
│   ├── lesson-01.json
│   └── ...
├── audio/                  # Pre-generated TTS audio
├── css/
│   └── style.css          # Responsive styling
├── js/
│   ├── app.js             # Core application logic
│   ├── timer.js           # Time tracking with pause detection
│   ├── progress.js        # Progress management
│   ├── unlock.js          # Unlock code generation
│   └── audio-player.js    # Audio playback controller
└── README.md
```

## Curriculum

**Pickleball Foundation (Lessons 1-7)**
1. Numbers 0-15 (scoring)
2. Basic court phrases
3. Game vocabulary
4. Action verbs
5. Game questions
6. Strategy/positioning
7. Pre/post-game conversation

**Expansion Beyond Court (Lessons 8-10)**
8. Talking about pickleball
9. General sports vocabulary
10. Daily conversation

Each lesson: ~10-15 minutes, includes vocabulary, example sentences, dialogue, and quiz.

## Setup

### Deploy to Cloudflare Pages

```bash
cd LotterLaw/spanish-tutor
npx wrangler pages deploy . --project-name spanish-tutor
```

### Generate Audio Files

Uses Google Cloud Text-to-Speech API (requires setup in separate script).

## Usage

### For Students
1. Open `index.html`
2. Complete lessons in sequence
3. Practice 15-30 minutes daily
4. Get unlock code when threshold met

### For Parents
1. Open `admin.html`
2. View progress, streak, total time
3. Adjust daily time requirement
4. Use override code if needed

## Development

### Testing Checklist
- [ ] Timer persists across browser refresh
- [ ] LocalStorage handles quota limits
- [ ] Audio works on mobile devices
- [ ] Unlock code generates at threshold
- [ ] Admin override doesn't disrupt student progress
- [ ] Tab inactive detection prevents gaming

### Lesson Quality
- [ ] Native speaker review (lessons 1-3 minimum)
- [ ] Audio pronunciation clear and natural
- [ ] Quiz questions test comprehension
- [ ] Dialogues age-appropriate and natural

## Success Metrics

- **Week 1**: MVP deployed, lesson 1 completed
- **Week 2**: 5+ consecutive days, lessons 1-5 done
- **Week 3**: Consistent 15-30 min daily, visible retention
- **Month 1**: All 10 lessons completed
- **Month 2**: Voice tutor added (Phase 3)

## Notes

- Start with 10 excellent lessons, expand later if needed
- Pickleball theme provides context but transitions to general conversation
- Native speaker review critical for foundational content
- Don't rush to voice tutor—validate MVP engagement first
