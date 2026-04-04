# Quick Start Guide

## ✅ What's Done

The MVP is **code-complete** and ready for content creation and testing:

- ✅ Full web application (HTML/CSS/JavaScript)
- ✅ Timer with pause detection
- ✅ Progress tracking and unlock system
- ✅ Parent admin dashboard
- ✅ Audio playback system
- ✅ Lesson 1 & 2 content (2 of 10)
- ✅ Full curriculum design (10 lessons)
- ✅ Audio generation script
- ✅ Deployment script

## 🎯 Next Steps (In Order)

### 1. Test Locally (5 minutes)

Open in browser to verify app works:
```bash
cd LotterLaw/spanish-tutor
# Open index.html in browser (double-click or use local server)
```

**What to test**:
- Timer starts and counts
- Lesson 1 loads and displays correctly
- Vocabulary and phrases show up
- Quiz questions work
- Progress bar updates
- Admin dashboard shows stats

**Known**: Audio won't play yet (files don't exist), but buttons should appear.

---

### 2. Create Remaining Lessons (2-3 hours)

Use `lessons/lesson-01.json` and `lessons/lesson-02.json` as templates.

**Copy template**:
```bash
cp lessons/lesson-02.json lessons/lesson-03.json
```

**Edit for Lesson 3** (Game Vocabulary):
- Update `id: 3`
- Update `title: "Game Vocabulary"`
- Replace vocabulary (see CURRICULUM.md for word lists)
- Update phrases and dialogue
- Create 5 quiz questions
- Update audio file paths (`03-` prefix)

**Repeat for Lessons 4-10**. Reference `CURRICULUM.md` for content outlines.

---

### 3. Generate Audio Files (30 minutes)

#### Option A: Google Cloud TTS (Recommended)

**Setup** (one-time):
1. Create Google Cloud project
2. Enable Text-to-Speech API
3. Create service account and download JSON key
4. Install Python package: `pip install google-cloud-texttospeech`
5. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
   ```

**Generate audio**:
```bash
cd LotterLaw/spanish-tutor
python generate-audio.py
```

This creates ~20 MP3 files per lesson in `audio/` directory.

**Cost**: ~$0.30 for all 10 lessons (Google charges per character)

#### Option B: Placeholder Testing

Create dummy audio files to test functionality:
```bash
# Create silent MP3s (requires ffmpeg)
for i in {1..50}; do
  ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 1 -q:a 9 -acodec libmp3lame audio/test-$i.mp3
done
```

Replace with real audio later.

---

### 4. Native Speaker Review (1 hour)

**Critical for Lessons 1-3** before son uses them.

**What to check**:
- Spanish spelling and accents
- Grammar correctness
- Natural phrasing (not word-for-word translation)
- Age-appropriate vocabulary
- Audio pronunciation (if generated)

**How to get review**:
- Ask Spanish teacher at son's school
- Hire on Fiverr ($10-20 for quick review)
- Ask Spanish-speaking colleague/friend

---

### 5. Deploy to Cloudflare Pages (5 minutes)

**Prerequisites**:
- Cloudflare account
- Wrangler CLI: `npm install -g wrangler`
- Login: `wrangler login`

**Deploy**:
```bash
cd LotterLaw/spanish-tutor
./deploy.sh
```

Or manually:
```bash
npx wrangler pages deploy . --project-name spanish-tutor
```

**Result**: App live at `https://spanish-tutor.pages.dev`

---

### 6. Test with Son (Day 1)

**Goal**: Validate engagement and difficulty level

**Test plan**:
1. Have him open app on phone: `https://spanish-tutor.pages.dev`
2. Watch him complete Lesson 1 (don't help unless stuck)
3. Note time to complete (~10-15 min target)
4. Ask feedback:
   - Was it too easy/hard/just right?
   - Was the pickleball theme helpful?
   - Did timer/progress feel motivating?
   - Would he want to do Lesson 2 tomorrow?

**Adjust based on feedback** before creating all 10 lessons.

---

### 7. Iterate (Week 1)

**Monitor**:
- Daily completion consistency
- Time per lesson (adjust length if needed)
- Vocabulary retention (spot check)
- Engagement level (is phone unlock motivating?)

**Adjust**:
- Lesson length (add/remove content)
- Daily goal (15-30 min range)
- Difficulty progression
- Quiz questions (if too easy/hard)

---

## 📁 File Structure

```
spanish-tutor/
├── index.html              # Main lesson interface
├── admin.html              # Parent dashboard
├── lessons/                # Lesson content (JSON)
│   ├── lesson-01.json     # ✅ Numbers (DONE)
│   ├── lesson-02.json     # ✅ Basic phrases (DONE)
│   └── lesson-03.json     # ⬜ To create (8 more)
├── audio/                  # MP3 pronunciation files
│   └── (generate 150-200 files)
├── css/style.css           # ✅ Complete
├── js/                     # ✅ All modules complete
│   ├── app.js
│   ├── progress.js
│   ├── timer.js
│   ├── unlock.js
│   └── audio-player.js
├── README.md               # Project documentation
├── CURRICULUM.md           # Full lesson plan
├── IMPLEMENTATION_STATUS.md # Status tracking
├── generate-audio.py       # Audio generation script
└── deploy.sh               # Deployment script
```

---

## 🎯 Success Metrics (Week 1)

- [ ] Son completes Lesson 1
- [ ] Son completes Lesson 2 next day (validates engagement)
- [ ] 3+ consecutive days of practice
- [ ] Can announce scores in Spanish during actual pickleball
- [ ] Requests to continue to next lessons

**If achieved**: Complete Lessons 3-10, proceed to Phase 2/3
**If not**: Adjust difficulty/incentives before investing more time

---

## 🐛 Troubleshooting

**Audio not playing**:
- Check browser console for errors
- Verify audio files exist in `audio/` directory
- Test with simple audio file first
- Try different browser (Safari on iOS is critical)

**Timer not working**:
- Check browser LocalStorage is enabled
- Check console for JavaScript errors
- Test timer pause detection by switching tabs

**Progress not saving**:
- Verify LocalStorage not disabled
- Check browser privacy settings
- Try incognito/private mode to test

**Unlock code not generating**:
- Verify daily goal set correctly
- Check progress in admin dashboard
- Ensure enough time accumulated

---

## 📞 Support

**Questions about**:
- Content structure: See `CURRICULUM.md`
- Technical issues: Check `IMPLEMENTATION_STATUS.md`
- Deployment: See `README.md`
- Audio generation: See `audio/README.md`

---

**Current Status (2026-03-27)**: Ready for content creation and testing. Core app functional, needs lessons 3-10 and audio generation.
