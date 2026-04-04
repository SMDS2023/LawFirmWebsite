#!/bin/bash
# Deploy Spanish Tutor to Cloudflare Pages

set -e

echo "=== Spanish Tutor Deployment ==="
echo ""

# Check if in correct directory
if [ ! -f "index.html" ]; then
  echo "Error: Must run from spanish-tutor directory"
  exit 1
fi

# Check for audio files
AUDIO_COUNT=$(ls -1 audio/*.mp3 2>/dev/null | wc -l)
if [ "$AUDIO_COUNT" -lt 10 ]; then
  echo "Warning: Only $AUDIO_COUNT audio files found"
  echo "Run 'python generate-audio.py' to generate pronunciation audio"
  read -p "Continue anyway? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Check for lesson files
LESSON_COUNT=$(ls -1 lessons/lesson-*.json 2>/dev/null | wc -l)
echo "Found $LESSON_COUNT lesson files"

if [ "$LESSON_COUNT" -lt 1 ]; then
  echo "Error: No lesson files found"
  exit 1
fi

# Deploy to Cloudflare Pages
echo ""
echo "Deploying to Cloudflare Pages (spanish-tutor project)..."
npx wrangler pages deploy . --project-name spanish-tutor

echo ""
echo "✓ Deployment complete!"
echo ""
echo "Access the app at: https://spanish-tutor.pages.dev"
echo "Admin dashboard: https://spanish-tutor.pages.dev/admin.html"
