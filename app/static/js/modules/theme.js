// Theme Module - Dark/Light Mode Toggle
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
    }

    // Initialize theme system
    init() {
        this.applyTheme(this.currentTheme);
        this.setupThemeToggle();
        console.log(`✅ Theme initialized: ${this.currentTheme}`);
    }

    // Apply theme
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);

        // Update toggle button icon
        const toggleBtn = document.getElementById('themeToggle');
        if (toggleBtn) {
            const icon = toggleBtn.querySelector('i');
            if (theme === 'dark') {
                icon.className = 'bi bi-sun-fill';
            } else {
                icon.className = 'bi bi-moon-stars-fill';
            }
        }
    }

    // Toggle theme
    toggle() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
        console.log(`✅ Theme toggled to: ${newTheme}`);
    }

    // Setup theme toggle button
    setupThemeToggle() {
        const toggleBtn = document.getElementById('themeToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggle());
        }
    }
}

// Export for use in main app
window.themeManager = new ThemeManager();
