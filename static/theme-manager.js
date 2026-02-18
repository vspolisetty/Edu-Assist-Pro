/**
 * Unified Theme Manager for Edu Assist Pro
 * Handles theme toggling consistently across all pages
 */

(function() {
    'use strict';
    
    // Apply theme immediately to prevent flash
    const saved = localStorage.getItem('theme') || localStorage.getItem('edu_theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    
    // Also set body class for pages that use it
    document.body.className = document.body.className.replace(/\b(light|dark)-theme\b/g, '').trim();
    document.body.classList.add(`${saved}-theme`);
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        initTheme();
    });
    
    function initTheme() {
        const saved = localStorage.getItem('theme') || localStorage.getItem('edu_theme') || 'light';
        
        // Apply theme to both systems (data-theme and body class)
        applyTheme(saved);
        
        // Find the toggle button (supports both IDs)
        const btn = document.getElementById('themeToggle') || document.getElementById('theme-toggle');
        
        if (btn) {
            // Update icon to match current theme
            updateIcon(btn, saved);
            
            // Remove any existing listeners by cloning the button
            const newBtn = btn.cloneNode(true);
            btn.parentNode.replaceChild(newBtn, btn);
            
            // Add click handler
            newBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const current = document.documentElement.getAttribute('data-theme') || 'light';
                const next = current === 'dark' ? 'light' : 'dark';
                
                applyTheme(next);
                updateIcon(this, next);
                
                // Save to localStorage
                localStorage.setItem('theme', next);
                localStorage.setItem('edu_theme', next);
            });
        }
    }
    
    function applyTheme(theme) {
        // Primary method: data-theme attribute on documentElement
        document.documentElement.setAttribute('data-theme', theme);
        
        // Secondary method: body class for pages that use it
        document.body.className = document.body.className.replace(/\b(light|dark)-theme\b/g, '').trim();
        document.body.classList.add(`${theme}-theme`);
    }
    
    function updateIcon(btn, theme) {
        const icon = btn.querySelector('.material-icons');
        if (icon) {
            // Show sun (light_mode) when in dark mode (to switch to light)
            // Show moon (dark_mode) when in light mode (to switch to dark)
            icon.textContent = theme === 'dark' ? 'light_mode' : 'dark_mode';
        }
    }
    
    // Export for manual use if needed
    window.ThemeManager = {
        toggle: function() {
            const current = document.documentElement.getAttribute('data-theme') || 'light';
            const next = current === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            localStorage.setItem('theme', next);
            localStorage.setItem('edu_theme', next);
            
            const btn = document.getElementById('themeToggle') || document.getElementById('theme-toggle');
            if (btn) updateIcon(btn, next);
        },
        getTheme: function() {
            return document.documentElement.getAttribute('data-theme') || 'light';
        },
        setTheme: function(theme) {
            applyTheme(theme);
            localStorage.setItem('theme', theme);
            localStorage.setItem('edu_theme', theme);
            
            const btn = document.getElementById('themeToggle') || document.getElementById('theme-toggle');
            if (btn) updateIcon(btn, theme);
        }
    };
})();
