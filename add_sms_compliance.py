#!/usr/bin/env python3
"""
Add SMS Compliance Disclosure to Lotter Law Contact Forms

This script adds TCPA-compliant SMS disclosure text to all contact forms
on the Lotter Law website. The text is inserted below the phone number
input field to meet RingCentral/Campaign Registry requirements.

Requirements addressed:
1. Opt-out instructions (STOP)
2. Customer support info (HELP)
3. Message/data rates disclosure
4. Message frequency disclosure
"""

import re
from pathlib import Path

# Base directory for website files
WEBSITE_DIR = Path(__file__).parent

# English files to update (20 files)
ENGLISH_FILES = [
    "index.html",
    "service-areas.html",
    "practice-areas/assault-battery.html",
    "practice-areas/auto-registration.html",
    "practice-areas/criminal-traffic.html",
    "practice-areas/driver-license-restoration.html",
    "practice-areas/drug-offense.html",
    "practice-areas/dui.html",
    "practice-areas/dv.html",
    "practice-areas/excessive-speed.html",
    "practice-areas/hit-and-run.html",
    "practice-areas/moving-violations.html",
    "practice-areas/other-crimes.html",
    "practice-areas/seal-and-expunge.html",
    "practice-areas/speeding-ticket.html",
    "practice-areas/suspended-license.html",
    "practice-areas/theft.html",
    "practice-areas/tolls.html",
    "practice-areas/weapons.html",
    "practice-areas/practice-area-template-.html",
]

# Spanish files to update (13 files)
SPANISH_FILES = [
    "es/index.html",
    "es/service-areas.html",
    "es/practice-areas/assault-battery.html",
    "es/practice-areas/criminal-traffic.html",
    "es/practice-areas/driver-license-restoration.html",
    "es/practice-areas/drug-offense.html",
    "es/practice-areas/dui.html",
    "es/practice-areas/dv.html",
    "es/practice-areas/moving-violations.html",
    "es/practice-areas/seal-and-expunge.html",
    "es/practice-areas/speeding-ticket.html",
    "es/practice-areas/suspended-license.html",
    "es/practice-areas/theft.html",
]

# Compliance text (English)
ENGLISH_COMPLIANCE = '''
                        <p class="text-gray-600 text-xs mt-2 leading-relaxed">By providing your phone number, you consent to receive SMS messages from Lotter Law. Message frequency varies. Message and data rates may apply. Reply HELP for help or STOP to unsubscribe.</p>
                        '''

# Compliance text (Spanish)
SPANISH_COMPLIANCE = '''
                        <p class="text-gray-600 text-xs mt-2 leading-relaxed">Al proporcionar su número de teléfono, usted consiente recibir mensajes SMS de Lotter Law. La frecuencia de mensajes varía. Pueden aplicarse tarifas de mensajes y datos. Responda HELP para ayuda o STOP para cancelar la suscripción.</p>
                        '''

# Regex pattern to find phone field closing tag (after error message)
# Matches: <p x-show="touched.phone && errors.phone"...>...</p> followed by </div>
PHONE_FIELD_PATTERN = re.compile(
    r'(<p x-show="touched\.phone && errors\.phone"[^>]*>.*?</p>)\s*(</div>)',
    re.DOTALL
)


def add_compliance_text(file_path: Path, compliance_text: str, test_mode: bool = False) -> bool:
    """
    Add SMS compliance text to a single file.

    Args:
        file_path: Path to HTML file
        compliance_text: The compliance disclosure to insert
        test_mode: If True, only test on template file

    Returns:
        True if file was updated, False if skipped or already has disclosure
    """
    try:
        # Read file
        content = file_path.read_text(encoding='utf-8')

        # Check if compliance text already exists
        if "you consent to receive SMS messages from Lotter Law" in content or \
           "usted consiente recibir mensajes SMS de Lotter Law" in content:
            print(f"[SKIP] {file_path.name} (already has compliance text)")
            return False

        # Find and replace
        match = PHONE_FIELD_PATTERN.search(content)
        if not match:
            print(f"[ERROR] {file_path.name} (phone field pattern not found)")
            return False

        # Insert compliance text between error message and closing div
        new_content = PHONE_FIELD_PATTERN.sub(
            rf'\1{compliance_text}\2',
            content
        )

        # Write back to file (unless test mode)
        if not test_mode:
            file_path.write_text(new_content, encoding='utf-8')

        print(f"[OK] {file_path.name}")
        return True

    except Exception as e:
        print(f"[ERROR] {file_path.name} ({str(e)})")
        return False


def main():
    """Process all English and Spanish files."""
    print("=" * 70)
    print("SMS Compliance Disclosure Update")
    print("=" * 70)
    print()

    updated_count = 0
    skipped_count = 0
    error_count = 0

    # Process English files
    print("Processing English files (20 files)...")
    print("-" * 70)
    for file_rel_path in ENGLISH_FILES:
        file_path = WEBSITE_DIR / file_rel_path
        if not file_path.exists():
            print(f"WARNING: {file_rel_path} (file not found)")
            error_count += 1
            continue

        result = add_compliance_text(file_path, ENGLISH_COMPLIANCE)
        if result:
            updated_count += 1
        elif "SKIP" in str(result):
            skipped_count += 1
        else:
            error_count += 1

    print()

    # Process Spanish files
    print("Processing Spanish files (13 files)...")
    print("-" * 70)
    for file_rel_path in SPANISH_FILES:
        file_path = WEBSITE_DIR / file_rel_path
        if not file_path.exists():
            print(f"WARNING: {file_rel_path} (file not found)")
            error_count += 1
            continue

        result = add_compliance_text(file_path, SPANISH_COMPLIANCE)
        if result:
            updated_count += 1
        elif "SKIP" in str(result):
            skipped_count += 1
        else:
            error_count += 1

    # Summary
    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"[OK] Updated: {updated_count} files")
    print(f"[SKIP] Skipped: {skipped_count} files (already compliant)")
    print(f"[ERROR] Errors:  {error_count} files")
    print()

    if updated_count > 0:
        print("Next steps:")
        print("1. Review changes: git diff")
        print("2. Test in browser (homepage + DUI practice area)")
        print("3. Commit and push to feature branch")
        print()


if __name__ == "__main__":
    main()
