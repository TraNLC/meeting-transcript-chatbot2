document.addEventListener('DOMContentLoaded', () => {
    // --- Theme Toggle ---
    const themeToggle = document.getElementById('themeToggle');
    const icon = themeToggle?.querySelector('i');

    // Initial Check
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
        });
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);

        if (icon) {
            if (theme === 'dark') {
                icon.className = 'bi bi-sun-fill';
            } else {
                icon.className = 'bi bi-moon-fill';
            }
        }
    }

    // --- Language Toggle ---
    const langSelect = document.getElementById('languageSelect');
    if (langSelect) {
        // Get current language from URL param OR Cookie OR localStorage
        const getCookie = (name) => {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }

        const currentLang = new URLSearchParams(window.location.search).get('lang') || getCookie('akari_lang') || 'vi';
        langSelect.value = currentLang;

        langSelect.addEventListener('change', (e) => {
            const newLang = e.target.value;
            localStorage.setItem('language', newLang);

            // Set Cookie for Backend
            document.cookie = `akari_lang=${newLang}; path=/; max-age=31536000`; // 1 year

            // Reload to apply
            window.location.reload();
        });
    }
});
