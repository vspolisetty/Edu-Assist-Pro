/**
 * Edu Assist Pro — Dashboard
 * Fetches enrolled courses, quiz results, and certificates from the API.
 */
(function () {
    'use strict';

    const API = '';
    if (!window.AUTH || !AUTH.requireAuth()) return;
    const USER_ID = AUTH.getUserId();

    // ─── Init ────────────────────────────────────────────────────────────────
    async function init() {
        setupTheme();
        setupUser();
        setupCertModal();

        const [enrollments, results, certificates] = await Promise.all([
            fetchJSON(`${API}/api/enrollments/${USER_ID}`),
            fetchJSON(`${API}/api/results/${USER_ID}`),
            fetchJSON(`${API}/api/certificates/${USER_ID}`)
        ]);

        const enrollList = enrollments?.enrollments || [];
        const resultList = results?.results || [];
        const certList   = certificates?.certificates || [];

        renderStats(enrollList, resultList, certList);
        renderCourses(enrollList);
        renderResults(resultList);
        renderCertificates(certList);
    }

    // ─── Theme ───────────────────────────────────────────────────────────────
    function setupTheme() {
        const saved = localStorage.getItem('theme') || localStorage.getItem('edu_theme') || 'light';
        document.documentElement.setAttribute('data-theme', saved);
        const btn = document.getElementById('themeToggle');
        btn.querySelector('.material-icons').textContent = saved === 'dark' ? 'light_mode' : 'dark_mode';
        btn.addEventListener('click', () => {
            const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            localStorage.setItem('edu_theme', next);
            btn.querySelector('.material-icons').textContent = next === 'dark' ? 'light_mode' : 'dark_mode';
        });
    }

    function setupUser() {
        const u = JSON.parse(localStorage.getItem('currentUser') || '{}');
        const name = u.name || u.username || u.user_id || 'User';
        const el = (id) => document.getElementById(id);
        if (el('userName')) el('userName').textContent = name;
        if (el('welcomeName')) el('welcomeName').textContent = name;
    }

    // ─── Fetch ───────────────────────────────────────────────────────────────
    async function fetchJSON(url) {
        return AUTH.fetchJSON(url);
    }

    // ─── Stats ───────────────────────────────────────────────────────────────
    function renderStats(enrollList, resultList, certList) {
        document.getElementById('statCourses').textContent = enrollList.length;
        document.getElementById('statQuizzes').textContent = resultList.length;
        document.getElementById('statCerts').textContent = certList.length;

        if (resultList.length > 0) {
            const avg = resultList.reduce((s, r) => s + (r.percentage || 0), 0) / resultList.length;
            document.getElementById('statAvgScore').textContent = `${Math.round(avg)}%`;
        }
    }

    // ─── My Courses ──────────────────────────────────────────────────────────
    function renderCourses(enrollList) {
        const container = document.getElementById('myCoursesList');
        if (!enrollList.length) return; // keep empty state

        container.innerHTML = enrollList.map(e => {
            const total = e.total_modules || 1;
            const done = e.completed_modules || 0;
            const pct = Math.round((done / total) * 100);
            const icon = e.icon || '📚';
            return `
                <div class="course-row">
                    <div class="course-row-icon">${icon}</div>
                    <div class="course-row-info">
                        <div class="course-row-title">${e.title || e.course_id}</div>
                        <div class="course-row-category">${e.category || ''}</div>
                    </div>
                    <div class="course-row-progress">
                        <div class="progress-bar-mini"><div class="progress-fill-mini" style="width:${pct}%"></div></div>
                        <div class="progress-pct">${done}/${total} modules</div>
                    </div>
                    <div class="course-row-action">
                        <a href="course.html?id=${e.course_id}">Open</a>
                    </div>
                </div>`;
        }).join('');
    }

    // ─── Quiz Results ────────────────────────────────────────────────────────
    function renderResults(resultList) {
        const container = document.getElementById('quizResultsList');
        if (!resultList.length) return;

        container.innerHTML = resultList.slice(0, 8).map(r => {
            const passed = r.passed;
            const pct = r.percentage ?? 0;
            const date = r.completed_at ? new Date(r.completed_at).toLocaleDateString() : '';
            return `
                <div class="result-row">
                    <div class="result-badge ${passed ? 'passed' : 'failed'}">${passed ? '✓' : '✗'}</div>
                    <div class="result-info">
                        <div class="result-title">${r.course_title || r.quiz_title || 'Quiz'}</div>
                        <div class="result-meta">${date}${r.time_spent_seconds ? ' · ' + formatTime(r.time_spent_seconds) : ''}</div>
                    </div>
                    <div class="result-score" style="color:${passed ? 'var(--success)' : 'var(--danger)'}">${Math.round(pct)}%</div>
                </div>`;
        }).join('');
    }

    // ─── Certificates ────────────────────────────────────────────────────────
    let allCerts = [];

    function renderCertificates(certList) {
        allCerts = certList;
        const container = document.getElementById('certsList');
        if (!certList.length) return;

        container.innerHTML = certList.map((c, i) => {
            const date = c.issued_at ? new Date(c.issued_at).toLocaleDateString('en-US', { year:'numeric', month:'short', day:'numeric' }) : '';
            return `
                <div class="cert-row" data-index="${i}">
                    <span class="material-icons cert-icon">workspace_premium</span>
                    <div class="cert-info">
                        <div class="cert-info-title">${c.course_title}</div>
                        <div class="cert-info-date">Earned ${date} · Score: ${Math.round(c.score || 0)}%</div>
                    </div>
                    <button class="cert-view-btn" data-index="${i}">View</button>
                </div>`;
        }).join('');

        container.querySelectorAll('.cert-view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                showCertModal(allCerts[parseInt(btn.dataset.index)]);
            });
        });
        container.querySelectorAll('.cert-row').forEach(row => {
            row.addEventListener('click', () => {
                showCertModal(allCerts[parseInt(row.dataset.index)]);
            });
        });
    }

    // ─── Certificate Modal ───────────────────────────────────────────────────
    function setupCertModal() {
        document.getElementById('closeCertModal').addEventListener('click', hideCertModal);
        document.getElementById('certModal').addEventListener('click', e => {
            if (e.target === document.getElementById('certModal')) hideCertModal();
        });
    }

    function showCertModal(cert) {
        if (!cert) return;
        const u = JSON.parse(localStorage.getItem('currentUser') || '{}');
        document.getElementById('certUserName').textContent = u.name || u.username || u.user_id || 'User';
        document.getElementById('certCourseName').textContent = cert.course_title;
        document.getElementById('certScore').textContent = `${Math.round(cert.score || 0)}%`;
        document.getElementById('certDate').textContent = cert.issued_at
            ? new Date(cert.issued_at).toLocaleDateString('en-US', { year:'numeric', month:'long', day:'numeric' })
            : '—';
        document.getElementById('certIdText').textContent = `Certificate ID: ${cert.id}`;
        document.getElementById('certModal').classList.remove('hidden');
    }

    function hideCertModal() {
        document.getElementById('certModal').classList.add('hidden');
    }

    // ─── Helpers ─────────────────────────────────────────────────────────────
    function formatTime(s) {
        const m = Math.floor(s / 60);
        const sec = s % 60;
        return `${m}:${sec.toString().padStart(2, '0')}`;
    }

    // ─── Boot ────────────────────────────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', init);
})();