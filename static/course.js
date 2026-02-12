/**
 * Course Detail Page — loads a single course, shows modules, handles progress & enrollment
 */

class CourseDetail {
    constructor() {
        if (!window.AUTH || !AUTH.requireAuth()) return;
        this.courseId = new URLSearchParams(window.location.search).get('id');
        this.userId = AUTH.getUserId();
        this.course = null;
        this.enrollment = null;
        this.moduleProgress = [];
        this.activeModuleIndex = -1;

        if (!this.courseId) {
            window.location.href = 'courses.html';
            return;
        }
        this.init();
    }

    async init() {
        this.applyTheme();
        this.bindEvents();
        this.setUserName();
        await this.loadData();
        this.render();
    }

    /* ── Theme ── */
    applyTheme() {
        const saved = localStorage.getItem('edu_theme');
        if (saved === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
    }

    /* ── Events ── */
    bindEvents() {
        document.getElementById('themeToggle').addEventListener('click', () => {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
            localStorage.setItem('edu_theme', isDark ? 'light' : 'dark');
            document.querySelector('#themeToggle .material-icons').textContent = isDark ? 'dark_mode' : 'light_mode';
        });

        document.getElementById('heroActionBtn').addEventListener('click', () => this.handleHeroAction());
        document.getElementById('viewerClose').addEventListener('click', () => this.closeViewer());
        document.getElementById('viewerComplete').addEventListener('click', () => this.completeCurrentModule());
        document.getElementById('viewerPrev').addEventListener('click', () => this.navigateModule(-1));
        document.getElementById('viewerNext').addEventListener('click', () => this.navigateModule(1));
        document.getElementById('aiAskBtn').addEventListener('click', () => this.askAI());
        document.getElementById('aiQuestion').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') this.askAI();
        });
    }

    setUserName() {
        const u = AUTH.getUser();
        const name = (u && (u.name || u.username)) || 'User';
        document.getElementById('userName').textContent = name;
    }

    /* ── Data ── */
    async loadData() {
        try {
            const [courseRes, enrollRes, progressRes] = await Promise.all([
                AUTH.fetch(`/api/courses/${this.courseId}`),
                AUTH.fetch(`/api/enrollments/${this.userId}/${this.courseId}`),
                AUTH.fetch(`/api/module-progress/${this.userId}/${this.courseId}`)
            ]);

            this.course = await courseRes.json();
            const enrollData = await enrollRes.json();
            this.enrollment = enrollData.enrollment;
            const progressData = await progressRes.json();
            this.moduleProgress = progressData.modules || [];
        } catch (err) {
            console.error('Error loading course:', err);
        }
    }

    /* ── Render ── */
    render() {
        if (!this.course || !this.course.title) {
            document.getElementById('heroTitle').textContent = 'Course not found';
            return;
        }

        const c = this.course;
        document.title = `Edu Assist Pro - ${c.title}`;
        document.getElementById('heroIcon').textContent = c.icon || '📋';
        document.getElementById('heroCategory').textContent = c.category || '';
        document.getElementById('heroTitle').textContent = c.title;
        document.getElementById('heroDescription').textContent = c.description || '';
        document.getElementById('heroDuration').textContent = c.duration_hours || 0;
        document.getElementById('heroModules').textContent = (c.modules || []).length;
        document.getElementById('heroDifficulty').textContent = c.difficulty || 'Beginner';

        this.renderProgress();
        this.renderHeroAction();
        this.renderModules();
    }

    renderProgress() {
        const total = (this.course.modules || []).length;
        const completed = this.moduleProgress.filter(m => m.progress_status === 'completed').length;
        const pct = total > 0 ? Math.round(completed / total * 100) : 0;

        // Ring
        const circumference = 2 * Math.PI * 42; // r=42
        const offset = circumference - (pct / 100) * circumference;
        const ringFill = document.getElementById('ringFill');
        ringFill.style.strokeDasharray = circumference;
        ringFill.style.strokeDashoffset = offset;
        if (pct >= 100) ringFill.classList.add('complete');
        else ringFill.classList.remove('complete');

        document.getElementById('ringText').textContent = `${pct}%`;
    }

    renderHeroAction() {
        const btn = document.getElementById('heroActionBtn');
        const assessBtn = document.getElementById('heroAssessmentBtn');
        if (!this.enrollment) {
            btn.textContent = 'Enroll Now';
            btn.className = 'hero-action-btn';
            assessBtn.classList.add('hidden');
        } else if (this.enrollment.status === 'completed') {
            btn.textContent = '✓ Completed';
            btn.className = 'hero-action-btn completed';
            assessBtn.classList.remove('hidden');
            assessBtn.href = `assessment.html?course_id=${this.courseId}`;
        } else {
            btn.textContent = 'Continue Learning';
            btn.className = 'hero-action-btn enrolled';
            assessBtn.classList.remove('hidden');
            assessBtn.href = `assessment.html?course_id=${this.courseId}`;
        }
    }

    renderModules() {
        const list = document.getElementById('moduleList');
        const modules = this.course.modules || [];

        // Merge progress data
        const progressMap = {};
        this.moduleProgress.forEach(mp => { progressMap[mp.id] = mp; });

        list.innerHTML = modules.map((mod, idx) => {
            const progress = progressMap[mod.id];
            const status = progress?.progress_status || 'not_started';
            const isActive = idx === this.activeModuleIndex;

            let iconClass = '';
            let iconContent = idx + 1;
            if (status === 'completed') {
                iconClass = 'completed';
                iconContent = '<span class="material-icons" style="font-size:18px">check</span>';
            } else if (status === 'in_progress') {
                iconClass = 'in-progress';
            }

            return `
            <div class="module-item ${isActive ? 'active' : ''}" data-index="${idx}" data-module-id="${mod.id}">
                <div class="module-status-icon ${iconClass}">${iconContent}</div>
                <div class="module-info">
                    <div class="module-title">${mod.title}</div>
                    <div class="module-desc">${mod.description || ''}</div>
                </div>
                <div class="module-duration">
                    <span class="material-icons">schedule</span>${mod.duration_minutes || 30}m
                </div>
            </div>`;
        }).join('');

        // Bind clicks
        list.querySelectorAll('.module-item').forEach(item => {
            item.addEventListener('click', () => {
                const idx = parseInt(item.dataset.index);
                this.openModule(idx);
            });
        });
    }

    /* ── Module Viewer ── */
    openModule(index) {
        if (!this.enrollment) return; // Must be enrolled
        const modules = this.course.modules || [];
        if (index < 0 || index >= modules.length) return;

        this.activeModuleIndex = index;
        const mod = modules[index];

        document.getElementById('viewerTitle').textContent = mod.title;
        document.getElementById('viewerBody').innerHTML = `
            <p><strong>${mod.description || ''}</strong></p>
            <br>
            <p>${mod.content || 'Content for this module is being developed. Use the AI assistant below to learn about this topic.'}</p>
        `;

        document.getElementById('moduleViewer').classList.remove('hidden');
        document.getElementById('viewerPrev').disabled = index === 0;
        document.getElementById('viewerNext').disabled = index === modules.length - 1;

        // Highlight active
        this.renderModules();

        // Scroll viewer into view
        document.getElementById('moduleViewer').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    closeViewer() {
        document.getElementById('moduleViewer').classList.add('hidden');
        this.activeModuleIndex = -1;
        this.renderModules();
    }

    navigateModule(delta) {
        const newIdx = this.activeModuleIndex + delta;
        this.openModule(newIdx);
    }

    async completeCurrentModule() {
        const modules = this.course.modules || [];
        if (this.activeModuleIndex < 0) return;
        const mod = modules[this.activeModuleIndex];

        try {
            await AUTH.fetch('/api/module-progress', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: this.userId,
                    module_id: mod.id,
                    course_id: this.courseId,
                    status: 'completed',
                    score: 100
                })
            });

            // Reload progress
            const progressRes = await AUTH.fetch(`/api/module-progress/${this.userId}/${this.courseId}`);
            const progressData = await progressRes.json();
            this.moduleProgress = progressData.modules || [];

            // Reload enrollment
            const enrollRes = await AUTH.fetch(`/api/enrollments/${this.userId}/${this.courseId}`);
            const enrollData = await enrollRes.json();
            this.enrollment = enrollData.enrollment;

            this.renderProgress();
            this.renderHeroAction();
            this.renderModules();

            // Auto-advance to next module
            const nextIdx = this.activeModuleIndex + 1;
            if (nextIdx < modules.length) {
                this.openModule(nextIdx);
            } else {
                this.closeViewer();
            }
        } catch (err) {
            console.error('Error marking complete:', err);
        }
    }

    /* ── Hero Action ── */
    async handleHeroAction() {
        if (!this.enrollment) {
            // Enroll
            try {
                await AUTH.fetch(`/api/courses/${this.courseId}/enroll`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: this.userId })
                });
                await this.loadData();
                this.render();
            } catch (err) {
                console.error('Enrollment error:', err);
            }
        } else if (this.enrollment.status !== 'completed') {
            // Find first incomplete module
            const progressMap = {};
            this.moduleProgress.forEach(mp => { progressMap[mp.id] = mp; });
            const modules = this.course.modules || [];
            for (let i = 0; i < modules.length; i++) {
                const p = progressMap[modules[i].id];
                if (!p || p.progress_status !== 'completed') {
                    this.openModule(i);
                    return;
                }
            }
        }
    }

    /* ── AI Q&A ── */
    async askAI() {
        const input = document.getElementById('aiQuestion');
        const question = input.value.trim();
        if (!question) return;

        const responseDiv = document.getElementById('aiResponse');
        const responseText = document.getElementById('aiResponseText');
        responseDiv.classList.remove('hidden');
        responseText.textContent = 'Thinking...';

        try {
            const res = await AUTH.fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: `Regarding the course "${this.course.title}" (${this.course.category}): ${question}`,
                    subject: this.course.category,
                    topic: this.course.title
                })
            });
            const data = await res.json();
            responseText.textContent = data.response || 'No response received.';
        } catch (err) {
            responseText.textContent = 'Error getting AI response. Please try again.';
        }

        input.value = '';
    }
}

document.addEventListener('DOMContentLoaded', () => new CourseDetail());
