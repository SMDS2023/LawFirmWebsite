"""
Audio Generation Script for Spanish Tutor
Uses Google Cloud Text-to-Speech API to generate pronunciation audio files
"""

import os
import json
from google.cloud import texttospeech

# Initialize client (requires GOOGLE_APPLICATION_CREDENTIALS env var)
client = texttospeech.TextToSpeechClient()

# Voice configuration - Spanish (Spain) female voice
VOICE_CONFIG = texttospeech.VoiceSelectionParams(
    language_code="es-ES",
    name="es-ES-Neural2-A",  # Female neural voice
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

# Audio configuration
AUDIO_CONFIG = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=0.85,  # Slightly slower for learning
    pitch=0.0
)

def generate_audio(text, output_filename):
    """Generate audio file from text"""
    synthesis_input = texttospeech.SynthesisInput(text=text)

    try:
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=VOICE_CONFIG,
            audio_config=AUDIO_CONFIG,
            timeout=600
        )

        # Save audio file
        output_path = os.path.join("audio", output_filename)
        with open(output_path, "wb") as out:
            out.write(response.audio_content)

        print(f"✓ Generated: {output_filename}")
        return True

    except Exception as e:
        print(f"✗ Error generating {output_filename}: {e}")
        return False

def process_lesson(lesson_file):
    """Process all audio for a lesson JSON file"""
    with open(lesson_file, 'r', encoding='utf-8') as f:
        lesson = json.load(f)

    lesson_id = lesson['id']
    print(f"\n=== Processing Lesson {lesson_id}: {lesson['title']} ===")

    # Generate vocabulary audio
    print("\nVocabulary:")
    for item in lesson['vocabulary']:
        audio_file = item['audio'].split('/')[-1]
        generate_audio(item['spanish'], audio_file)

    # Generate phrase audio
    print("\nPhrases:")
    for item in lesson['phrases']:
        audio_file = item['audio'].split('/')[-1]
        generate_audio(item['spanish'], audio_file)

    # Optional: Generate dialogue audio (full lines)
    print("\nDialogue (optional):")
    for i, line in enumerate(lesson['dialogue']['lines']):
        audio_file = f"{lesson_id:02d}-dialogue-{i+1}.mp3"
        generate_audio(line['spanish'], audio_file)

def main():
    """Main execution"""
    # Create audio directory if it doesn't exist
    os.makedirs("audio", exist_ok=True)

    # Process all lesson files
    lesson_files = sorted([
        f for f in os.listdir("lessons")
        if f.startswith("lesson-") and f.endswith(".json")
    ])

    if not lesson_files:
        print("No lesson files found in lessons/ directory")
        return

    print(f"Found {len(lesson_files)} lesson file(s)")

    for lesson_file in lesson_files:
        process_lesson(os.path.join("lessons", lesson_file))

    print("\n✓ Audio generation complete!")
    print(f"Generated files are in the audio/ directory")

if __name__ == "__main__":
    # Check for credentials
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("ERROR: GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        print("Please set it to the path of your Google Cloud service account JSON file")
        exit(1)

    main()
