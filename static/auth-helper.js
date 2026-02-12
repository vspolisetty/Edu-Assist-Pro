/**
 * Auth Helper — shared authentication utilities for all pages
 * Provides: token management, authenticated fetch, auth guards, user info
 */
(function () {
    'use strict';

    const AUTH = {
        /** Get stored JWT token */
        getToken() {
            return localStorage.getItem('authToken');
        },

        /** Get current user object */
        getUser() {
            try {
                return JSON.parse(localStorage.getItem('currentUser') || 'null');
            } catch (_) {
                return null;
            }
        },

        /** Get user ID from stored profile */
        getUserId() {
            const u = this.getUser();
            return (u && (u.id || u.user_id || u.username)) || 'default_user';
        },

        /** Get user role */
        getRole() {
            const u = this.getUser();
            return (u && u.role) || 'trainee';
        },

        /** Check if user is authenticated */
        isAuthenticated() {
            return !!this.getToken() && !!this.getUser();
        },

        /** Build Authorization header object */
        authHeaders(extra) {
            const headers = { 'Content-Type': 'application/json', ...(extra || {}) };
            const token = this.getToken();
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            return headers;
        },

        /**
         * Authenticated fetch wrapper.
         * Automatically adds Bearer token. Redirects to login on 401.
         */
        async fetch(url, options = {}) {
            const token = this.getToken();
            const headers = { ...(options.headers || {}) };
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            if (!headers['Content-Type'] && options.body && typeof options.body === 'string') {
                headers['Content-Type'] = 'application/json';
            }

            const res = await fetch(url, { ...options, headers });

            // On 401 Unauthorized, redirect to login
            if (res.status === 401) {
                this.logout();
                return res;
            }

            return res;
        },

        /**
         * Authenticated fetch that returns parsed JSON.
         * Returns null on error (non-OK responses).
         */
        async fetchJSON(url, options = {}) {
            try {
                const res = await this.fetch(url, options);
                if (!res.ok) return null;
                return await res.json();
            } catch (err) {
                console.error('Auth fetch error:', err);
                return null;
            }
        },

        /** Require authentication — redirect to login if not authenticated */
        requireAuth() {
            if (!this.isAuthenticated()) {
                window.location.href = 'login.html';
                return false;
            }
            return true;
        },

        /** Require specific role(s) — redirect if not authorized */
        requireRole(...roles) {
            if (!this.requireAuth()) return false;
            const userRole = this.getRole();
            if (!roles.includes(userRole)) {
                alert('You do not have permission to access this page.');
                window.location.href = 'dashboard.html';
                return false;
            }
            return true;
        },

        /** Clear auth data and redirect to login */
        logout() {
            localStorage.removeItem('authToken');
            localStorage.removeItem('currentUser');
            localStorage.removeItem('edu_user');
            window.location.href = 'login.html';
        }
    };

    // Expose globally
    window.AUTH = AUTH;

    // ─── Show Admin nav link for admin/manager users ─────────────────────────
    function showAdminNav() {
        const role = AUTH.getRole();
        if (role !== 'admin' && role !== 'manager') return;

        // Reveal any hidden admin nav links already in the HTML
        document.querySelectorAll('.admin-nav-link').forEach(function (el) {
            el.style.display = '';
        });

        // Fallback: if no admin link exists in the nav, inject one
        var navCenter = document.querySelector('.nav-center');
        if (navCenter && !navCenter.querySelector('a[href="admin.html"]')) {
            var link = document.createElement('a');
            link.href = 'admin.html';
            link.className = 'nav-link admin-nav-link';
            if (window.location.pathname.indexOf('admin.html') !== -1) link.classList.add('active');
            link.innerHTML = '<span class="material-icons">admin_panel_settings</span> Admin';
            navCenter.appendChild(link);
        }
    }

    // Run immediately (scripts are at bottom of body, DOM is ready)
    showAdminNav();
    // Also run on DOMContentLoaded as a safety net
    document.addEventListener('DOMContentLoaded', showAdminNav);
})();
