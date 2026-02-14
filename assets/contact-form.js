// Alpine.js Contact Form Component
// Handles validation, submission, and user feedback for native contact forms

document.addEventListener('alpine:init', () => {
    Alpine.data('contactForm', () => ({
        // Form state
        formData: {
            name: '',
            email: '',
            phone: '',
            caseType: '',
            message: ''
        },

        // UTM tracking data (populated on init, submitted as hidden fields)
        utmData: {},

        // Capture UTM params from URL and store in sessionStorage (first-touch attribution)
        init() {
            const params = new URLSearchParams(window.location.search);
            const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid'];

            // Store UTM params in sessionStorage (first-touch: don't overwrite existing)
            utmKeys.forEach(key => {
                const value = params.get(key);
                if (value && !sessionStorage.getItem(key)) {
                    sessionStorage.setItem(key, value);
                }
            });

            // Also capture fbclid as gclid (both are click IDs)
            const fbclid = params.get('fbclid');
            if (fbclid && !sessionStorage.getItem('gclid')) {
                sessionStorage.setItem('gclid', fbclid);
            }

            // Capture landing page (first page in session)
            if (!sessionStorage.getItem('landing_page')) {
                sessionStorage.setItem('landing_page', window.location.pathname);
            }

            // Load UTM data for form submission
            this.utmData = {};
            utmKeys.forEach(key => {
                this.utmData[key] = sessionStorage.getItem(key) || '';
            });
            this.utmData.landing_page = sessionStorage.getItem('landing_page') || window.location.pathname;
        },

        // Validation state
        errors: {
            name: '',
            email: '',
            phone: '',
            caseType: '',
            message: ''
        },

        touched: {
            name: false,
            email: false,
            phone: false,
            caseType: false,
            message: false
        },

        // UI state
        submitting: false,
        showSuccess: false,
        showError: false,

        // Validation methods
        validateName() {
            if (!this.formData.name.trim()) {
                this.errors.name = 'Name is required';
                return false;
            }
            if (this.formData.name.trim().length < 2) {
                this.errors.name = 'Name must be at least 2 characters';
                return false;
            }
            this.errors.name = '';
            return true;
        },

        validateEmail() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!this.formData.email.trim()) {
                this.errors.email = 'Email is required';
                return false;
            }
            if (!emailRegex.test(this.formData.email)) {
                this.errors.email = 'Please enter a valid email address';
                return false;
            }
            this.errors.email = '';
            return true;
        },

        validatePhone() {
            const digits = this.formData.phone.replace(/\D/g, '');
            if (!this.formData.phone.trim()) {
                this.errors.phone = 'Phone number is required';
                return false;
            }
            if (digits.length < 10) {
                this.errors.phone = 'Phone number must be at least 10 digits';
                return false;
            }
            this.errors.phone = '';
            return true;
        },

        validateCaseType() {
            if (!this.formData.caseType) {
                this.errors.caseType = 'Please select a case type';
                return false;
            }
            this.errors.caseType = '';
            return true;
        },

        validateMessage() {
            if (!this.formData.message.trim()) {
                this.errors.message = 'Message is required';
                return false;
            }
            if (this.formData.message.trim().length < 10) {
                this.errors.message = 'Message must be at least 10 characters';
                return false;
            }
            this.errors.message = '';
            return true;
        },

        // Validate all fields
        validateAll() {
            const nameValid = this.validateName();
            const emailValid = this.validateEmail();
            const phoneValid = this.validatePhone();
            const caseTypeValid = this.validateCaseType();
            const messageValid = this.validateMessage();

            return nameValid && emailValid && phoneValid && caseTypeValid && messageValid;
        },

        // Check if form is valid (for button state)
        get isValid() {
            return this.formData.name.trim().length >= 2 &&
                   /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.formData.email) &&
                   this.formData.phone.replace(/\D/g, '').length >= 10 &&
                   this.formData.caseType !== '' &&
                   this.formData.message.trim().length >= 10;
        },

        // Mark field as touched
        markTouched(field) {
            this.touched[field] = true;
        },

        // Handle field blur
        onBlur(field) {
            this.markTouched(field);
            this['validate' + field.charAt(0).toUpperCase() + field.slice(1)]();
        },

        // Handle form submission
        async submitForm() {
            // Mark all fields as touched
            Object.keys(this.touched).forEach(key => {
                this.touched[key] = true;
            });

            // Validate all fields
            if (!this.validateAll()) {
                return;
            }

            // Set submitting state
            this.submitting = true;
            this.showSuccess = false;
            this.showError = false;

            try {
                // Map to JotForm field names (actual field names from form 251224345324145)
                const formData = new URLSearchParams();

                // Split name into first and last
                const nameParts = this.formData.name.trim().split(' ');
                const firstName = nameParts[0] || '';
                const lastName = nameParts.slice(1).join(' ') || '';

                formData.append('q3_name[first]', firstName);
                formData.append('q3_name[last]', lastName);
                formData.append('q4_contactNumber[full]', this.formData.phone);
                formData.append('q5_emailAddress', this.formData.email);
                formData.append('q10_pleaseExplain', this.formData.message);
                formData.append('q23_typeA23', this.formData.caseType);

                // Append UTM tracking hidden fields
                formData.append('q24_utmSource', this.utmData.utm_source || '');
                formData.append('q25_utmMedium', this.utmData.utm_medium || '');
                formData.append('q26_utmCampaign', this.utmData.utm_campaign || '');
                formData.append('q27_utmContent', this.utmData.utm_content || '');
                formData.append('q28_utmTerm', this.utmData.utm_term || '');
                formData.append('q29_gclid', this.utmData.gclid || '');
                formData.append('q30_landingPage', this.utmData.landing_page || window.location.pathname);

                // Submit to JotForm
                const response = await fetch('https://submit.jotform.com/submit/251224345324145', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                });

                if (response.ok) {
                    // Show success message
                    this.showSuccess = true;

                    // Track in GTM with UTM attribution
                    if (window.dataLayer) {
                        window.dataLayer.push({
                            'event': 'form_submission',
                            'form_name': 'contact_form',
                            'case_type': this.formData.caseType,
                            'utm_source': this.utmData.utm_source || 'direct',
                            'utm_medium': this.utmData.utm_medium || '',
                            'utm_campaign': this.utmData.utm_campaign || '',
                            'landing_page': this.utmData.landing_page || ''
                        });
                    }

                    // Reset form after 2 seconds
                    setTimeout(() => {
                        this.resetForm();
                    }, 2000);
                } else {
                    throw new Error('Form submission failed');
                }
            } catch (error) {
                console.error('Form submission error:', error);
                this.showError = true;
            } finally {
                this.submitting = false;
            }
        },

        // Reset form
        resetForm() {
            this.formData = {
                name: '',
                email: '',
                phone: '',
                caseType: '',
                message: ''
            };
            this.errors = {
                name: '',
                email: '',
                phone: '',
                caseType: '',
                message: ''
            };
            this.touched = {
                name: false,
                email: false,
                phone: false,
                caseType: false,
                message: false
            };
            this.showSuccess = false;
            this.showError = false;
        }
    }));
});
