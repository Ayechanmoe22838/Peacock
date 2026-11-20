/**
 * PEACOCK - Smart Wedding Reception System
 * Frontend interactive utilities, dual-theme engine, and UX helpers
 * Adhering strictly to Section 8.2 and Section 9 of implementation.md
 */

// Global register for Chart.js instances to allow live theme repainting
window.peacockCharts = window.peacockCharts || [];

/**
 * Apply theme to document, update toggle buttons, and repaint Chart.js
 */
function applyPeacockTheme(theme) {
    let applied = theme;
    if (theme === 'system') {
        applied = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    
    // Set Bootstrap 5.3 & custom CSS theme attribute
    document.documentElement.setAttribute('data-bs-theme', applied);
    
    // Update all theme toggle buttons across public, customer, and admin navbars
    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    toggleBtns.forEach(btn => {
        const icon = btn.querySelector('.theme-toggle-icon');
        const text = btn.querySelector('.theme-toggle-text');
        
        if (applied === 'dark') {
            if (icon) icon.className = 'theme-toggle-icon bi bi-sun-fill text-warning fs-5';
            if (text) text.textContent = 'Light Mode';
            btn.setAttribute('title', 'Switch to Light Mode');
            btn.setAttribute('aria-label', 'Switch to Light Mode');
        } else {
            if (icon) icon.className = 'theme-toggle-icon bi bi-moon-stars-fill text-primary fs-5';
            if (text) text.textContent = 'Dark Mode';
            btn.setAttribute('title', 'Switch to Dark Mode');
            btn.setAttribute('aria-label', 'Switch to Dark Mode');
        }
    });

    // Update active check in theme dropdown menus if present
    const dropdownActiveText = document.getElementById('themeDropdownActiveText');
    if (dropdownActiveText) {
        dropdownActiveText.textContent = applied === 'dark' ? 'Dark' : (theme === 'system' ? 'Auto' : 'Light');
    }
    
    // Repaint registered Chart.js charts dynamically without page reload
    if (window.Chart && window.peacockCharts && window.peacockCharts.length > 0) {
        const isDark = (applied === 'dark');
        // Section 9: Light mode text must be black, dark mode text must be white
        const textColor = isDark ? '#ffffff' : '#000000';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.15)' : 'rgba(0, 0, 0, 0.08)';
        
        window.peacockCharts.forEach(chart => {
            if (chart && chart.options) {
                // Update axis ticks & grids
                if (chart.options.scales) {
                    if (chart.options.scales.x) {
                        chart.options.scales.x.ticks = chart.options.scales.x.ticks || {};
                        chart.options.scales.x.ticks.color = textColor;
                        chart.options.scales.x.grid = chart.options.scales.x.grid || {};
                        chart.options.scales.x.grid.color = gridColor;
                    }
                    if (chart.options.scales.y) {
                        chart.options.scales.y.ticks = chart.options.scales.y.ticks || {};
                        chart.options.scales.y.ticks.color = textColor;
                        chart.options.scales.y.grid = chart.options.scales.y.grid || {};
                        chart.options.scales.y.grid.color = gridColor;
                    }
                }
                // Update legend labels
                if (chart.options.plugins && chart.options.plugins.legend) {
                    chart.options.plugins.legend.labels = chart.options.plugins.legend.labels || {};
                    chart.options.plugins.legend.labels.color = textColor;
                }
                chart.update();
            }
        });
    }
}

/**
 * Direct One-Click Theme Switcher (toggles between Light and Dark)
 * Never reloads the page; updates DOM instantly
 */
function togglePeacockTheme() {
    const currentApplied = document.documentElement.getAttribute('data-bs-theme') || 'light';
    const nextTheme = (currentApplied === 'dark') ? 'light' : 'dark';
    localStorage.setItem('peacock-theme', nextTheme);
    applyPeacockTheme(nextTheme);
}

/**
 * Explicit Theme Setter (light, dark, or system)
 */
function setPeacockTheme(theme) {
    localStorage.setItem('peacock-theme', theme);
    applyPeacockTheme(theme);
}

// OS Preference change listener (System auto-adapt)
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const savedTheme = localStorage.getItem('peacock-theme') || 'system';
    if (savedTheme === 'system') {
        applyPeacockTheme('system');
    }
});

document.addEventListener("DOMContentLoaded", () => {
    // 1. Initial Theme Activation
    const savedTheme = localStorage.getItem('peacock-theme') || 'system';
    applyPeacockTheme(savedTheme);

    // 2. Initialize tooltips and popovers if bootstrap is present
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl));
    }

    // 3. Prevent booking in the past
    const datePickers = document.querySelectorAll('input[type="date"][data-min-today="true"]');
    if (datePickers.length > 0) {
        const today = new Date().toISOString().split("T")[0];
        datePickers.forEach(picker => picker.min = today);
    }

    // 4. Smooth alert auto-dismissal
    const alerts = document.querySelectorAll('.alert-auto-dismiss');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                alert.remove();
            }
        }, 5000);
    });
});

/**
 * Helper: Copy text to clipboard with user feedback
 */
function copyToClipboard(text) {
    if (!navigator.clipboard) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            alert("Invitation link copied to clipboard!");
        } catch (err) {}
        document.body.removeChild(textArea);
        return;
    }
    navigator.clipboard.writeText(text).then(() => {
        alert("Invitation link copied to clipboard!");
    });
}
