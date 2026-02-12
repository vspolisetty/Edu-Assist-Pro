/**
 * Two-Factor Authentication — Frontend Controller
 * Handles method selection, code entry, verification, and timer
 */
(function () {
    'use strict';

    // ─── State ──────────────────────────────────────────────────────────────
    let state = {
        tempToken: '',
        challengeId: '',
        currentMethod: '',
        availableMethods: [],
        userPreview: {},
        timerInterval: null,
        timerSeconds: 300,
    };

    // ─── DOM references ─────────────────────────────────────────────────────
    const $stepMethod = document.getElementById('stepMethodSelect');
    const $stepCode = document.getElementById('stepCodeEntry');
    const $stepSuccess = document.getElementById('stepSuccess');
    const $methodGrid = document.getElementById('methodGrid');
    const $username = document.getElementById('twofaUsername');
    const $selectedIcon = document.getElementById('selectedMethodIcon');
    const $selectedLabel = document.getElementById('selectedMethodLabel');
    const $instructions = document.getElementById('twofaInstructions');
    const $demoHint = document.getElementById('demoHint');
    const $demoHintText = document.getElementById('demoHintText');
    const $codeForm = document.getElementById('codeForm');
    const $verifyBtn = document.getElementById('verifyBtn');
    const $resendBtn = document.getElementById('resendBtn');
    const $changeMethodBtn = document.getElementById('changeMethodBtn');
    const $timerValue = document.getElementById('timerValue');
    const $codeTimer = document.getElementById('codeTimer');
    const digits = [
        document.getElementById('digit1'),
        document.getElementById('digit2'),
        document.getElementById('digit3'),
        document.getElementById('digit4'),
        document.getElementById('digit5'),
        document.getElementById('digit6'),
    ];

    // ─── Init ───────────────────────────────────────────────────────────────
    function init() {
        setupTheme();

        // Read 2FA data from sessionStorage (set by login.js)
        const data = sessionStorage.getItem('twofa_data');
        if (!data) {
            // No 2FA data — redirect to login
            window.location.href = 'login.html';
            return;
        }

        const parsed = JSON.parse(data);
        state.tempToken = parsed.temp_token;
        state.challengeId = parsed.challenge_id;
        state.currentMethod = parsed.method;
        state.availableMethods = parsed.available_methods || [];
        state.userPreview = parsed.user_preview || {};

        $username.textContent = state.userPreview.name || state.userPreview.username || '—';

        // Render method cards
        renderMethodGrid();

        // Set up code entry
        setupCodeInputs();
        setupEventListeners();

        // If we already have a method + challenge, go straight to code entry
        if (state.challengeId && state.currentMethod) {
            showCodeEntry(
                state.currentMethod,
                parsed.instructions || '',
                parsed.demo_hint || ''
            );
        }
    }

    // ─── Method Grid ────────────────────────────────────────────────────────
    function renderMethodGrid() {
        $methodGrid.innerHTML = '';
        state.availableMethods.forEach(function (m) {
            const card = document.createElement('div');
            card.className = 'method-card';
            card.setAttribute('data-method', m.id);
            card.innerHTML = `
                <div class="method-icon"><span class="material-icons">${m.icon}</span></div>
                <div class="method-name">${m.label}</div>
                <div class="method-desc">${m.description}</div>
            `;
            card.addEventListener('click', function () {
                selectMethod(m.id);
            });
            $methodGrid.appendChild(card);
        });
    }

    // ─── Select Method ──────────────────────────────────────────────────────
    async function selectMethod(methodId) {
        try {
            // Request a new challenge for this method
            const res = await fetch('/api/auth/2fa/send-code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    temp_token: state.tempToken,
                    method: methodId,
                }),
            });

            if (!res.ok) {
                const err = await res.json().catch(function () { return {}; });
                alert(err.detail || 'Failed to send verification code');
                if (res.status === 401) window.location.href = 'login.html';
                return;
            }

            const data = await res.json();
            state.challengeId = data.challenge_id;
            state.currentMethod = methodId;

            showCodeEntry(methodId, data.instructions, data.demo_hint || '');
        } catch (err) {
            console.error('Error selecting method:', err);
            alert('Network error. Please try again.');
        }
    }

    // ─── Show Code Entry Step ───────────────────────────────────────────────
    function showCodeEntry(methodId, instructions, demoHint) {
        const method = state.availableMethods.find(function (m) { return m.id === methodId; });

        $selectedIcon.textContent = method ? method.icon : 'lock';
        $selectedLabel.textContent = method ? method.label : 'Enter Verification Code';
        $instructions.textContent = instructions || (method ? method.instructions : '');

        if (demoHint) {
            $demoHint.style.display = 'flex';
            $demoHintText.textContent = demoHint;
        } else {
            $demoHint.style.display = 'none';
        }

        // Clear code inputs
        digits.forEach(function (d) {
            d.value = '';
            d.classList.remove('filled', 'error');
        });

        // Switch steps
        $stepMethod.classList.add('hidden');
        $stepCode.classList.remove('hidden');
        $stepSuccess.classList.add('hidden');

        // Focus first digit
        setTimeout(function () { digits[0].focus(); }, 100);

        // Start timer
        startTimer(300);
    }

    // ─── Code Inputs ────────────────────────────────────────────────────────
    function setupCodeInputs() {
        digits.forEach(function (input, idx) {
            input.addEventListener('input', function (e) {
                const val = e.target.value.replace(/[^0-9]/g, '');
                e.target.value = val;

                if (val) {
                    e.target.classList.add('filled');
                    // Auto-advance
                    if (idx < 5) digits[idx + 1].focus();
                } else {
                    e.target.classList.remove('filled');
                }

                // Auto-submit when all 6 digits entered
                if (getCode().length === 6) {
                    setTimeout(function () { submitCode(); }, 150);
                }
            });

            input.addEventListener('keydown', function (e) {
                if (e.key === 'Backspace' && !e.target.value && idx > 0) {
                    digits[idx - 1].focus();
                    digits[idx - 1].value = '';
                    digits[idx - 1].classList.remove('filled');
                }
                if (e.key === 'ArrowLeft' && idx > 0) digits[idx - 1].focus();
                if (e.key === 'ArrowRight' && idx < 5) digits[idx + 1].focus();
            });

            // Handle paste
            input.addEventListener('paste', function (e) {
                e.preventDefault();
                const pasteData = (e.clipboardData || window.clipboardData).getData('text').replace(/[^0-9]/g, '');
                for (var i = 0; i < 6 && i < pasteData.length; i++) {
                    digits[i].value = pasteData[i];
                    digits[i].classList.add('filled');
                }
                if (pasteData.length >= 6) {
                    digits[5].focus();
                    setTimeout(function () { submitCode(); }, 150);
                } else if (pasteData.length > 0) {
                    digits[Math.min(pasteData.length, 5)].focus();
                }
            });
        });
    }

    function getCode() {
        return digits.map(function (d) { return d.value; }).join('');
    }

    // ─── Submit Code ────────────────────────────────────────────────────────
    async function submitCode() {
        const code = getCode();
        if (code.length !== 6) return;

        $verifyBtn.classList.add('loading');

        try {
            const res = await fetch('/api/auth/2fa/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    temp_token: state.tempToken,
                    challenge_id: state.challengeId,
                    code: code,
                }),
            });

            if (!res.ok) {
                const err = await res.json().catch(function () { return {}; });
                showCodeError(err.detail || 'Invalid code. Please try again.');
                return;
            }

            const data = await res.json();

            // Success! Store token and user
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('currentUser', JSON.stringify(data.user));

            // Clean up
            sessionStorage.removeItem('twofa_data');
            stopTimer();

            // Show success
            showSuccess();
        } catch (err) {
            console.error('Verification error:', err);
            showCodeError('Network error. Please try again.');
        } finally {
            $verifyBtn.classList.remove('loading');
        }
    }

    function showCodeError(message) {
        digits.forEach(function (d) { d.classList.add('error'); });
        setTimeout(function () {
            digits.forEach(function (d) { d.classList.remove('error'); });
        }, 600);

        // Show error message below timer
        var existing = document.querySelector('.twofa-error');
        if (existing) existing.remove();

        var errDiv = document.createElement('div');
        errDiv.className = 'error-message twofa-error';
        errDiv.style.textAlign = 'center';
        errDiv.style.marginBottom = '12px';
        errDiv.innerHTML = '<span class="material-icons" style="font-size:16px">error</span> ' + message;
        $verifyBtn.parentNode.insertBefore(errDiv, $verifyBtn);

        setTimeout(function () {
            if (errDiv.parentNode) errDiv.remove();
        }, 5000);

        // Clear and refocus
        digits.forEach(function (d) { d.value = ''; d.classList.remove('filled'); });
        digits[0].focus();
    }

    // ─── Success ────────────────────────────────────────────────────────────
    function showSuccess() {
        $stepCode.classList.add('hidden');
        $stepSuccess.classList.remove('hidden');

        setTimeout(function () {
            window.location.href = 'dashboard.html';
        }, 1500);
    }

    // ─── Timer ──────────────────────────────────────────────────────────────
    function startTimer(seconds) {
        stopTimer();
        state.timerSeconds = seconds;
        updateTimerDisplay();

        state.timerInterval = setInterval(function () {
            state.timerSeconds--;
            updateTimerDisplay();

            if (state.timerSeconds <= 60) {
                $codeTimer.classList.add('expiring');
            }

            if (state.timerSeconds <= 0) {
                stopTimer();
                $timerValue.textContent = 'Expired';
                $verifyBtn.disabled = true;
                $verifyBtn.querySelector('.btn-text').textContent = 'Code Expired';
            }
        }, 1000);
    }

    function stopTimer() {
        if (state.timerInterval) {
            clearInterval(state.timerInterval);
            state.timerInterval = null;
        }
    }

    function updateTimerDisplay() {
        var m = Math.floor(state.timerSeconds / 60);
        var s = state.timerSeconds % 60;
        $timerValue.textContent = m + ':' + (s < 10 ? '0' : '') + s;
    }

    // ─── Event Listeners ────────────────────────────────────────────────────
    function setupEventListeners() {
        $codeForm.addEventListener('submit', function (e) {
            e.preventDefault();
            submitCode();
        });

        $resendBtn.addEventListener('click', function () {
            selectMethod(state.currentMethod);
        });

        $changeMethodBtn.addEventListener('click', function () {
            stopTimer();
            $stepCode.classList.add('hidden');
            $stepMethod.classList.remove('hidden');
        });
    }

    // ─── Theme ──────────────────────────────────────────────────────────────
    function setupTheme() {
        var saved = localStorage.getItem('theme') || 'light';
        document.body.className = saved + '-theme';

        var toggle = document.getElementById('theme-toggle');
        var icon = toggle.querySelector('.material-icons');
        icon.textContent = saved === 'dark' ? 'dark_mode' : 'light_mode';

        toggle.addEventListener('click', function () {
            var current = document.body.className.includes('dark') ? 'dark' : 'light';
            var next = current === 'dark' ? 'light' : 'dark';
            document.body.className = next + '-theme';
            icon.textContent = next === 'dark' ? 'dark_mode' : 'light_mode';
            localStorage.setItem('theme', next);
        });
    }

    // ─── Start ──────────────────────────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', init);
})();
