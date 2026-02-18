/* ───────────────────────────────────────────────────────────
   Edu Assist Pro – Main Chat Application
   ─────────────────────────────────────────────────────────── */

class EduAssist {
    constructor() {
        this.checkAuthentication();
        this.currentSubject   = null;   // e.g. "Compliance Training"
        this.currentSubjectId = null;   // e.g. "compliance"
        this.currentTopic     = null;   // e.g. "Company Policies"
        this.subjects       = [];
        this.questionsData  = {};
        this.topicsData     = {};
        this.isRecording    = false;
        this.eli5Mode       = false;
        this.chatStarted    = false;

        // Time-tracking
        this.sessionStartTime = null;
        this.lastActivityTime = null;
        this.activityTimeout  = 5 * 60 * 1000;
        this.sessionTimer     = null;
        this.totalSessionTime = 0;

        this.init();
    }

    /* ── Auth gate ─────────────────────────────────────────── */
    checkAuthentication() {
        if (window.AUTH && !AUTH.isAuthenticated()) {
            window.location.href = 'login.html';
        }
    }

    setUserName() {
        const u  = JSON.parse(localStorage.getItem('currentUser') || '{}');
        const el = document.getElementById('userName');
        if (el) el.textContent = u.name || u.username || u.user_id || 'User';
    }

    /* ── Bootstrap ─────────────────────────────────────────── */
    async init() {
        await Promise.all([
            this.loadSubjects(),
            this.loadQuestions(),
            this.loadTopics()
        ]);
        this.setupEventListeners();
        this.setupTheme();
        this.setUserName();
        this.renderSubjects();
        this.renderTopicCards();
        this.renderQuestions();
        this.renderSubtopics();
        this.loadBookmarks();
        this.startTimeTracking();
    }

    /* ── Data loaders ──────────────────────────────────────── */
    async loadSubjects() {
        try {
            const r = await fetch('sidebar_data.json');
            this.subjects = await r.json();
        } catch (e) {
            console.error('Failed to load subjects:', e);
            this.subjects = [];
        }
    }
    async loadQuestions() {
        try {
            const r = await fetch('questions_data.json');
            this.questionsData = await r.json();
        } catch (e) {
            console.error('Failed to load questions:', e);
            this.questionsData = {};
        }
    }
    async loadTopics() {
        try {
            const r = await fetch('topics_data.json');
            this.topicsData = await r.json();
        } catch (e) {
            console.error('Failed to load topics:', e);
            this.topicsData = {};
        }
    }

    /* ── Event listeners ───────────────────────────────────── */
    setupEventListeners() {
        const $ = id => document.getElementById(id);

        // Theme toggle - handled by theme-manager.js
        $('send-btn')?.addEventListener('click', () => this.sendMessage());
        $('mic-btn')?.addEventListener('click', () => this.toggleRecording());
        $('clear-context-btn')?.addEventListener('click', () => this.clearContext());

        $('message-input')?.addEventListener('keypress', e => {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.sendMessage(); }
        });

