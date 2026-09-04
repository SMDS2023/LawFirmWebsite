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
        return {
            website: component.formData.website || '',
            utm_source: component.utmData.utm_source || '',
            utm_medium: component.utmData.utm_medium || '',
            utm_campaign: component.utmData.utm_campaign || '',
            utm_content: component.utmData.utm_content || '',
            utm_term: component.utmData.utm_term || '',
            gclid: component.utmData.gclid || '',
            landing_page: component.utmData.landing_page || window.location.pathname,
            referrer: document.referrer || '',
            user_agent: navigator.userAgent || ''
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
            const params = new URLSearchParams(window.location.search);
            const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid'];

            utmKeys.forEach(key => {
                const value = params.get(key);
                if (value && !sessionStorage.getItem(key)) {
                    sessionStorage.setItem(key, value);
                }
            });

            const fbclid = params.get('fbclid');
            if (fbclid && !sessionStorage.getItem('gclid')) {
                sessionStorage.setItem('gclid', fbclid);
            }

            const defaults = {
                utm_source: 'vehicle',
                utm_medium: 'qr',
                utm_campaign: 'car_page'
            };
            Object.keys(defaults).forEach(key => {
                if (!sessionStorage.getItem(key)) {
                    sessionStorage.setItem(key, defaults[key]);
                }
            });

            if (!sessionStorage.getItem('landing_page')) {
                sessionStorage.setItem('landing_page', '/car/');
            }

            this.utmData = {};
            utmKeys.forEach(key => {
                this.utmData[key] = sessionStorage.getItem(key) || '';
            });
            this.utmData.landing_page = sessionStorage.getItem('landing_page') || '/car/';
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
                    if (window.dataLayer) {
                        window.dataLayer.push({
                            'event': 'form_submission',
                            'form_name': 'car_qr_optin',
                            'case_type': this.formData.caseType || 'Other',
                            'utm_source': this.utmData.utm_source || 'vehicle',
                            'utm_medium': this.utmData.utm_medium || 'qr',
                            'utm_campaign': this.utmData.utm_campaign || 'car_page',
                            'landing_page': this.utmData.landing_page || '/car/'
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
