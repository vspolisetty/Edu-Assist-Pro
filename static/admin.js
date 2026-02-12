/**
 * Edu Assist Pro — Admin Panel
 * User management, role editing, audit log viewer
 */
(function () {
    'use strict';

    // ─── Auth Guard ──────────────────────────────────────────────────────────
    if (!window.AUTH || !AUTH.requireRole('admin', 'manager')) return;

    // ─── State ───────────────────────────────────────────────────────────────
    let users = [];
    let auditLog = [];
    let reportData = { team: null, scores: null, compliance: null };
    let securityData = { stats: null, requestLog: [] };
    let twofaData = { stats: null };
    let currentFilter = 'all';
    let searchQuery = '';
    let editingUserId = null; // null = adding new user
    let reqLogMethodFilter = 'all';
    let reqLogSearchQuery = '';

    const $ = id => document.getElementById(id);
    const currentUserRole = AUTH.getRole();

    // ─── Init ────────────────────────────────────────────────────────────────
    async function init() {
        setupTheme();
        bindEvents();
        await loadData();
        render();
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

    // ─── Events ──────────────────────────────────────────────────────────────
    function bindEvents() {
        // Tabs
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => switchTab(tab.dataset.tab));
        });

        // Search
        $('userSearch').addEventListener('input', e => {
            searchQuery = e.target.value.toLowerCase().trim();
            renderUsersTable();
        });

        // Filter chips
        document.querySelectorAll('.filter-chips .chip').forEach(chip => {
            chip.addEventListener('click', () => {
                document.querySelectorAll('.filter-chips .chip').forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
                currentFilter = chip.dataset.role;
                renderUsersTable();
            });
        });

        // Add user button
        $('addUserBtn').addEventListener('click', () => openModal(null));

        // Modal close / cancel
        $('modalClose').addEventListener('click', closeModal);
        $('modalCancel').addEventListener('click', closeModal);
        $('editUserModal').addEventListener('click', e => {
            if (e.target === $('editUserModal')) closeModal();
        });

        // Form submit
        $('editUserForm').addEventListener('submit', handleFormSubmit);

        // Only admin can add/edit users
        if (currentUserRole !== 'admin') {
            $('addUserBtn').style.display = 'none';
        }
    }

    // ─── Data ────────────────────────────────────────────────────────────────
    async function loadData() {
        const [usersData, auditData, teamData, scoreData, complianceData, secStats, secLog, tfaStats] = await Promise.all([
            AUTH.fetchJSON('/api/admin/users'),
            currentUserRole === 'admin' ? AUTH.fetchJSON('/api/admin/audit-log?limit=100') : Promise.resolve(null),
            AUTH.fetchJSON('/api/reports/team-overview'),
            AUTH.fetchJSON('/api/reports/score-distribution'),
            AUTH.fetchJSON('/api/reports/compliance'),
            currentUserRole === 'admin' ? AUTH.fetchJSON('/api/admin/security/stats') : Promise.resolve(null),
            currentUserRole === 'admin' ? AUTH.fetchJSON('/api/admin/security/request-log?limit=100') : Promise.resolve(null),
            AUTH.fetchJSON('/api/admin/2fa/stats'),
        ]);

        users = usersData?.users || [];
        auditLog = auditData?.log || [];
        reportData.team = teamData;
        reportData.scores = scoreData;
        reportData.compliance = complianceData;
        securityData.stats = secStats;
        securityData.requestLog = secLog?.log || [];
        twofaData.stats = tfaStats;
    }

    // ─── Tab Switching ───────────────────────────────────────────────────────
    function switchTab(tab) {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelector(`.tab[data-tab="${tab}"]`).classList.add('active');

        $('tabUsers').classList.toggle('hidden', tab !== 'users');
        $('tabReports').classList.toggle('hidden', tab !== 'reports');
        $('tabSecurity').classList.toggle('hidden', tab !== 'security');
        $('tabTwofa').classList.toggle('hidden', tab !== 'twofa');
        $('tabAudit').classList.toggle('hidden', tab !== 'audit');
    }

    // ─── Render ──────────────────────────────────────────────────────────────
    function render() {
        renderStats();
        renderUsersTable();
        renderAuditTable();
        renderReports();
        renderSecurityTab();
        renderTwofaTab();
    }

    function renderStats() {
        $('statTotal').textContent = users.length;
        $('statTrainees').textContent = users.filter(u => u.role === 'trainee').length;
        $('statManagers').textContent = users.filter(u => u.role === 'manager').length;
        $('statAdmins').textContent = users.filter(u => u.role === 'admin').length;
    }

    function getFilteredUsers() {
        return users.filter(u => {
            if (currentFilter !== 'all' && u.role !== currentFilter) return false;
            if (searchQuery) {
                const hay = `${u.name} ${u.username} ${u.email} ${u.department}`.toLowerCase();
                if (!hay.includes(searchQuery)) return false;
            }
            return true;
        });
    }

    function renderUsersTable() {
        const filtered = getFilteredUsers();
        const tbody = $('usersTableBody');

        if (!filtered.length) {
            tbody.innerHTML = '<tr><td colspan="7" class="loading-cell">No users found</td></tr>';
            return;
        }

        tbody.innerHTML = filtered.map(u => {
            const initials = (u.name || u.username || '?').split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
            const joinDate = u.created_at ? new Date(u.created_at).toLocaleDateString() : '—';
            const isCurrentUser = u.id === AUTH.getUserId();

            return `
            <tr>
                <td>
                    <div class="user-cell">
                        <div class="user-avatar">${initials}</div>
                        <div>
                            <div class="user-cell-name">${escHtml(u.name || u.username)}</div>
                            <div class="user-cell-username">@${escHtml(u.username)}</div>
                        </div>
                    </div>
                </td>
                <td>${escHtml(u.email || '—')}</td>
                <td><span class="role-badge ${u.role}">${u.role}</span></td>
                <td>${escHtml(u.department || '—')}</td>
                <td><span class="status-badge ${u.is_active ? 'active' : 'inactive'}">${u.is_active ? 'Active' : 'Inactive'}</span></td>
                <td>${joinDate}</td>
                <td>
                    <div class="action-btns">
                        ${currentUserRole === 'admin' ? `
                        <button class="btn-icon" title="Edit" onclick="ADMIN.editUser('${u.id}')">
                            <span class="material-icons">edit</span>
                        </button>
                        ${!isCurrentUser ? `
                        <button class="btn-icon" title="${u.is_active ? 'Deactivate' : 'Reactivate'}" onclick="ADMIN.toggleUser('${u.id}', ${u.is_active})">
                            <span class="material-icons">${u.is_active ? 'person_off' : 'person'}</span>
                        </button>` : ''}
                        ` : ''}
                    </div>
                </td>
            </tr>`;
        }).join('');
    }

    function renderAuditTable() {
        const tbody = $('auditTableBody');

        if (!auditLog.length) {
            tbody.innerHTML = '<tr><td colspan="5" class="loading-cell">No audit entries</td></tr>';
            return;
        }

        tbody.innerHTML = auditLog.map(entry => {
            const ts = entry.created_at ? new Date(entry.created_at).toLocaleString() : '—';
            const actionClass = ['login', 'login_failed', 'register', 'password_change'].includes(entry.action)
                ? entry.action : 'default';

            return `
            <tr>
                <td>${ts}</td>
                <td style="font-family: monospace; font-size:.8rem">${(entry.user_id || '—').slice(0, 8)}…</td>
                <td><span class="action-badge ${actionClass}">${escHtml(entry.action)}</span></td>
                <td>${escHtml(entry.detail || '—')}</td>
                <td>${escHtml(entry.ip_address || '—')}</td>
            </tr>`;
        }).join('');
    }

    // ─── Reports ─────────────────────────────────────────────────────────────
    function renderReports() {
        renderTeamReport();
        renderScoreReport();
        renderComplianceReport();
    }

    function renderTeamReport() {
        const d = reportData.team;
        if (!d) { $('teamStats').textContent = 'No data'; return; }

        $('teamStats').innerHTML = `
            <div class="rstat"><div class="rstat-value">${d.total_users}</div><div class="rstat-label">Users</div></div>
            <div class="rstat"><div class="rstat-value">${d.total_enrollments}</div><div class="rstat-label">Enrollments</div></div>
            <div class="rstat"><div class="rstat-value">${d.total_completions}</div><div class="rstat-label">Completions</div></div>
            <div class="rstat"><div class="rstat-value">${d.completion_rate}%</div><div class="rstat-label">Rate</div></div>
        `;

        const tbody = $('teamTableBody');
        if (!d.members.length) { tbody.innerHTML = '<tr><td colspan="6" class="loading-cell">No data</td></tr>'; return; }
        tbody.innerHTML = d.members.map(m => `
            <tr>
                <td><strong>${escHtml(m.name)}</strong></td>
                <td>${escHtml(m.department)}</td>
                <td>${m.enrolled}</td>
                <td>${m.completed}</td>
                <td>${m.completion_rate}%</td>
                <td>${m.avg_score}</td>
            </tr>
        `).join('');
    }

    function renderScoreReport() {
        const d = reportData.scores;
        if (!d) { $('scoreStats').textContent = 'No data'; return; }

        $('scoreStats').innerHTML = `
            <div class="rstat"><div class="rstat-value">${d.total_attempts}</div><div class="rstat-label">Attempts</div></div>
            <div class="rstat"><div class="rstat-value">${d.pass_count}</div><div class="rstat-label">Passed</div></div>
            <div class="rstat"><div class="rstat-value">${d.fail_count}</div><div class="rstat-label">Failed</div></div>
            <div class="rstat"><div class="rstat-value">${d.pass_rate}%</div><div class="rstat-label">Pass Rate</div></div>
        `;

        // Bar chart
        const bars = $('scoreBars');
        const maxCount = Math.max(1, ...Object.values(d.distribution));
        bars.innerHTML = Object.entries(d.distribution).map(([range, count]) => {
            const pct = (count / maxCount) * 100;
            return `<div class="score-bar">
                <div class="score-bar-count">${count}</div>
                <div class="score-bar-fill" style="height:${Math.max(pct, 3)}%"></div>
                <div class="score-bar-label">${range.split('-')[0]}</div>
            </div>`;
        }).join('');

        // Per-course table
        const tbody = $('courseScoreBody');
        if (!d.per_course.length) { tbody.innerHTML = '<tr><td colspan="6" class="loading-cell">No quiz data</td></tr>'; return; }
        tbody.innerHTML = d.per_course.map(c => `
            <tr>
                <td><strong>${escHtml(c.course)}</strong></td>
                <td>${c.attempts}</td>
                <td>${c.avg_score}</td>
                <td>${c.min_score}</td>
                <td>${c.max_score}</td>
                <td>${c.pass_rate}%</td>
            </tr>
        `).join('');
    }

    function renderComplianceReport() {
        const d = reportData.compliance;
        if (!d) { $('complianceStats').textContent = 'No data'; return; }

        $('complianceStats').innerHTML = `
            <div class="rstat"><div class="rstat-value">${d.mandatory_course_count}</div><div class="rstat-label">Courses</div></div>
            <div class="rstat"><div class="rstat-value">${d.total_users}</div><div class="rstat-label">Users</div></div>
            <div class="rstat"><div class="rstat-value">${d.compliant_users}</div><div class="rstat-label">Compliant</div></div>
            <div class="rstat"><div class="rstat-value">${d.compliance_rate}%</div><div class="rstat-label">Rate</div></div>
        `;

        // Build header
        const courseTitles = d.users.length ? d.users[0].courses.map(c => c.course_title) : [];
        $('complianceHead').innerHTML = '<tr><th>Name</th><th>Dept</th><th>Status</th>' +
            courseTitles.map(t => `<th>${escHtml(t.length > 20 ? t.slice(0,18) + '…' : t)}</th>`).join('') + '</tr>';

        $('complianceBody').innerHTML = d.users.map(u => {
            const cells = u.courses.map(c => {
                const cls = c.status === 'completed' ? 'completed' : c.status === 'in_progress' ? 'in_progress' : 'not_enrolled';
                const label = c.status === 'not_enrolled' ? 'Not Started' : c.status === 'completed' ? 'Done' : `${c.progress}%`;
                return `<td><span class="compliance-status ${cls}">${label}</span></td>`;
            }).join('');
            return `<tr>
                <td><strong>${escHtml(u.name)}</strong></td>
                <td>${escHtml(u.department)}</td>
                <td><span class="${u.compliant ? 'compliance-yes' : 'compliance-no'}">${u.compliant ? '✓ Compliant' : '✗ Incomplete'}</span></td>
                ${cells}
            </tr>`;
        }).join('');
    }

    // ─── CSV Export ──────────────────────────────────────────────────────────
    async function exportCSV(type) {
        const url = `/api/reports/export/${type}`;
        try {
            const res = await AUTH.fetch(url);
            if (!res.ok) throw new Error('Export failed');
            const blob = await res.blob();
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `${type}_report.csv`;
            a.click();
            URL.revokeObjectURL(a.href);
            showToast('CSV downloaded', 'success');
        } catch (err) {
            showToast(err.message, 'error');
        }
    }

    // ─── Modal ───────────────────────────────────────────────────────────────
    function openModal(userId) {
        editingUserId = userId;
        const modal = $('editUserModal');
        modal.classList.remove('hidden');

        if (userId) {
            // Edit existing user
            $('modalTitle').textContent = 'Edit User';
            $('modalSave').textContent = 'Save Changes';
            const u = users.find(u => u.id === userId);
            if (u) {
                $('formUsername').value = u.username;
                $('formUsername').disabled = true;
                $('formName').value = u.name || '';
                $('formEmail').value = u.email || '';
                $('formPassword').value = '';
                $('formRole').value = u.role || 'trainee';
                $('formDepartment').value = u.department || '';
            }
        } else {
            // Add new user
            $('modalTitle').textContent = 'Add New User';
            $('modalSave').textContent = 'Create User';
            $('formUsername').value = '';
            $('formUsername').disabled = false;
            $('formName').value = '';
            $('formEmail').value = '';
            $('formPassword').value = '';
            $('formPassword').placeholder = 'Required';
            $('formRole').value = 'trainee';
            $('formDepartment').value = '';
        }
    }

    function closeModal() {
        $('editUserModal').classList.add('hidden');
        editingUserId = null;
    }

    async function handleFormSubmit(e) {
        e.preventDefault();

        const username = $('formUsername').value.trim();
        const name = $('formName').value.trim();
        const email = $('formEmail').value.trim();
        const password = $('formPassword').value;
        const role = $('formRole').value;
        const department = $('formDepartment').value.trim();

        try {
            if (editingUserId) {
                // Update existing user
                const body = { name, email, role, department };
                const res = await AUTH.fetch(`/api/admin/users/${editingUserId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body)
                });
                if (!res.ok) {
                    const err = await res.json().catch(() => ({}));
                    throw new Error(err.detail || 'Failed to update user');
                }
                showToast('User updated successfully', 'success');
            } else {
                // Create new user
                if (!password) {
                    showToast('Password is required for new users', 'error');
                    return;
                }
                const res = await AUTH.fetch('/api/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, name, email, password, role, department })
                });
                if (!res.ok) {
                    const err = await res.json().catch(() => ({}));
                    throw new Error(err.detail || 'Failed to create user');
                }
                showToast('User created successfully', 'success');
            }

            closeModal();
            await loadData();
            render();
        } catch (err) {
            showToast(err.message, 'error');
        }
    }

    // ─── Actions ─────────────────────────────────────────────────────────────
    async function editUser(userId) {
        openModal(userId);
    }

    async function toggleUser(userId, isActive) {
        const action = isActive ? 'deactivate' : 'reactivate';
        if (!confirm(`Are you sure you want to ${action} this user?`)) return;

        try {
            if (isActive) {
                // Deactivate = DELETE (soft delete)
                const res = await AUTH.fetch(`/api/admin/users/${userId}`, { method: 'DELETE' });
                if (!res.ok) throw new Error('Failed to deactivate');
            } else {
                // Reactivate = PUT is_active: true
                const res = await AUTH.fetch(`/api/admin/users/${userId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ is_active: true })
                });
                if (!res.ok) throw new Error('Failed to reactivate');
            }

            showToast(`User ${action}d successfully`, 'success');
            await loadData();
            render();
        } catch (err) {
            showToast(err.message, 'error');
        }
    }

    // ─── Security Tab ──────────────────────────────────────────────────────
    function renderSecurityTab() {
        renderSecurityStats();
        renderRequestLog();
        bindSecurityEvents();
    }

    function renderSecurityStats() {
        const s = securityData.stats;
        if (!s) return;
        $('secTotalReqs').textContent = s.total_requests_today;
        $('secFailedLogins').textContent = s.failed_logins_today;
        $('secForbidden').textContent = s.forbidden_attempts_today;
        $('secRateLimited').textContent = s.rate_limited_today;
        $('secUniqueIPs').textContent = s.unique_ips_today;
        $('secAvgMs').textContent = s.avg_response_ms + 'ms';
    }

    function renderRequestLog() {
        const tbody = $('requestLogBody');
        if (!tbody) return;

        let logs = securityData.requestLog;

        // Apply method filter
        if (reqLogMethodFilter !== 'all') {
            logs = logs.filter(l => l.method === reqLogMethodFilter);
        }
        // Apply path search
        if (reqLogSearchQuery) {
            logs = logs.filter(l => l.path.toLowerCase().includes(reqLogSearchQuery));
        }

        if (!logs.length) {
            tbody.innerHTML = '<tr><td colspan="7" class="loading-cell">No requests found</td></tr>';
            return;
        }

        tbody.innerHTML = logs.map(l => {
            const ts = l.created_at ? new Date(l.created_at).toLocaleTimeString() : '—';
            const statusCls = l.status < 300 ? 'ok' : l.status < 400 ? 'redirect' : l.status < 500 ? 'client' : 'server';
            return `
            <tr>
                <td>${ts}</td>
                <td><span class="method-badge ${l.method}">${l.method}</span></td>
                <td style="font-family:monospace;font-size:.78rem">${escHtml(l.path)}</td>
                <td><span class="status-badge ${statusCls}">${l.status}</span></td>
                <td>${escHtml(l.username || '—')}</td>
                <td style="font-family:monospace;font-size:.78rem">${escHtml(l.ip_address || '—')}</td>
                <td>${l.duration_ms ? l.duration_ms.toFixed(1) + 'ms' : '—'}</td>
            </tr>`;
        }).join('');
    }

    let _secEvtBound = false;
    function bindSecurityEvents() {
        if (_secEvtBound) return;
        _secEvtBound = true;

        // Method filter chips
        const methodChips = document.getElementById('methodChips');
        if (methodChips) {
            methodChips.querySelectorAll('.chip').forEach(chip => {
                chip.addEventListener('click', () => {
                    methodChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
                    chip.classList.add('active');
                    reqLogMethodFilter = chip.dataset.method;
                    renderRequestLog();
                });
            });
        }

        // Path search
        const searchInput = $('reqLogSearch');
        if (searchInput) {
            searchInput.addEventListener('input', e => {
                reqLogSearchQuery = e.target.value.toLowerCase().trim();
                renderRequestLog();
            });
        }
    }

    // ─── 2FA Tab ────────────────────────────────────────────────────────────
    function renderTwofaTab() {
        renderTwofaStats();
        renderTwofaUsers();
    }

    function renderTwofaStats() {
        const s = twofaData.stats;
        if (!s) return;
        $('twofaTotalUsers').textContent = s.total_users || 0;
        $('twofaEnabled').textContent = s.enabled_count || 0;
        $('twofaDisabled').textContent = s.disabled_count || 0;
        $('twofaAdoption').textContent = (s.adoption_rate || 0) + '%';
        $('twofaChallenges24h').textContent = s.challenges_last_24h || 0;

        const mb = s.method_breakdown || {};
        $('twofaCountAuth').textContent = (mb.authenticator || 0) + ' users';
        $('twofaCountSms').textContent = (mb.sms || 0) + ' users';
        $('twofaCountHw').textContent = (mb.hardware_key || 0) + ' users';
        $('twofaCountAdmin').textContent = (mb.contact_admin || 0) + ' users';
    }

    function renderTwofaUsers() {
        const tbody = $('twofaUsersBody');
        if (!tbody || !users.length) return;

        // We need to fetch 2FA settings per user — for now, build from stats
        // The users list + stats give us what we need
        const s = twofaData.stats;
        tbody.innerHTML = users.filter(u => u.is_active).map(u => {
            // We don't have per-user 2FA data in the table yet, so we'll make it dynamic
            return `
            <tr id="twofa-row-${u.id}">
                <td>
                    <div class="user-cell">
                        <div class="user-avatar">${(u.name || u.username || '?').split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()}</div>
                        <div>
                            <div class="user-cell-name">${escHtml(u.name || u.username)}</div>
                            <div class="user-cell-username">@${escHtml(u.username)}</div>
                        </div>
                    </div>
                </td>
                <td><span class="role-badge ${u.role}">${u.role}</span></td>
                <td class="twofa-status-cell" data-uid="${u.id}">
                    <span class="status-badge loading-2fa">Checking...</span>
                </td>
                <td class="twofa-method-cell" data-uid="${u.id}">—</td>
                <td class="twofa-action-cell" data-uid="${u.id}">
                    ${currentUserRole === 'admin' ? `
                    <button class="btn-icon btn-sm" title="Enable 2FA" onclick="ADMIN.enable2fa('${u.id}')">
                        <span class="material-icons">verified_user</span>
                    </button>
                    <button class="btn-icon btn-sm" title="Disable 2FA" onclick="ADMIN.disable2fa('${u.id}')">
                        <span class="material-icons">no_encryption</span>
                    </button>
                    ` : '—'}
                </td>
            </tr>`;
        }).join('');

        // Async-load 2FA status for each user
        loadUserTwofaStatuses();
    }

    async function loadUserTwofaStatuses() {
        // Fetch 2FA settings for each user using the admin's token
        for (const u of users.filter(u => u.is_active)) {
            try {
                // We use the 2fa settings endpoint to check each user
                // Since we only have a "get my own settings" endpoint, we'll use a simple approach:
                // Check if user has 2FA by looking at the twofa_settings table via admin endpoint
                const statusCell = document.querySelector(`.twofa-status-cell[data-uid="${u.id}"]`);
                const methodCell = document.querySelector(`.twofa-method-cell[data-uid="${u.id}"]`);
                if (!statusCell) continue;

                // For now, we'll query individually — in production, batch this
                const res = await AUTH.fetchJSON(`/api/admin/2fa/status/${u.id}`);
                if (res && res.is_enabled) {
                    statusCell.innerHTML = '<span class="status-badge active">Enabled</span>';
                    const methodLabels = { authenticator: 'Authenticator', sms: 'SMS OTP', hardware_key: 'Hardware Key', contact_admin: 'Admin Code' };
                    methodCell.textContent = methodLabels[res.preferred_method] || res.preferred_method;
                } else {
                    statusCell.innerHTML = '<span class="status-badge inactive">Disabled</span>';
                    methodCell.textContent = '—';
                }
            } catch (_) {
                const statusCell = document.querySelector(`.twofa-status-cell[data-uid="${u.id}"]`);
                if (statusCell) statusCell.innerHTML = '<span class="status-badge inactive">Disabled</span>';
            }
        }
    }

    async function enable2fa(userId) {
        const method = prompt('Choose 2FA method:\n• authenticator\n• sms\n• hardware_key\n• contact_admin', 'authenticator');
        if (!method) return;

        try {
            const res = await AUTH.fetch(`/api/admin/2fa/enable/${userId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ method })
            });
            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail || 'Failed to enable 2FA');
            }
            showToast('2FA enabled for user', 'success');
            await loadData();
            render();
        } catch (err) {
            showToast(err.message, 'error');
        }
    }

    async function disable2fa(userId) {
        if (!confirm('Disable 2FA for this user? They will only need a password to login.')) return;

        try {
            const res = await AUTH.fetch(`/api/admin/2fa/disable/${userId}`, { method: 'POST' });
            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail || 'Failed to disable 2FA');
            }
            showToast('2FA disabled for user', 'success');
            await loadData();
            render();
        } catch (err) {
            showToast(err.message, 'error');
        }
    }

    // ─── Helpers ─────────────────────────────────────────────────────────────
    function escHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('show'));
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // ─── Expose for inline onclick handlers ──────────────────────────────────
    window.ADMIN = { editUser, toggleUser, exportCSV, enable2fa, disable2fa };

    // ─── Start ───────────────────────────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', init);
})();
