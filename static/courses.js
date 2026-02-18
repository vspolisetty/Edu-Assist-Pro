/**
 * Courses Page — Fetches courses from API, renders cards, handles filtering/search/enrollment
 */

class CoursesPage {
    constructor() {
        if (!window.AUTH || !AUTH.requireAuth()) return;
        this.courses = [];
        this.enrollments = {};
        this.userId = AUTH.getUserId();
        this.currentFilter = 'all';
        this.searchQuery = '';

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
        // Handled by theme-manager.js
    }

    /* ── Events ── */
    bindEvents() {
        // Theme toggle - handled by theme-manager.js

        // Search
        document.getElementById('searchInput').addEventListener('input', (e) => {
            this.searchQuery = e.target.value.toLowerCase().trim();
            this.render();
        });

        // Filter chips
        document.querySelectorAll('.chip').forEach(chip => {
            chip.addEventListener('click', () => {
                document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
                this.currentFilter = chip.dataset.filter;
                this.render();
            });
        });
    }

    setUserName() {
        const u = AUTH.getUser();
        const name = (u && (u.name || u.username)) || 'User';
        const el = document.getElementById('userName');
        if (el) el.textContent = name;
    }

    /* ── Data Loading ── */
    async loadData() {
        try {
            const [coursesRes, enrollmentsRes] = await Promise.all([
                AUTH.fetch('/api/courses'),
                AUTH.fetch(`/api/enrollments/${this.userId}`)
            ]);
            const coursesData = await coursesRes.json();
            const enrollmentsData = await enrollmentsRes.json();

            this.courses = coursesData.courses || [];
            // Map enrollments by course_id for quick lookup
            (enrollmentsData.enrollments || []).forEach(e => {
                this.enrollments[e.course_id] = e;
            });
        } catch (err) {
            console.error('Error loading courses:', err);
            this.courses = [];
        }
    }

    /* ── Filtering ── */
    getFilteredCourses() {
        return this.courses.filter(c => {
            // Category / mandatory filter
            if (this.currentFilter === 'mandatory') {
                if (!c.is_mandatory) return false;
            } else if (this.currentFilter !== 'all') {
                if (c.category !== this.currentFilter) return false;
            }
            // Search
            if (this.searchQuery) {
                const haystack = `${c.title} ${c.description} ${c.category}`.toLowerCase();
                if (!haystack.includes(this.searchQuery)) return false;
            }
            return true;
        });
    }

    /* ── Render ── */
    render() {
        const grid = document.getElementById('courseGrid');
        const empty = document.getElementById('emptyState');
        const loading = document.getElementById('loadingState');
        loading.classList.add('hidden');

        const filtered = this.getFilteredCourses();

        // Stats
        document.getElementById('totalCourses').textContent = this.courses.length;
        const enrolledCount = Object.keys(this.enrollments).length;
        const completedCount = Object.values(this.enrollments).filter(e => e.status === 'completed').length;
        document.getElementById('enrolledCount').textContent = enrolledCount;
        document.getElementById('completedCount').textContent = completedCount;

        if (filtered.length === 0) {
            grid.innerHTML = '';
            empty.classList.remove('hidden');
            return;
        }
        empty.classList.add('hidden');

        grid.innerHTML = filtered.map(course => this.renderCard(course)).join('');

        // Bind card clicks and buttons
        grid.querySelectorAll('.course-card').forEach(card => {
            const courseId = card.dataset.courseId;
            card.addEventListener('click', (e) => {
                // Don't navigate if clicking the action button
                if (e.target.closest('.card-action-btn')) return;
                window.location.href = `course.html?id=${courseId}`;
            });
        });

        grid.querySelectorAll('.card-action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const courseId = btn.dataset.courseId;
                const action = btn.dataset.action;
                if (action === 'enroll') this.enrollInCourse(courseId);
                else window.location.href = `course.html?id=${courseId}`;
            });
        });
    }

    renderCard(course) {
        const enrollment = this.enrollments[course.id];
        const progress = enrollment ? Math.round(enrollment.progress || 0) : 0;
        const isEnrolled = !!enrollment;
        const isCompleted = enrollment?.status === 'completed';

        let actionBtn = '';
        let progressBar = '';

        if (isCompleted) {
            progressBar = `
                <div class="progress-bar-container">
                    <div class="progress-label">Completed</div>
                    <div class="progress-track"><div class="progress-fill complete" style="width:100%"></div></div>
                </div>`;
            actionBtn = `<button class="card-action-btn btn-review" data-course-id="${course.id}" data-action="view">Review</button>`;
        } else if (isEnrolled) {
            progressBar = `
                <div class="progress-bar-container">
                    <div class="progress-label">${progress}% Complete</div>
                    <div class="progress-track"><div class="progress-fill" style="width:${progress}%"></div></div>
                </div>`;
            actionBtn = `<button class="card-action-btn btn-continue" data-course-id="${course.id}" data-action="view">Continue</button>`;
        } else {
            progressBar = `
                <div class="progress-bar-container">
                    <div class="progress-label">Not Started</div>
                    <div class="progress-track"><div class="progress-fill" style="width:0%"></div></div>
                </div>`;
            actionBtn = `<button class="card-action-btn btn-enroll" data-course-id="${course.id}" data-action="enroll">Enroll</button>`;
        }

        const mandatoryBadge = course.is_mandatory
            ? '<span class="mandatory-badge"><span class="material-icons" style="font-size:11px">priority_high</span>Required</span>'
            : '';

        const difficultyIcon = { Beginner: 'signal_cellular_alt_1_bar', Intermediate: 'signal_cellular_alt_2_bar', Advanced: 'signal_cellular_alt' }[course.difficulty] || 'signal_cellular_alt_1_bar';

        return `
        <div class="course-card" data-course-id="${course.id}">
            <div class="card-header">
                <div class="card-icon">${course.icon || '📋'}</div>
                <div class="card-title-area">
                    <div class="card-title">${course.title}</div>
                    <div class="card-category">${course.category}${mandatoryBadge}</div>
                </div>
            </div>
            <div class="card-body">
                <div class="card-description">${course.description || ''}</div>
            </div>
            <div class="card-meta">
                <div class="meta-item"><span class="material-icons">schedule</span>${course.duration_hours || 0}h</div>
                <div class="meta-item"><span class="material-icons">view_module</span>${course.module_count || 0} modules</div>
                <div class="meta-item"><span class="material-icons">${difficultyIcon}</span>${course.difficulty || 'Beginner'}</div>
            </div>
            <div class="card-footer">
                ${progressBar}
                ${actionBtn}
            </div>
        </div>`;
    }

    /* ── Enrollment ── */
    async enrollInCourse(courseId) {
        try {
            const res = await AUTH.fetch(`/api/courses/${courseId}/enroll`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: this.userId })
            });
            if (res.ok) {
                await this.loadData();
                this.render();
            }
        } catch (err) {
            console.error('Enrollment failed:', err);
        }
    }
}

// Launch
document.addEventListener('DOMContentLoaded', () => new CoursesPage());