        $('eli5-toggle')?.addEventListener('change', e => {
            this.eli5Mode = e.target.checked;
        });

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn =>
            btn.addEventListener('click', e => this.switchTab(e.target.dataset.tab))
        );

        // Quick-action buttons on welcome screen
        document.querySelectorAll('.quick-action-btn').forEach(btn =>
            btn.addEventListener('click', e => {
                const q = e.currentTarget.dataset.question;
                if (q) { $('message-input').value = q; this.sendMessage(); }
            })
        );

        // Delegated click for message actions
        document.addEventListener('click', e => {
            const btn = e.target.closest('.action-btn');
            if (btn) this.handleMessageAction(btn.title.toLowerCase(), btn);
        });
    }

    /* ════════════════════════════════════════════════════════
       WELCOME SCREEN  –  topic cards with images
       ════════════════════════════════════════════════════════ */
    renderTopicCards() {
        const grid = document.getElementById('topic-cards-grid');
        if (!grid) return;

        grid.innerHTML = this.subjects.map(s => `
            <div class="topic-card" data-sid="${s.id}">
                <div class="topic-card-img">
                    <img src="${s.image || ''}" alt="${s.name}" loading="lazy"
                         onerror="this.style.display='none'">
                    <span class="topic-card-emoji">${s.icon}</span>
                </div>
                <div class="topic-card-body">
                    <h4>${s.name}</h4>
                    <p>${s.description || ''}</p>
                    <span class="topic-card-meta">
                        <span class="material-icons" style="font-size:14px">menu_book</span>
                        ${s.topics.length} topics
                    </span>
                </div>
            </div>
        `).join('');

        grid.querySelectorAll('.topic-card').forEach(card => {
            card.addEventListener('click', () => {
                const s = this.subjects.find(x => x.id === card.dataset.sid);
                if (s) { this.selectTopic(s.name, s.topics[0]); this.expandSubject(s.id); }
            });
        });
    }

    /* ── Show / hide welcome ───────────────────────────────── */
    hideWelcome() {
        const el = document.getElementById('welcome-screen');
        if (el) el.style.display = 'none';
        this.chatStarted = true;
    }
    showWelcome() {
        const el = document.getElementById('welcome-screen');
        if (el) el.style.display = '';
        document.getElementById('chat-context-bar').style.display = 'none';
        this.chatStarted = false;
    }
    clearContext() {
        this.currentSubject = this.currentSubjectId = this.currentTopic = null;
        // Remove dynamic chat messages (keep the welcome div)
        const box = document.getElementById('chat-messages');
        [...box.children].forEach(c => { if (c.id !== 'welcome-screen') c.remove(); });
        this.showWelcome();
        document.querySelectorAll('.topic-item, .subject-header').forEach(el => el.classList.remove('active'));
        this.renderQuestions();
        this.renderSubtopics();
    }

    /* ════════════════════════════════════════════════════════
       LEFT SIDEBAR  –  modules & topics
       ════════════════════════════════════════════════════════ */
    renderSubjects() {
        const list = document.getElementById('subjects-list');
        if (!list) return;
        list.innerHTML = '';

        this.subjects.forEach(s => {
            const div = document.createElement('div');
            div.className = 'subject-item';
            div.innerHTML = `
                <div class="subject-header" data-subject="${s.id}">
                    <span class="subject-icon">${s.icon}</span>
                    <span class="subject-name">${s.name}</span>
                    <span class="material-icons expand-icon">expand_more</span>
                </div>
                <div class="topics-list" id="topics-${s.id}">
                    ${s.topics.map(t => `
                        <div class="topic-item" data-subject-name="${s.name}" data-subject-id="${s.id}" data-topic="${t}">
                            ${t}
                        </div>`).join('')}
                </div>`;
            list.appendChild(div);
        });

        list.querySelectorAll('.subject-header').forEach(h =>
            h.addEventListener('click', () => this.toggleSubject(h.dataset.subject))
        );
        list.querySelectorAll('.topic-item').forEach(ti =>
            ti.addEventListener('click', () =>
                this.selectTopic(ti.dataset.subjectName, ti.dataset.topic)
            )
        );
    }

    toggleSubject(id) {
        const tl = document.getElementById(`topics-${id}`);
        if (!tl) return;
        tl.classList.toggle('expanded');
        const icon = document.querySelector(`.subject-header[data-subject="${id}"] .expand-icon`);
        if (icon) icon.style.transform = tl.classList.contains('expanded') ? 'rotate(180deg)' : '';
    }
    expandSubject(id) {
        const tl = document.getElementById(`topics-${id}`);
        if (tl && !tl.classList.contains('expanded')) this.toggleSubject(id);
    }

    /* ── Select a topic ────────────────────────────────────── */
    selectTopic(subjectName, topic) {
        this.currentSubject = subjectName;
        this.currentTopic   = topic;
        const obj = this.subjects.find(s => s.name === subjectName);
        this.currentSubjectId = obj ? obj.id : null;

        // Context bar
        const bar = document.getElementById('chat-context-bar');
        if (bar) bar.style.display = 'flex';
        const cs = document.getElementById('context-subject');
        const ct = document.getElementById('context-topic');
        if (cs) cs.textContent = subjectName;
        if (ct) ct.textContent = topic;

        // Active highlights
        document.querySelectorAll('.topic-item').forEach(i => i.classList.remove('active'));
        document.querySelectorAll('.subject-header').forEach(h => h.classList.remove('active'));
        document.querySelector(`.topic-item[data-topic="${topic}"][data-subject-id="${this.currentSubjectId}"]`)?.classList.add('active');
        document.querySelector(`.subject-header[data-subject="${this.currentSubjectId}"]`)?.classList.add('active');

        this.renderQuestions();
        this.renderSubtopics();

        if (!this.chatStarted) {
            this.hideWelcome();
            this.addMessage('ai',
                `Great choice! You've selected **${subjectName}** › **${topic}**.\n\nI'm ready to help you learn about this module. What would you like to know?`);
        }

        // Track progress
        try {
            let p = JSON.parse(localStorage.getItem('userProgress') || '{}');
            if (!p[subjectName]) p[subjectName] = {};
            if (!p[subjectName][topic]) p[subjectName][topic] = { sessions: 0 };
            p[subjectName][topic].sessions++;
            p[subjectName][topic].lastStudied = new Date().toISOString();
            localStorage.setItem('userProgress', JSON.stringify(p));
        } catch (_) {}
    }

    /* Helper: subject name → id */
    _sid(name) {
        const s = this.subjects.find(x => x.name === name);
        return s ? s.id : null;
    }

    /* ════════════════════════════════════════════════════════
       RIGHT SIDEBAR
       ════════════════════════════════════════════════════════ */
    renderSubtopics() {
        const box = document.getElementById('topic-list');
        if (!box) return;
        const sid = this._sid(this.currentSubject);
        box.innerHTML = '';

        if (sid && this.topicsData[sid] && this.topicsData[sid][this.currentTopic]) {
            this.topicsData[sid][this.currentTopic].forEach((t, i) => {
                const d = document.createElement('div');
                d.className = 'topic-item-right';
                d.innerHTML = `<div class="topic-number">${i + 1}</div>
                    <div class="topic-content"><h4>${t}</h4><p>Click to explore</p></div>`;
                d.addEventListener('click', () => {
                    document.getElementById('message-input').value = `Tell me about ${t}`;
                    this.sendMessage();
                });
                box.appendChild(d);
            });
        } else {
            box.innerHTML = `<div class="empty-state">
                <span class="material-icons">library_books</span>
                <p>${this.currentTopic ? 'No subtopics yet' : 'Select a module to see subtopics'}</p></div>`;
        }
    }

    renderQuestions() {
        const box = document.getElementById('suggested-questions');
        if (!box) return;
        const sid = this._sid(this.currentSubject);
        box.innerHTML = '';

        if (sid && this.questionsData[sid] && this.questionsData[sid][this.currentTopic]) {
            this.questionsData[sid][this.currentTopic].forEach(q => {
                const b = document.createElement('button');
                b.className = 'question-btn';
                b.textContent = q;
                b.addEventListener('click', () => {
                    document.getElementById('message-input').value = q;
                    this.sendMessage();
                });
                box.appendChild(b);
            });
        } else {
            box.innerHTML = `<div class="empty-state">
                <span class="material-icons">help_outline</span>
                <p>${this.currentTopic ? 'No suggestions yet' : 'Select a module for suggestions'}</p></div>`;
        }
    }

    loadBookmarks() { this._refreshBookmarks(); }
    _refreshBookmarks() {
        const box = document.getElementById('bookmarks-list');
        if (!box) return;
        const bm = JSON.parse(localStorage.getItem('bookmarks') || '[]');
        if (!bm.length) {
            box.innerHTML = `<div class="empty-state">
                <span class="material-icons">bookmark_border</span>
                <p>No saved items yet</p></div>`;
            return;
        }
        box.innerHTML = bm.map(b => `
            <div class="bookmark-item">
                <p>${b.text.substring(0, 120)}${b.text.length > 120 ? '…' : ''}</p>
                <span class="bookmark-meta">${b.subject || ''} · ${new Date(b.date).toLocaleDateString()}</span>
            </div>`).join('');
    }

    /* ════════════════════════════════════════════════════════
       CHAT
       ════════════════════════════════════════════════════════ */
    sendMessage() {
        const input = document.getElementById('message-input');
        const msg = input.value.trim();
        if (!msg) return;
        if (!this.chatStarted) this.hideWelcome();
        input.value = '';
        this.addMessage('student', msg);
        this.trackChatActivity(msg);
        setTimeout(() => this.generateAIResponse(msg), 800);
    }

    addMessage(type, text) {
        const box  = document.getElementById('chat-messages');
        const div  = document.createElement('div');
        div.className = `message ${type}-message`;
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        if (type === 'ai') {
            div.innerHTML = `
                <div class="message-avatar"><span class="material-icons">smart_toy</span></div>
                <div class="message-content">
                    <div class="message-bubble">${this._fmt(text)}</div>
                    <div class="message-actions">
                        <button class="action-btn" title="Copy message"><span class="material-icons">content_copy</span></button>
                        <button class="action-btn" title="Save message"><span class="material-icons">bookmark</span></button>
                        <button class="action-btn" title="Like message"><span class="material-icons">thumb_up</span></button>
                    </div>
                </div>`;
        } else {
            div.innerHTML = `
                <div class="message-content">
                    <div class="message-bubble"><p>${text}</p></div>
                    <div class="message-time">${time}</div>
                </div>`;
        }

        box.appendChild(div);
        box.scrollTop = box.scrollHeight;
        if (type === 'student') this._addXP(5);
    }

    async generateAIResponse(userMsg) {
        this._showTyping();
        try {
            const body = JSON.stringify({
                message: userMsg,
                subject: this.currentSubject || 'General',
                topic:   this.currentTopic   || 'General',
                eli5_mode: this.eli5Mode,
                conversation_history: this._recentMsgs()
            });
            const opts = { method: 'POST', headers: { 'Content-Type': 'application/json' }, body };
            const res = await (window.AUTH ? AUTH.fetch('/api/chat', opts) : fetch('/api/chat', opts));
            this._hideTyping();
            if (!res.ok) throw new Error(res.status);
            const data = await res.json();
            let reply = data.response || "Sorry, I couldn't generate a response.";
            if (this.eli5Mode) reply += '\n\n🧠 *Simplified mode active*';
            this.addMessage('ai', reply);
        } catch (err) {
            console.error('AI error:', err);
            this._hideTyping();
            this.addMessage('ai',
                `I'm having trouble reaching the backend. Make sure the server is running on port 3000.\n\nIn the meantime, feel free to ask general questions about **${this.currentTopic || 'your training'}**!`);
        }
    }

    _recentMsgs() {
        return [...document.querySelectorAll('.message')].slice(-5).map(m => ({
            role: m.classList.contains('student-message') ? 'user' : 'assistant',
            content: m.querySelector('.message-bubble p')?.textContent || ''
        }));
    }

    _showTyping() {
        const d = document.createElement('div');
        d.className = 'message ai-message typing-indicator'; d.id = 'typing-indicator';
        d.innerHTML = `<div class="message-avatar"><span class="material-icons">smart_toy</span></div>
            <div class="message-content"><div class="message-bubble">
                <div class="typing-dots"><span></span><span></span><span></span></div>
            </div></div>`;
        const box = document.getElementById('chat-messages');
        box.appendChild(d); box.scrollTop = box.scrollHeight;
    }
    _hideTyping() { document.getElementById('typing-indicator')?.remove(); }

    _fmt(text) {
        let h = text
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/^[•\-]\s+(.+)$/gm, '<li>$1</li>')
            .replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');
        if (!h.startsWith('<')) h = '<p>' + h + '</p>';
        h = h.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');
        return h;
    }

    /* ── Message actions ───────────────────────────────────── */
    handleMessageAction(action, btn) {
        const txt = btn.closest('.message')?.querySelector('.message-bubble p')?.textContent || '';
        if (action.includes('copy'))  { navigator.clipboard.writeText(txt); this._toast('Copied!'); }
        if (action.includes('save'))  { this._bookmark(txt); btn.querySelector('.material-icons').textContent = 'bookmark_added'; this._toast('Saved!'); }
        if (action.includes('like'))  { btn.querySelector('.material-icons').textContent = 'thumb_up'; btn.style.color = 'var(--primary-color)'; this._toast('Liked!'); this._addXP(2); }
    }
    _bookmark(text) {
        const bm = JSON.parse(localStorage.getItem('bookmarks') || '[]');
        bm.push({ text, subject: this.currentSubject || 'General', topic: this.currentTopic || 'General', date: new Date().toISOString() });
        localStorage.setItem('bookmarks', JSON.stringify(bm));
        this._refreshBookmarks();
    }

    /* ── Tabs ──────────────────────────────────────────────── */
    switchTab(name) {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelector(`[data-tab="${name}"]`)?.classList.add('active');
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        document.getElementById(`${name}-panel`)?.classList.add('active');
    }

    /* ── Theme ─────────────────────────────────────────────── */
    setupTheme() {
        // Handled by theme-manager.js
    }
    setTheme(t) {
        // Handled by theme-manager.js
        if (window.ThemeManager) {
            window.ThemeManager.setTheme(t);
        }
    }
    toggleTheme() {
        // Handled by theme-manager.js
        if (window.ThemeManager) {
            window.ThemeManager.toggle();
        }
    }

    /* ── Voice (demo) ──────────────────────────────────────── */
    toggleRecording() {
        const btn = document.getElementById('mic-btn');
        if (!this.isRecording) {
            this.isRecording = true; btn.classList.add('recording');
            setTimeout(() => { if (this.isRecording) { this.isRecording = false; btn.classList.remove('recording'); document.getElementById('message-input').value = 'What are the key compliance requirements?'; } }, 3000);
        } else { this.isRecording = false; btn.classList.remove('recording'); }
    }

    /* ── XP / Toasts ───────────────────────────────────────── */
    _addXP(pts) {
        const xp = parseInt(localStorage.getItem('currentXP') || '0') + pts;
        localStorage.setItem('currentXP', String(xp));
        this._toast(`+${pts} XP`);
    }
    _toast(msg) {
        const t = document.createElement('div');
        t.textContent = msg;
        t.style.cssText = 'position:fixed;bottom:100px;right:24px;background:var(--surface-color);color:var(--text-color);padding:10px 18px;border-radius:8px;box-shadow:var(--shadow-elevated);border:1px solid var(--border-color);z-index:9999;font-size:14px;animation:slideInUp .3s ease';
        document.body.appendChild(t);
        setTimeout(() => { t.style.animation = 'slideOutDown .3s ease'; setTimeout(() => t.remove(), 300); }, 2000);
    }

    /* ── Activity tracking ─────────────────────────────────── */
    trackChatActivity(msg) {
        const subj = this.currentSubject || 'General';
        const topic = this.currentTopic || 'General';
        const title = /what|how/i.test(msg) ? 'Asked Question' : /help|explain/i.test(msg) ? 'Requested Help' : 'Chat';
        const desc  = msg.length > 50 ? msg.substring(0, 50) + '…' : msg;
        if (typeof DashboardManager !== 'undefined' && DashboardManager.trackActivity)
            DashboardManager.trackActivity('chat', title, desc, subj, topic);
        const a = JSON.parse(localStorage.getItem('userActivity') || '[]');
        a.unshift({ type: 'chat', title, description: desc, time: 'just now', timestamp: new Date().toISOString(), subject: subj, topic, icon: '💬' });
        if (a.length > 20) a.length = 20;
        localStorage.setItem('userActivity', JSON.stringify(a));
        if (typeof window.refreshDashboard === 'function') window.refreshDashboard();
    }

    /* ── Time tracking ─────────────────────────────────────── */
    startTimeTracking() {
        this.sessionStartTime = this.lastActivityTime = new Date();
        this.sessionTimer = setInterval(() => this._tick(), 1000);
        ['mousedown','mousemove','keypress','scroll','touchstart','click'].forEach(e =>
            document.addEventListener(e, () => { this.lastActivityTime = new Date(); }, true));
        this._saveSession('start');
        window.addEventListener('beforeunload', () => this._endTracking());
    }
    _tick() {
        if (new Date() - this.lastActivityTime < this.activityTimeout) {
            this.totalSessionTime += 1000;
            if (this.totalSessionTime % 10000 === 0) this._saveSession('update');
        }
    }
    _saveSession(action) {
        const ss = JSON.parse(localStorage.getItem('studySessions') || '[]');
        const today = new Date().toDateString();
        let ts = ss.find(s => s.date === today);
        if (!ts) { ts = { date: today, totalTime: 0, sessions: [] }; ss.push(ts); }
        if (action === 'start') ts.sessions.push({ startTime: this.sessionStartTime.toISOString(), endTime: null, duration: 0 });
        else if (action === 'end') {
            const l = ts.sessions[ts.sessions.length - 1];
            if (l && !l.endTime) { l.endTime = new Date().toISOString(); l.duration = this.totalSessionTime; ts.totalTime += this.totalSessionTime; }
        } else {
            const l = ts.sessions[ts.sessions.length - 1];
            if (l && !l.endTime) { l.duration = this.totalSessionTime; ts.totalTime = ts.sessions.filter(s => s.endTime).reduce((t, s) => t + s.duration, 0) + this.totalSessionTime; }
        }
        localStorage.setItem('studySessions', JSON.stringify(ss));
    }
    _endTracking() { if (this.sessionTimer) { clearInterval(this.sessionTimer); this.sessionTimer = null; } this._saveSession('end'); }
    static getTodayStudyTime() {
        const ss = JSON.parse(localStorage.getItem('studySessions') || '[]');
        const t = ss.find(s => s.date === new Date().toDateString());
        return t ? t.totalTime : 0;
    }
}

// ── Initialise ────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    window.eduAssistInstance = new EduAssist();
});

// Toast animations
(() => {
    const s = document.createElement('style');
    s.textContent = `
        @keyframes slideInUp  { from{transform:translateY(100%);opacity:0} to{transform:translateY(0);opacity:1} }
        @keyframes slideOutDown{from{transform:translateY(0);opacity:1}   to{transform:translateY(100%);opacity:0} }
    `;
    document.head.appendChild(s);
})();
