// i18n Module - Internationalization Logic
class I18n {
    constructor() {
        this.currentLang = localStorage.getItem('language') || 'vi';
        this.translations = window.translations || {};
    }

    // Initialize i18n system
    init() {
        this.applyTranslations();
        this.setupLanguageSelector();
        console.log(`✅ i18n initialized with language: ${this.currentLang}`);
    }

    // Get translation for a key
    t(key) {
        const keys = key.split('.');
        let value = this.translations[this.currentLang];

        for (const k of keys) {
            if (value && value[k]) {
                value = value[k];
            } else {
                console.warn(`Translation missing for key: ${key} in language: ${this.currentLang}`);
                return key;
            }
        }

        return value;
    }

    // Apply translations to all elements with data-i18n attribute
    applyTranslations() {
        // Translate text content
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            el.textContent = this.t(key);
        });

        // Translate placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = this.t(key);
        });

        // Translate titles
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            el.title = this.t(key);
        });
    }

    // Change language
    changeLanguage(lang) {
        if (!this.translations[lang]) {
            console.error(`Language ${lang} not found`);
            return;
        }

        this.currentLang = lang;
        localStorage.setItem('language', lang);
        this.applyTranslations();

        // Update HTML lang attribute
        document.documentElement.lang = lang;

        console.log(`✅ Language changed to: ${lang}`);
    }

    // Setup language selector
    setupLanguageSelector() {
        const selector = document.getElementById('languageSelector');
        if (selector) {
            selector.value = this.currentLang;
            selector.addEventListener('change', (e) => {
                this.changeLanguage(e.target.value);
            });
        }
    }
}

// Export for use in main app
window.i18n = new I18n();
