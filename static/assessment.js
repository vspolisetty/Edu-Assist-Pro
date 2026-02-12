/**
 * Edu Assist Pro — Assessment Engine
 * Handles quiz loading, timer, navigation, submission, results & certificates.
 */
(function () {
    'use strict';

    // ─── Config ──────────────────────────────────────────────────────────────
    const API = '';  // relative
    const CIRCLE_CIRCUMFERENCE = 2 * Math.PI * 58; // r=58 on the SVG ring

    // ─── State ───────────────────────────────────────────────────────────────
    let courseId = null;
    let quiz = null;           // full quiz object from API
    let questions = [];        // quiz.questions
    let answers = {};          // { question_id: "selected option text" }
    let currentIndex = 0;
    let timerInterval = null;
    let secondsLeft = 0;
    let startedAt = null;      // Date
    let gradeResult = null;    // grade response

    // ─── DOM Cache ───────────────────────────────────────────────────────────
    const $ = id => document.getElementById(id);
    const screens = {
        start: $('quizStart'),
        active: $('quizActive'),
        results: $('quizResults')
    };

    // ─── Init ────────────────────────────────────────────────────────────────
    function init() {
        if (!window.AUTH || !AUTH.requireAuth()) return;
        const params = new URLSearchParams(window.location.search);
        courseId = params.get('course_id');
        if (!courseId) {
            alert('Missing course_id parameter.');
            window.location.href = 'courses.html';
            return;
        }
        setupTheme();
        setupUser();
        loadQuiz();
        bindEvents();
    }

    // ─── Theme ───────────────────────────────────────────────────────────────
    function setupTheme() {
        const saved = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', saved);
        const btn = $('themeToggle');
        btn.querySelector('.material-icons').textContent = saved === 'dark' ? 'light_mode' : 'dark_mode';
        btn.addEventListener('click', () => {
            const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            btn.querySelector('.material-icons').textContent = next === 'dark' ? 'light_mode' : 'dark_mode';
        });
    }

    function setupUser() {
        const user = JSON.parse(localStorage.getItem('currentUser') || '{}');
        const nameEl = $('userName');
        if (nameEl) nameEl.textContent = user.name || user.user_id || 'User';
    }

    // ─── Load Quiz ───────────────────────────────────────────────────────────
    async function loadQuiz() {
        showScreen('start');
        try {
            // First try GET (quiz already generated)
            let res = await AUTH.fetch(`${API}/api/quiz/${courseId}`);
            if (res.status === 404) {
                // Generate a new quiz
                $('startTitle').textContent = 'Generating Assessment...';
                $('startDesc').textContent = 'Our AI is crafting your assessment questions. This may take a moment.';
                res = await AUTH.fetch(`${API}/api/quiz/generate/${courseId}`, { method: 'POST' });
            }
            if (!res.ok) throw new Error(`Server error ${res.status}`);
            quiz = await res.json();
            questions = quiz.questions || [];
            renderStartScreen();
        } catch (err) {
            console.error('Quiz load error:', err);
            $('startTitle').textContent = 'Unable to Load Assessment';
            $('startDesc').textContent = err.message;
        }
    }

    function renderStartScreen() {
        $('startTitle').textContent = quiz.title || 'Assessment';
        $('startDesc').textContent = quiz.description || 'Test your knowledge with this AI-generated assessment.';
        $('startQuestionCount').textContent = questions.length;
        $('startTimeLimit').textContent = quiz.time_limit_minutes || 15;
        $('startPassingScore').textContent = quiz.passing_score || 70;
        $('backToCourse').href = `course.html?id=${courseId}`;
    }

    // ─── Bind Events ─────────────────────────────────────────────────────────
    function bindEvents() {
        $('btnStartQuiz').addEventListener('click', startQuiz);
        $('btnPrev').addEventListener('click', () => navigateTo(currentIndex - 1));
        $('btnNext').addEventListener('click', () => navigateTo(currentIndex + 1));
        $('btnSubmit').addEventListener('click', confirmSubmit);
        $('btnRetake').addEventListener('click', retakeQuiz);
        $('btnViewCert').addEventListener('click', showCertModal);
        $('closeCertModal').addEventListener('click', hideCertModal);
        $('certModal').addEventListener('click', e => { if (e.target === $('certModal')) hideCertModal(); });
    }

    // ─── Start Quiz ──────────────────────────────────────────────────────────
    function startQuiz() {
        if (!questions.length) return;
        currentIndex = 0;
        answers = {};
        startedAt = new Date();
        secondsLeft = (quiz.time_limit_minutes || 15) * 60;
        showScreen('active');
        buildNavButtons();
        renderQuestion();
        startTimer();
    }

    // ─── Timer ───────────────────────────────────────────────────────────────
    function startTimer() {
        updateTimerDisplay();
        timerInterval = setInterval(() => {
            secondsLeft--;
            updateTimerDisplay();
            if (secondsLeft <= 0) {
                clearInterval(timerInterval);
                submitQuiz();   // auto-submit
            }
        }, 1000);
    }

    function updateTimerDisplay() {
        const m = Math.floor(secondsLeft / 60);
        const s = secondsLeft % 60;
        $('timerDisplay').textContent = `${m}:${s.toString().padStart(2, '0')}`;
        const el = $('quizTimer');
        if (secondsLeft <= 60) el.style.color = 'var(--danger)';
        else el.style.color = '';
    }

    // ─── Navigation ──────────────────────────────────────────────────────────
    function buildNavButtons() {
        const nav = $('questionNav');
        nav.innerHTML = '';
        questions.forEach((_, i) => {
            const btn = document.createElement('button');
            btn.className = 'q-nav-btn';
            btn.textContent = i + 1;
            btn.addEventListener('click', () => navigateTo(i));
            nav.appendChild(btn);
        });
    }

    function navigateTo(idx) {
        if (idx < 0 || idx >= questions.length) return;
        currentIndex = idx;
        renderQuestion();
    }

    function renderQuestion() {
        const q = questions[currentIndex];
        $('currentQ').textContent = currentIndex + 1;
        $('totalQ').textContent = questions.length;
        $('progressFill').style.width = `${((currentIndex + 1) / questions.length) * 100}%`;

        // Type badge
        const typeBadge = $('questionTypeBadge');
        typeBadge.textContent = q.question_type === 'true_false' ? 'True / False' : 'Multiple Choice';

        // Question text
        $('questionText').textContent = q.question_text;

        // Options
        const list = $('optionsList');
        list.innerHTML = '';
        const letters = ['A', 'B', 'C', 'D', 'E', 'F'];
        (q.options || []).forEach((opt, i) => {
            const btn = document.createElement('button');
            btn.className = 'option-btn' + (answers[q.id] === opt ? ' selected' : '');
            btn.innerHTML = `<span class="option-letter">${letters[i] || i + 1}</span><span class="option-text">${opt}</span>`;
            btn.addEventListener('click', () => selectOption(q.id, opt));
            list.appendChild(btn);
        });

        // Nav highlight
        document.querySelectorAll('.q-nav-btn').forEach((b, i) => {
            b.classList.toggle('active', i === currentIndex);
            b.classList.toggle('answered', !!answers[questions[i].id] && i !== currentIndex);
        });

        // Prev/Next/Submit visibility
        $('btnPrev').style.visibility = currentIndex > 0 ? 'visible' : 'hidden';
        if (currentIndex === questions.length - 1) {
            $('btnNext').classList.add('hidden');
            $('btnSubmit').classList.remove('hidden');
        } else {
            $('btnNext').classList.remove('hidden');
            $('btnSubmit').classList.add('hidden');
        }
    }

    function selectOption(questionId, optionText) {
        answers[questionId] = optionText;
        renderQuestion();
    }

    // ─── Submit ──────────────────────────────────────────────────────────────
    function confirmSubmit() {
        const answered = Object.keys(answers).length;
        const total = questions.length;
        const msg = answered < total
            ? `You've answered ${answered} of ${total} questions. Unanswered questions will be marked incorrect. Submit now?`
            : 'Submit your assessment?';
        if (confirm(msg)) submitQuiz();
    }

    async function submitQuiz() {
        clearInterval(timerInterval);
        const elapsed = startedAt ? Math.round((new Date() - startedAt) / 1000) : 0;
        const userId = AUTH.getUserId();

        // Show loading state
        showScreen('results');
        $('resultsTitle').textContent = 'Grading...';
        $('resultsSubtitle').textContent = 'Please wait while we grade your assessment.';

        try {
            const res = await AUTH.fetch(`${API}/api/quiz/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    quiz_id: quiz.id,
                    answers: answers,
                    time_spent_seconds: elapsed
                })
            });
            if (!res.ok) throw new Error(`Server error ${res.status}`);
            gradeResult = await res.json();
            renderResults();
        } catch (err) {
            console.error('Submit error:', err);
            $('resultsTitle').textContent = 'Submission Failed';
            $('resultsSubtitle').textContent = err.message;
        }
    }

    // ─── Results ─────────────────────────────────────────────────────────────
    function renderResults() {
        const r = gradeResult;
        const pct = r.percentage || 0;
        const passed = r.passed;

        // Header
        $('resultsIcon').textContent = passed ? '🎉' : '📝';
        $('resultsTitle').textContent = passed ? 'Congratulations!' : 'Assessment Complete';
        $('resultsSubtitle').textContent = passed
            ? 'You passed the assessment!'
            : 'Keep studying and try again.';

        // Score ring
        const fill = $('scoreRingFill');
        const offset = CIRCLE_CIRCUMFERENCE - (pct / 100) * CIRCLE_CIRCUMFERENCE;
        fill.style.strokeDasharray = CIRCLE_CIRCUMFERENCE;
        setTimeout(() => { fill.style.strokeDashoffset = offset; }, 50);
        fill.classList.remove('passed', 'failed');
        fill.classList.add(passed ? 'passed' : 'failed');
        $('scoreText').textContent = `${Math.round(pct)}%`;

        // Score details
        $('scoreValue').textContent = `${r.score}/${r.total_points}`;
        $('passingValue').textContent = `${r.passing_score}%`;
        $('timeValue').textContent = formatTime(r.time_spent_seconds || 0);
        $('statusValue').textContent = passed ? '✅ Passed' : '❌ Failed';
        $('statusValue').style.color = passed ? 'var(--success)' : 'var(--danger)';

        // Certificate banner
        const banner = $('certificateBanner');
        if (r.certificate) {
            banner.classList.remove('hidden');
            $('certCourseTitle').textContent = r.certificate.course_title || quiz.title;
        } else {
            banner.classList.add('hidden');
        }

        // Answer review
        renderReview(r.results || []);
    }

    function renderReview(results) {
        const list = $('reviewList');
        list.innerHTML = '';
        results.forEach((r, i) => {
            const q = questions.find(q => q.id === r.question_id) || {};
            const div = document.createElement('div');
            div.className = `review-item ${r.is_correct ? 'correct' : 'incorrect'}`;
            div.innerHTML = `
                <div class="review-q">${i + 1}. ${q.question_text || 'Question'}</div>
                <div class="review-answer">Your answer: <strong>${r.user_answer || '(not answered)'}</strong></div>
                ${!r.is_correct ? `<div class="review-answer">Correct answer: <strong>${r.correct_answer}</strong></div>` : ''}
                ${r.explanation ? `<div class="review-explanation">${r.explanation}</div>` : ''}
            `;
            list.appendChild(div);
        });
    }

    // ─── Certificate Modal ───────────────────────────────────────────────────
    function showCertModal() {
        if (!gradeResult || !gradeResult.certificate) return;
        const c = gradeResult.certificate;
        const user = JSON.parse(localStorage.getItem('currentUser') || '{}');
        $('certUserName').textContent = user.name || user.user_id || 'User';
        $('certCourseName').textContent = c.course_title || quiz.title;
        $('certScore').textContent = `${Math.round(gradeResult.percentage)}%`;
        $('certDate').textContent = new Date(c.issued_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        $('certId').textContent = `Certificate ID: ${c.certificate_id}`;
        $('certModal').classList.remove('hidden');
    }
    function hideCertModal() { $('certModal').classList.add('hidden'); }

    // ─── Retake ──────────────────────────────────────────────────────────────
    async function retakeQuiz() {
        gradeResult = null;
        // Delete existing quiz so a fresh one is generated
        // For now, just reload the page to re-generate
        window.location.reload();
    }

    // ─── Helpers ─────────────────────────────────────────────────────────────
    function showScreen(name) {
        Object.entries(screens).forEach(([k, el]) => {
            if (el) el.classList.toggle('hidden', k !== name);
        });
    }

    function formatTime(secs) {
        const m = Math.floor(secs / 60);
        const s = secs % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    }

    // ─── Boot ────────────────────────────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', init);
})();
