// Alpine.js Contact Form Component
// Handles validation, submission, and user feedback for native contact forms

document.addEventListener('alpine:init', () => {
    const LEAD_ENDPOINT = 'https://lotterlaw-leads.vercel.app/api/lead';

    function installHoneypot(component) {
        const form = component.$root;
        if (!form || form.querySelector('[data-lead-honeypot]')) {
            return;
        }
        const input = document.createElement('input');
        input.type = 'text';
        input.name = 'website';
        input.autocomplete = 'off';
        input.tabIndex = -1;
        input.setAttribute('aria-hidden', 'true');
        input.setAttribute('data-lead-honeypot', '');
        input.style.position = 'absolute';
        input.style.left = '-10000px';
        input.style.width = '1px';
        input.style.height = '1px';
        input.style.opacity = '0';
        input.addEventListener('input', () => {
            component.formData.website = input.value;
        });
        form.appendChild(input);
    }

    function trackingPayload(component) {
        const tracking = window.LotterLeadTracking?.payload() || {
            tracking_version: '2',
            tracking_storage: 'page-only',
            landing_page: window.location.origin + window.location.pathname,
            submission_page: window.location.origin + window.location.pathname,
            entry_referrer: '',
            referrer: '',
            user_agent: navigator.userAgent.slice(0, 512)
        };
        return { website: component.formData.website || '', ...tracking };
    }

    function analyticsTracking(component) {
        const tracking = trackingPayload(component);
        let entryHost = '';
        try { entryHost = new URL(tracking.entry_referrer).hostname; } catch (_) {}
        // Only attribution is sent to analytics; never contact fields, message, honeypot or user agent.
        return {
            utm_source: tracking.utm_source || '',
            utm_medium: tracking.utm_medium || '',
            utm_campaign: tracking.utm_campaign || '',
            landing_page: tracking.landing_page || '',
            submission_page: tracking.submission_page || '',
            entry_referrer_host: entryHost,
            tracking_storage: tracking.tracking_storage || 'page-only'
        };
    }

    Alpine.data('contactForm', () => ({
        // Form state
        formData: {
            name: '',
            email: '',
            phone: '',
            caseType: '',
            message: '',
            website: ''
        },

        // UTM tracking data (populated on init, submitted as hidden fields)
        utmData: {},

        // Capture UTM params from URL and store in sessionStorage (first-touch attribution)
        init() {
            installHoneypot(this);
            this.utmData = trackingPayload(this);
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
                const response = await fetch(LEAD_ENDPOINT, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        form: 'contact',
                        name: this.formData.name,
                        phone: this.formData.phone,
                        email: this.formData.email,
                        message: this.formData.message,
                        caseType: this.formData.caseType,
                        smsConsent: true,
                        ...trackingPayload(this)
                    })
                });
                const result = await response.json().catch(() => ({ ok: false }));

                if (response.ok && result.ok) {
                    // Show success message
                    this.showSuccess = true;

                    // Track in GTM with UTM attribution
                    if (window.dataLayer && typeof result.id === 'string' && result.id) {
                        window.dataLayer.push({
                            'event': 'form_submission',
                            'form_name': 'contact_form',
                            'case_type': this.formData.caseType,
                            ...analyticsTracking(this)
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
                console.error('Form submission failed.');
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
                message: '',
                website: ''
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

    // Short opt-in for the Tesla wrap QR lander at /car/. Do not change contactForm above.
    Alpine.data('qrOptInForm', () => ({
        formData: {
            name: '',
            phone: '',
            caseType: '',
            website: ''
        },
        smsConsent: false,
        utmData: {},
        errors: {
            name: '',
            phone: '',
            smsConsent: ''
        },
        touched: {
            name: false,
            phone: false,
            smsConsent: false
        },
        submitting: false,
        showSuccess: false,
        showError: false,

        init() {
            installHoneypot(this);
            this.utmData = trackingPayload(this);
        },

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

        validateSmsConsent() {
            if (!this.smsConsent) {
                this.errors.smsConsent = 'Check the box to agree to text updates';
                return false;
            }
            this.errors.smsConsent = '';
            return true;
        },

        validateAll() {
            const nameValid = this.validateName();
            const phoneValid = this.validatePhone();
            const consentValid = this.validateSmsConsent();
            return nameValid && phoneValid && consentValid;
        },

        markTouched(field) {
            this.touched[field] = true;
        },

        onBlur(field) {
            this.markTouched(field);
            const method = 'validate' + field.charAt(0).toUpperCase() + field.slice(1);
            if (typeof this[method] === 'function') {
                this[method]();
            }
        },

        async submitForm() {
            Object.keys(this.touched).forEach(key => {
                this.touched[key] = true;
            });

            if (!this.validateAll()) {
                return;
            }

            this.submitting = true;
            this.showSuccess = false;
            this.showError = false;

            try {
                const response = await fetch(LEAD_ENDPOINT, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        form: 'car',
                        name: this.formData.name,
                        phone: this.formData.phone,
                        caseType: this.formData.caseType || 'Other',
                        smsConsent: this.smsConsent,
                        ...trackingPayload(this)
                    })
                });
                const result = await response.json().catch(() => ({ ok: false }));

                if (response.ok && result.ok) {
                    this.showSuccess = true;
                    if (window.dataLayer && typeof result.id === 'string' && result.id) {
                        window.dataLayer.push({
                            'event': 'form_submission',
                            'form_name': 'car_qr_optin',
                            'case_type': this.formData.caseType || 'Other',
                            ...analyticsTracking(this)
                        });
                    }
                    this.formData = { name: '', phone: '', caseType: '', website: '' };
                    this.smsConsent = false;
                    this.touched = { name: false, phone: false, smsConsent: false };
                    this.errors = { name: '', phone: '', smsConsent: '' };
                } else {
                    throw new Error('Form submission failed');
                }
            } catch (error) {
                console.error('Form submission failed.');
                this.showError = true;
            } finally {
                this.submitting = false;
            }
        }
    }));
});
