/**
 * Course Detail — Two-mode page:
 *   1. Overview (course info + module list)
 *   2. Learning View (full-screen reader + AI tutor + sidebar nav)
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
        this.aiMessages = [];

        if (!this.courseId) { window.location.href = 'courses.html'; return; }
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
        // Theme
        document.getElementById('themeToggle').addEventListener('click', () => {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
            localStorage.setItem('edu_theme', isDark ? 'light' : 'dark');
            document.querySelector('#themeToggle .material-icons').textContent = isDark ? 'dark_mode' : 'light_mode';
        });

        // Overview actions
        document.getElementById('heroActionBtn').addEventListener('click', () => this.handleHeroAction());

        // Learning view actions
        document.getElementById('lvBackBtn').addEventListener('click', () => this.closeLearningView());
        document.getElementById('lvSidebarToggle').addEventListener('click', () => this.toggleSidebar());
        document.getElementById('lvAiToggle').addEventListener('click', () => this.toggleAiPanel());
        document.getElementById('lvAiClose').addEventListener('click', () => this.toggleAiPanel(false));
        document.getElementById('lvCompleteBtn').addEventListener('click', () => this.completeCurrentModule());
        document.getElementById('lvPrevBtn').addEventListener('click', () => this.navigateModule(-1));
        document.getElementById('lvNextBtn').addEventListener('click', () => this.navigateModule(1));
        document.getElementById('lvBookmarkBtn').addEventListener('click', () => this.toggleBookmark());

        // AI Chat
        document.getElementById('lvAiSendBtn').addEventListener('click', () => this.sendAiMessage());
        document.getElementById('lvAiInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') this.sendAiMessage();
        });
        document.querySelectorAll('.lv-quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.getElementById('lvAiInput').value = btn.dataset.prompt;
                this.sendAiMessage();
            });
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (this.activeModuleIndex < 0) return;
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
            if (e.key === 'ArrowLeft') this.navigateModule(-1);
            if (e.key === 'ArrowRight') this.navigateModule(1);
            if (e.key === 'Escape') this.closeLearningView();
        });
    }

    setUserName() {
        const u = AUTH.getUser();
        const name = (u && (u.name || u.username)) || 'User';
        document.getElementById('userName').textContent = name;
    }

    /* ══════════════════════════════════════════════════════════
       DATA
       ══════════════════════════════════════════════════════════ */

    async loadData() {
        try {
            const [courseRes, enrollRes, progressRes] = await Promise.all([
                AUTH.fetch(`/api/courses/${this.courseId}`),
                AUTH.fetch(`/api/enrollments/${this.userId}/${this.courseId}`),
                AUTH.fetch(`/api/module-progress/${this.userId}/${this.courseId}`)
            ]);
            this.course = await courseRes.json();
            this.enrollment = (await enrollRes.json()).enrollment;
            this.moduleProgress = (await progressRes.json()).modules || [];
        } catch (err) {
            console.error('Error loading course:', err);
        }
    }

    getProgressMap() {
        const map = {};
        this.moduleProgress.forEach(mp => { map[mp.id] = mp; });
        return map;
    }

    getCompletionPct() {
        const total = (this.course?.modules || []).length;
        const completed = this.moduleProgress.filter(m => m.progress_status === 'completed').length;
        return total > 0 ? Math.round(completed / total * 100) : 0;
    }

    /* ══════════════════════════════════════════════════════════
       OVERVIEW RENDERING
       ══════════════════════════════════════════════════════════ */

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
        this.renderModuleList();
        this.renderAssessmentCta();
    }

    renderProgress() {
        const pct = this.getCompletionPct();
        const circumference = 2 * Math.PI * 42;
        const offset = circumference - (pct / 100) * circumference;
        const ringFill = document.getElementById('ringFill');
        ringFill.style.strokeDasharray = circumference;
        ringFill.style.strokeDashoffset = offset;
        ringFill.classList.toggle('complete', pct >= 100);
        document.getElementById('ringText').textContent = `${pct}%`;
    }

    renderHeroAction() {
        const btn = document.getElementById('heroActionBtn');
        if (!this.enrollment) {
            btn.textContent = 'Enroll Now'; btn.className = 'hero-action-btn';
        } else if (this.enrollment.status === 'completed') {
            btn.textContent = '✓ Completed'; btn.className = 'hero-action-btn completed';
        } else {
            btn.textContent = 'Continue Learning'; btn.className = 'hero-action-btn enrolled';
        }
    }

    renderModuleList() {
        const list = document.getElementById('moduleList');
        const modules = this.course.modules || [];
        const progressMap = this.getProgressMap();

        list.innerHTML = modules.map((mod, idx) => {
            const p = progressMap[mod.id];
            const status = p?.progress_status || 'not_started';
            let iconClass = '', iconContent = idx + 1;
            if (status === 'completed') { iconClass = 'completed'; iconContent = '<span class="material-icons" style="font-size:18px">check</span>'; }
            else if (status === 'in_progress') { iconClass = 'in-progress'; }

            return `
            <div class="module-item" data-index="${idx}" data-module-id="${mod.id}">
                <div class="module-status-icon ${iconClass}">${iconContent}</div>
                <div class="module-info">
                    <div class="module-title">${mod.title}</div>
                    <div class="module-desc">${mod.description || ''}</div>
                </div>
                <div class="module-duration"><span class="material-icons">schedule</span>${mod.duration_minutes || 30}m</div>
                <span class="material-icons module-open-icon">chevron_right</span>
            </div>`;
        }).join('');

        list.querySelectorAll('.module-item').forEach(item => {
            item.addEventListener('click', () => this.openModule(parseInt(item.dataset.index)));
        });
    }

    renderAssessmentCta() {
        const cta = document.getElementById('assessmentCta');
        const btn = document.getElementById('heroAssessmentBtn');
        const pct = this.getCompletionPct();
        if (this.enrollment && pct >= 100) {
            cta.classList.remove('hidden');
            btn.href = `assessment.html?course_id=${this.courseId}`;
        } else if (this.enrollment) {
            // Show it dimmed if enrolled but not complete
            cta.classList.remove('hidden');
            btn.href = `assessment.html?course_id=${this.courseId}`;
        } else {
            cta.classList.add('hidden');
        }
    }

    /* ══════════════════════════════════════════════════════════
       LEARNING VIEW
       ══════════════════════════════════════════════════════════ */

    openModule(index) {
        if (!this.enrollment) {
            // Auto-enroll if clicking a module
            this.handleHeroAction();
            return;
        }
        const modules = this.course.modules || [];
        if (index < 0 || index >= modules.length) return;

        this.activeModuleIndex = index;

        // Switch to learning view
        document.getElementById('courseOverview').classList.add('hidden');
        document.getElementById('learningView').classList.remove('hidden');

        // Set sidebar course title
        document.getElementById('lvCourseTitle').textContent = this.course.title;

        this.renderLvSidebar();
        this.renderLvContent();
        this.updateLvNav();

        // Scroll content to top
        document.getElementById('lvContentScroll').scrollTop = 0;
    }

    closeLearningView() {
        document.getElementById('learningView').classList.add('hidden');
        document.getElementById('courseOverview').classList.remove('hidden');
        this.activeModuleIndex = -1;
        // Refresh overview data
        this.loadData().then(() => this.render());
    }

    /* ── Sidebar ── */
    toggleSidebar() {
        document.getElementById('lvSidebar').classList.toggle('collapsed');
    }

    renderLvSidebar() {
        const nav = document.getElementById('lvModuleNav');
        const modules = this.course.modules || [];
        const progressMap = this.getProgressMap();
        const pct = this.getCompletionPct();

        document.getElementById('lvProgressFill').style.width = `${pct}%`;

        nav.innerHTML = modules.map((mod, idx) => {
            const p = progressMap[mod.id];
            const status = p?.progress_status || 'not_started';
            let iconClass = '', iconContent = idx + 1;
            if (status === 'completed') { iconClass = 'completed'; iconContent = '<span class="material-icons" style="font-size:14px">check</span>'; }
            else if (status === 'in_progress') { iconClass = 'in-progress'; }

            return `
            <div class="lv-mod-item ${idx === this.activeModuleIndex ? 'active' : ''}" data-index="${idx}">
                <div class="lv-mod-icon ${iconClass}">${iconContent}</div>
                <span class="lv-mod-title">${mod.title}</span>
                <span class="lv-mod-dur">${mod.duration_minutes || 30}m</span>
            </div>`;
        }).join('');

        nav.querySelectorAll('.lv-mod-item').forEach(item => {
            item.addEventListener('click', () => {
                const idx = parseInt(item.dataset.index);
                this.activeModuleIndex = idx;
                this.renderLvSidebar();
                this.renderLvContent();
                this.updateLvNav();
                document.getElementById('lvContentScroll').scrollTop = 0;
            });
        });
    }

    /* ── Content ── */
    renderLvContent() {
        const modules = this.course.modules || [];
        const mod = modules[this.activeModuleIndex];
        if (!mod) return;

        // Label
        document.getElementById('lvModuleLabel').textContent =
            `Module ${this.activeModuleIndex + 1} of ${modules.length}`;

        // Article content
        const article = document.getElementById('lvArticle');
        if (mod.content && mod.content.trim().startsWith('<')) {
            article.innerHTML = mod.content;
        } else {
            article.innerHTML = `
                <h2>${mod.title}</h2>
                <p><strong>${mod.description || ''}</strong></p>
                <p>${mod.content || 'Content for this module is being developed. Use the AI tutor to learn about this topic.'}</p>
            `;
        }

        // Update complete button state
        const progressMap = this.getProgressMap();
        const p = progressMap[mod.id];
        const btn = document.getElementById('lvCompleteBtn');
        if (p?.progress_status === 'completed') {
            btn.innerHTML = '<span class="material-icons">check_circle</span> Completed';
            btn.classList.add('completed');
        } else {
            btn.innerHTML = '<span class="material-icons">check_circle</span> Mark Complete & Continue';
            btn.classList.remove('completed');
        }
    }

    /* ── Navigation ── */
    updateLvNav() {
        const modules = this.course.modules || [];
        const idx = this.activeModuleIndex;
        const prev = document.getElementById('lvPrevBtn');
        const next = document.getElementById('lvNextBtn');

        prev.disabled = idx <= 0;
        next.disabled = idx >= modules.length - 1;

        document.getElementById('lvPrevLabel').textContent = idx > 0 ? modules[idx - 1].title : '—';
        document.getElementById('lvNextLabel').textContent = idx < modules.length - 1 ? modules[idx + 1].title : '—';
    }

    navigateModule(delta) {
        const newIdx = this.activeModuleIndex + delta;
        const modules = this.course.modules || [];
        if (newIdx < 0 || newIdx >= modules.length) return;

        this.activeModuleIndex = newIdx;
        this.renderLvSidebar();
        this.renderLvContent();
        this.updateLvNav();
        document.getElementById('lvContentScroll').scrollTop = 0;
    }

    /* ── Module Completion ── */
    async completeCurrentModule() {
        const modules = this.course.modules || [];
        const mod = modules[this.activeModuleIndex];
        if (!mod) return;

        // Check if already completed
        const progressMap = this.getProgressMap();
        if (progressMap[mod.id]?.progress_status === 'completed') return;

        const btn = document.getElementById('lvCompleteBtn');
        btn.innerHTML = '<span class="material-icons">hourglass_top</span> Saving...';

        try {
            await AUTH.fetch('/api/module-progress', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: this.userId, module_id: mod.id,
                    course_id: this.courseId, status: 'completed', score: 100
                })
            });

            // Reload progress
            const progressRes = await AUTH.fetch(`/api/module-progress/${this.userId}/${this.courseId}`);
            this.moduleProgress = (await progressRes.json()).modules || [];

            // Reload enrollment
            const enrollRes = await AUTH.fetch(`/api/enrollments/${this.userId}/${this.courseId}`);
            this.enrollment = (await enrollRes.json()).enrollment;

            // Update UI
            this.renderLvSidebar();
            this.renderLvContent();

            // Auto-advance
            const nextIdx = this.activeModuleIndex + 1;
            if (nextIdx < modules.length) {
                setTimeout(() => this.navigateModule(1), 400);
            }
        } catch (err) {
            console.error('Error marking complete:', err);
            btn.innerHTML = '<span class="material-icons">error</span> Error — Try Again';
        }
    }

    /* ── Hero Action (enroll / continue) ── */
    async handleHeroAction() {
        if (!this.enrollment) {
            try {
                await AUTH.fetch(`/api/courses/${this.courseId}/enroll`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: this.userId })
                });
                await this.loadData();
                this.render();

                // Open first module automatically
                if (this.course.modules?.length > 0) {
                    this.openModule(0);
                }
            } catch (err) { console.error('Enrollment error:', err); }
        } else if (this.enrollment.status !== 'completed') {
            // Find first incomplete module
            const progressMap = this.getProgressMap();
            const modules = this.course.modules || [];
            for (let i = 0; i < modules.length; i++) {
                const p = progressMap[modules[i].id];
                if (!p || p.progress_status !== 'completed') { this.openModule(i); return; }
            }
            // All complete? Open first
            this.openModule(0);
        }
    }

    /* ── Bookmark (simple visual toggle) ── */
    toggleBookmark() {
        const btn = document.getElementById('lvBookmarkBtn');
        const icon = btn.querySelector('.material-icons');
        if (icon.textContent === 'bookmark_border') {
            icon.textContent = 'bookmark';
            btn.title = 'Bookmarked';
        } else {
            icon.textContent = 'bookmark_border';
            btn.title = 'Bookmark';
        }
    }

    /* ══════════════════════════════════════════════════════════
       AI TUTOR PANEL
       ══════════════════════════════════════════════════════════ */

    toggleAiPanel(forceOpen) {
        const panel = document.getElementById('lvAiPanel');
        const btn = document.getElementById('lvAiToggle');
        const shouldOpen = forceOpen !== undefined ? forceOpen : panel.classList.contains('hidden');

        panel.classList.toggle('hidden', !shouldOpen);
        btn.classList.toggle('active', shouldOpen);

        if (shouldOpen) {
            document.getElementById('lvAiInput').focus();
        }
    }

    async sendAiMessage() {
        const input = document.getElementById('lvAiInput');
        const question = input.value.trim();
        if (!question) return;
        input.value = '';

        const messagesDiv = document.getElementById('lvAiMessages');
        const modules = this.course.modules || [];
        const mod = modules[this.activeModuleIndex];

        // Add user message
        messagesDiv.innerHTML += `
            <div class="lv-ai-msg user">
                <span class="material-icons lv-ai-avatar">person</span>
                <div class="lv-ai-bubble">${this.escapeHtml(question)}</div>
            </div>`;

        // Add thinking indicator
        const thinkingId = `thinking-${Date.now()}`;
        messagesDiv.innerHTML += `
            <div class="lv-ai-msg bot" id="${thinkingId}">
                <span class="material-icons lv-ai-avatar">smart_toy</span>
                <div class="lv-ai-bubble thinking"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
            </div>`;
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        try {
            const contextPrompt = `You are an AI tutor for the course "${this.course.title}" (${this.course.category}). The student is currently on the module "${mod?.title || 'unknown'}". ${mod?.description ? 'Module description: ' + mod.description + '.' : ''} Answer concisely and helpfully. If asked to quiz, provide 3 multiple-choice questions.`;

            const res = await AUTH.fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: `${contextPrompt}\n\nStudent question: ${question}`,
                    subject: this.course.category,
                    topic: mod?.title || this.course.title
                })
            });
            const data = await res.json();
            const answer = data.response || 'I couldn\'t generate a response. Please try again.';

            // Replace thinking with response
            const thinkingEl = document.getElementById(thinkingId);
            if (thinkingEl) {
                thinkingEl.querySelector('.lv-ai-bubble').classList.remove('thinking');
                thinkingEl.querySelector('.lv-ai-bubble').innerHTML = this.formatAiResponse(answer);
            }
        } catch (err) {
            const thinkingEl = document.getElementById(thinkingId);
            if (thinkingEl) {
                thinkingEl.querySelector('.lv-ai-bubble').classList.remove('thinking');
                thinkingEl.querySelector('.lv-ai-bubble').textContent = 'Sorry, I couldn\'t get a response. Please try again.';
            }
        }

        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    formatAiResponse(text) {
        // Basic markdown-like formatting
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code style="background:var(--surface-hover);padding:1px 4px;border-radius:3px;font-size:.84rem">$1</code>')
            .replace(/\n/g, '<br>');
    }
}

// Launch
document.addEventListener('DOMContentLoaded', () => new CourseDetail());
