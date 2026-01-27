#!/usr/bin/env python3
"""
Script to replace JotForm iframes with native HTML forms across all practice area pages.
"""
import os
import re

# Define the directory containing practice area pages
PRACTICE_AREAS_DIR = r"C:\Users\jeff\OneDrive\Documents\LotterLaw\Website\practice-areas"

# Files to update (excluding dui.html which is already done)
FILES_TO_UPDATE = [
    "assault-battery.html",
    "auto-registration.html",
    "criminal-traffic.html",
    "driver-license-restoration.html",
    "drug-offense.html",
    "dv.html",
    "excessive-speed.html",
    "hit-and-run.html",
    "moving-violations.html",
    "other-crimes.html",
    "practice-area-template-.html",
    "seal-and-expunge.html",
    "speeding-ticket.html",
    "suspended-license.html",
    "theft.html",
    "tolls.html",
    "weapons.html"
]

# Script tag to add after Alpine.js
SCRIPT_TAG = '    <script defer src="../assets/contact-form.js"></script>'

# Pattern to find Alpine.js script tag
ALPINEJS_PATTERN = r'(<script defer src="https://cdn\.jsdelivr\.net/npm/alpinejs@3\.x\.x/dist/cdn\.min\.js"></script>)'

# Native form HTML
NATIVE_FORM = '''                 <div class="max-w-2xl mx-auto section-fade-in">
                    <form x-data="contactForm()" @submit.prevent="submitForm()" class="bg-white p-8 rounded-lg shadow-xl space-y-6 text-gray-900">
                        <!-- Success Alert -->
                        <div x-show="showSuccess" role="alert" class="bg-green-100 border border-green-400 text-green-700 px-6 py-4 rounded-lg">
                            <strong class="font-bold">Success!</strong>
                            <span class="block">Your message has been sent. We'll contact you shortly.</span>
                        </div>

                        <!-- Error Alert -->
                        <div x-show="showError" role="alert" class="bg-red-100 border border-red-400 text-red-700 px-6 py-4 rounded-lg">
                            <strong class="font-bold">Error!</strong>
                            <span class="block">There was a problem submitting your form. Please call us directly at <a href="tel:407-500-7000" class="underline font-bold">407-500-7000</a>.</span>
                        </div>

                        <!-- Name Field -->
                        <div>
                            <label for="name" class="block text-gray-700 font-semibold mb-2">
                                Full Name <span class="text-red-500">*</span>
                            </label>
                            <input
                                type="text"
                                id="name"
                                x-model="formData.name"
                                @blur="onBlur('name')"
                                @input="touched.name && validateName()"
                                :class="{'border-red-500': touched.name && errors.name}"
                                class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                                placeholder="John Smith"
                            />
                            <p x-show="touched.name && errors.name" x-text="errors.name" class="text-red-600 text-sm mt-1"></p>
                        </div>

                        <!-- Email Field -->
                        <div>
                            <label for="email" class="block text-gray-700 font-semibold mb-2">
                                Email Address <span class="text-red-500">*</span>
                            </label>
                            <input
                                type="email"
                                id="email"
                                x-model="formData.email"
                                @blur="onBlur('email')"
                                @input="touched.email && validateEmail()"
                                :class="{'border-red-500': touched.email && errors.email}"
                                class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                                inputmode="email"
                                placeholder="john@example.com"
                            />
                            <p x-show="touched.email && errors.email" x-text="errors.email" class="text-red-600 text-sm mt-1"></p>
                        </div>

                        <!-- Phone Field -->
                        <div>
                            <label for="phone" class="block text-gray-700 font-semibold mb-2">
                                Phone Number <span class="text-red-500">*</span>
                            </label>
                            <input
                                type="tel"
                                id="phone"
                                x-model="formData.phone"
                                @blur="onBlur('phone')"
                                @input="touched.phone && validatePhone()"
                                :class="{'border-red-500': touched.phone && errors.phone}"
                                class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                                inputmode="tel"
                                placeholder="407-555-1234"
                            />
                            <p x-show="touched.phone && errors.phone" x-text="errors.phone" class="text-red-600 text-sm mt-1"></p>
                        </div>

                        <!-- Case Type Field -->
                        <div>
                            <label for="caseType" class="block text-gray-700 font-semibold mb-2">
                                Case Type <span class="text-red-500">*</span>
                            </label>
                            <select
                                id="caseType"
                                x-model="formData.caseType"
                                @blur="onBlur('caseType')"
                                @change="touched.caseType && validateCaseType()"
                                :class="{'border-red-500': touched.caseType && errors.caseType}"
                                class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                            >
                                <option value="">Select a case type...</option>
                                <option value="DUI">DUI</option>
                                <option value="Traffic">Traffic</option>
                                <option value="Criminal">Criminal</option>
                                <option value="License">Driver License</option>
                                <option value="Other">Other</option>
                            </select>
                            <p x-show="touched.caseType && errors.caseType" x-text="errors.caseType" class="text-red-600 text-sm mt-1"></p>
                        </div>

                        <!-- Message Field -->
                        <div>
                            <label for="message" class="block text-gray-700 font-semibold mb-2">
                                Tell Us About Your Case <span class="text-red-500">*</span>
                            </label>
                            <textarea
                                id="message"
                                x-model="formData.message"
                                @blur="onBlur('message')"
                                @input="touched.message && validateMessage()"
                                :class="{'border-red-500': touched.message && errors.message}"
                                class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                                rows="4"
                                placeholder="Please provide details about your case..."
                            ></textarea>
                            <p x-show="touched.message && errors.message" x-text="errors.message" class="text-red-600 text-sm mt-1"></p>
                        </div>

                        <!-- Submit Button -->
                        <button
                            type="submit"
                            :disabled="!isValid || submitting"
                            class="w-full bg-amber-500 hover:bg-amber-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-bold py-4 px-8 rounded-lg text-lg transition duration-300 shadow-lg inline-flex items-center justify-center"
                        >
                            <svg x-show="submitting" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            <span x-text="submitting ? 'Sending...' : 'Send Message'"></span>
                        </button>
                    </form>
                </div>'''

