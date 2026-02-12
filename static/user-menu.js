/**
 * User Menu Dropdown — shared across all pages
 * Handles: toggle dropdown, set username, settings modal, logout
 */
(function () {
    'use strict';

    const btn = document.getElementById('userMenuBtn');
    const dropdown = document.getElementById('userDropdown');
    const logoutBtn = document.getElementById('logoutBtn');
    const settingsBtn = document.getElementById('settingsBtn');
    const userNameEl = document.getElementById('userName');

    /* ── Set display name from localStorage ── */
    function setUserName() {
        try {
            const u = JSON.parse(localStorage.getItem('currentUser') || '{}');
            const name = u.name || u.username || u.user_id || 'User';
            if (userNameEl) userNameEl.textContent = name;
        } catch (_) { /* ignore */ }
    }
    setUserName();

    /* ── Toggle dropdown ── */
    function openDropdown() {
        dropdown.classList.add('open');
        btn.classList.add('active');
    }

    function closeDropdown() {
        dropdown.classList.remove('open');
        btn.classList.remove('active');
    }

    btn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (dropdown.classList.contains('open')) {
            closeDropdown();
        } else {
            openDropdown();
        }
    });

    /* Close when clicking outside */
    document.addEventListener('click', function (e) {
        if (!btn.contains(e.target) && !dropdown.contains(e.target)) {
            closeDropdown();
        }
    });

    /* Close on Escape */
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeDropdown();
    });

    /* ── Settings ── */
    if (settingsBtn) {
        settingsBtn.addEventListener('click', function (e) {
            e.preventDefault();
            closeDropdown();
            openSettingsModal();
        });
    }

    /* ── Logout ── */
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function (e) {
            e.preventDefault();
            closeDropdown();
            localStorage.removeItem('currentUser');
            localStorage.removeItem('edu_user');
            localStorage.removeItem('authToken');
            window.location.href = 'login.html';
        });
    }

    /* ── Settings Modal ── */
    function openSettingsModal() {
        // Remove existing modal if any
        const existing = document.getElementById('settingsModal');
        if (existing) existing.remove();

        const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
                    || document.body.classList.contains('dark-theme');

        const modal = document.createElement('div');
        modal.id = 'settingsModal';
        modal.className = 'settings-overlay';
        modal.innerHTML = `
            <div class="settings-modal">
                <div class="settings-header">
                    <h2><span class="material-icons">settings</span> Settings</h2>
                    <button class="settings-close" id="settingsClose">
                        <span class="material-icons">close</span>
                    </button>
                </div>
                <div class="settings-body">
                    <div class="settings-group">
                        <h3>Appearance</h3>
                        <label class="settings-row">
                            <span><span class="material-icons">dark_mode</span> Dark Mode</span>
                            <input type="checkbox" id="settingsDarkMode" ${isDark ? 'checked' : ''}>
                        </label>
                    </div>
                    <div class="settings-group">
                        <h3>Notifications</h3>
                        <label class="settings-row">
                            <span><span class="material-icons">notifications</span> Email Notifications</span>
                            <input type="checkbox" id="settingsNotif" checked>
                        </label>
                    </div>
                    <div class="settings-group">
                        <h3>Account</h3>
                        <div class="settings-row account-info">
                            <span><span class="material-icons">person</span> <span id="settingsUserDisplay">${userNameEl ? userNameEl.textContent : 'User'}</span></span>
                        </div>
                    </div>
                </div>
                <div class="settings-footer">
                    <button class="settings-btn-save" id="settingsSave">Save</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Animate in
        requestAnimationFrame(() => modal.classList.add('open'));

        // Close handlers
        document.getElementById('settingsClose').addEventListener('click', closeSettings);
        modal.addEventListener('click', function (e) {
            if (e.target === modal) closeSettings();
        });

        // Dark mode toggle inside settings
        document.getElementById('settingsDarkMode').addEventListener('change', function () {
            if (this.checked) {
                document.body.classList.remove('light-theme');
                document.body.classList.add('dark-theme');
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.remove('dark-theme');
                document.body.classList.add('light-theme');
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
            }
        });

        // Save
        document.getElementById('settingsSave').addEventListener('click', function () {
            closeSettings();
        });

        function closeSettings() {
            modal.classList.remove('open');
            setTimeout(() => modal.remove(), 250);
        }
    }
})();