def add_script_tag(content):
    """Add contact-form.js script tag after Alpine.js if not already present."""
    if 'contact-form.js' in content:
        return content

    # Add script tag after Alpine.js
    replacement = r'\1\n    <script defer src="../assets/contact-form.js"></script>'
    return re.sub(ALPINEJS_PATTERN, replacement, content)

def replace_jotform_iframe(content):
    """Replace JotForm iframe with native form HTML."""
    # Pattern to match JotForm iframe container (various formats)
    # This matches the div container through the closing </div>
    pattern = r'<div class="max-w-2xl mx-auto.*?section-fade-in">\s*<iframe[^>]*JotFormIFrame[^>]*>.*?</iframe>.*?(?:<script[^>]*>.*?</script>\s*)*</div>'

    # Replace with native form
    return re.sub(pattern, NATIVE_FORM, content, flags=re.DOTALL)

def update_file(filepath):
    """Update a single HTML file."""
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file has JotForm iframe
        if 'JotFormIFrame' not in content:
            print(f"  [SKIPPED]  Skipped (no JotForm found)")
            return False

        # Add script tag
        content = add_script_tag(content)

        # Replace iframe
        new_content = replace_jotform_iframe(content)

        # Check if replacement was made
        if new_content == content:
            print(f"  [WARNING]  Warning: Pattern didn't match")
            return False

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  [OK] Updated successfully")
        return True

    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        return False

def main():
    """Main function to update all files."""
    print("Replacing JotForm iframes with native forms...\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for filename in FILES_TO_UPDATE:
        filepath = os.path.join(PRACTICE_AREAS_DIR, filename)
        print(f"Processing {filename}...")

        if not os.path.exists(filepath):
            print(f"  [WARNING]  File not found")
            error_count += 1
            continue

        result = update_file(filepath)
        if result:
            updated_count += 1
        elif result is False and 'JotFormIFrame' in open(filepath, encoding='utf-8').read():
            error_count += 1
        else:
            skipped_count += 1

    print(f"\nSummary: Summary:")
    print(f"  [OK] Updated: {updated_count}")
    print(f"  [SKIPPED]  Skipped: {skipped_count}")
    print(f"  [ERROR] Errors: {error_count}")
    print(f"\nDone! Done!")

if __name__ == "__main__":
    main()
