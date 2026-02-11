class DashboardManager {
    constructor() {
        this.currentUser = null;
        this.bookmarks = [];
        this.progressData = {};
        this.activityData = [];
        
        this.init();
    }
    
    async init() {
        this.checkAuthentication();
        this.loadUserData();
        this.setupEventListeners();
        this.setupTheme();
        this.loadBookmarks();
        this.loadProgressData();
        this.loadActivityData();
        this.renderDashboard();
        
        // Refresh stats when page becomes visible
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.refreshStats();
            }
        });
        
        // Refresh stats every 10 seconds
        setInterval(() => {
            this.refreshStats();
        }, 10000);
    }
    
    checkAuthentication() {
        const userData = localStorage.getItem('currentUser');
        if (!userData) {
            window.location.href = 'login.html';
            return;
        }
        
        this.currentUser = JSON.parse(userData);
    }
    
    loadUserData() {
        if (this.currentUser) {
            document.getElementById('user-name').textContent = this.currentUser.username;
            document.getElementById('welcome-username').textContent = this.currentUser.username;
        }
    }
    
    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // User menu
        const userButton = document.getElementById('user-button');
        const userMenu = document.getElementById('user-menu');
        
        userButton.addEventListener('click', (e) => {
            e.stopPropagation();
            userMenu.classList.toggle('open');
        });
        
        document.addEventListener('click', () => {
            userMenu.classList.remove('open');
        });
        
        // Logout
        const logoutBtn = document.getElementById('logout-btn');
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.logout();
        });
        
        // Clear bookmarks
        const clearBookmarksBtn = document.getElementById('clear-bookmarks');
        clearBookmarksBtn.addEventListener('click', () => this.clearBookmarks());
        
        // Subject filter
        const subjectFilter = document.getElementById('subject-filter');
        subjectFilter.addEventListener('change', (e) => {
            this.filterProgress(e.target.value);
        });
        
        // View progress button
        const viewProgressBtn = document.getElementById('view-progress-btn');
        viewProgressBtn.addEventListener('click', () => {
            document.querySelector('.progress-card').scrollIntoView({ 
                behavior: 'smooth' 
            });
        });
    }
    
    setupTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);
    }
    
    setTheme(theme) {
        document.body.className = `${theme}-theme`;
        const themeToggle = document.getElementById('theme-toggle');
        const icon = themeToggle.querySelector('.material-icons');
        
        if (theme === 'dark') {
            icon.textContent = 'dark_mode';
        } else {
            icon.textContent = 'light_mode';
        }
        
        localStorage.setItem('theme', theme);
    }
    
    toggleTheme() {
        const currentTheme = document.body.className.includes('dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
    
    logout() {
        localStorage.removeItem('currentUser');
        localStorage.removeItem('rememberedUser');
        window.location.href = 'login.html';
    }
    
    loadBookmarks() {
        const savedBookmarks = localStorage.getItem('bookmarks');
        if (savedBookmarks) {
            this.bookmarks = JSON.parse(savedBookmarks);
        } else {
            // Empty bookmarks initially
            this.bookmarks = [];
        }
    }
    
    loadProgressData() {
        // Load real progress data from localStorage
        const savedProgress = localStorage.getItem('userProgress');
        if (savedProgress) {
            try {
                const parsedProgress = JSON.parse(savedProgress);
                // Ensure each subject has the required structure
                this.progressData = {};
                Object.keys(parsedProgress).forEach(key => {
                    const subject = parsedProgress[key];
                    this.progressData[key] = {
                        name: subject.name || key,
                        icon: subject.icon || "📚",
                        chapters: subject.chapters || [],
                        completedChapters: subject.completedChapters || 0,
                        totalChapters: subject.totalChapters || (subject.chapters ? subject.chapters.length : 0),
                        studySessions: subject.studySessions || 0,
                        lastStudied: subject.lastStudied || null
                    };
                });
            } catch (error) {
                console.error('Error parsing progress data:', error);
                this.initializeDefaultProgress();
            }
        } else {
            this.initializeDefaultProgress();
        }
    }

    initializeDefaultProgress() {
            this.progressData = {
                mathematics: {
                    name: "Mathematics",
                    icon: "📐",
                    chapters: [
                        { name: "Basic Arithmetic", status: "pending" },
                        { name: "Algebra", status: "pending" },
                        { name: "Geometry", status: "pending" },
                        { name: "Trigonometry", status: "pending" },
                        { name: "Calculus", status: "pending" }
                    ],
                    completedChapters: 0,
                    totalChapters: 5,
                    studySessions: 0,
                    lastStudied: null
                },
                science: {
                    name: "Science",
                    icon: "🧪",
                    chapters: [
                        { name: "Physics Basics", status: "pending" },
                        { name: "Chemistry", status: "pending" },
                        { name: "Biology", status: "pending" },
                        { name: "Earth Science", status: "pending" },
                        { name: "Astronomy", status: "pending" }
                    ],
                    completedChapters: 0,
                    totalChapters: 5,
                    studySessions: 0,
                    lastStudied: null
                },
                english: {
                    name: "English",
                    icon: "📚",
                    chapters: [
                        { name: "Grammar", status: "pending" },
                        { name: "Vocabulary", status: "pending" },
                        { name: "Literature", status: "pending" },
                        { name: "Writing", status: "pending" }
                    ],
                    completedChapters: 0,
                    totalChapters: 4,
                    studySessions: 0,
                    lastStudied: null
                },
                history: {
                    name: "History",
                    icon: "🏛️",
                    chapters: [
                        { name: "Ancient History", status: "pending" },
                        { name: "Medieval History", status: "pending" },
                        { name: "Modern History", status: "pending" },
                        { name: "Contemporary History", status: "pending" }
                    ],
                    completedChapters: 0,
                    totalChapters: 4,
                    studySessions: 0,
                    lastStudied: null
                }
            };
            // Save default structure
            localStorage.setItem('userProgress', JSON.stringify(this.progressData));
    }
    
    loadActivityData() {
        // Load real activity data from localStorage
        const savedActivity = localStorage.getItem('userActivity');
        if (savedActivity) {
            this.activityData = JSON.parse(savedActivity);
        } else {
            this.activityData = [];
        }
        
        // If no activity, show helpful message
        if (this.activityData.length === 0) {
            this.activityData = [{
                type: "welcome",
                title: "Welcome to Edu Assist!",
                description: "Start chatting to see your activity here",
                time: "now",
                icon: "👋"
            }];
        }
    }
    
    renderDashboard() {
        this.renderBookmarks();
        this.renderProgress();
        this.renderActivity();
        this.updateStats();
    }
    
    renderBookmarks() {
        const bookmarksList = document.getElementById('bookmarks-list');
        
        if (this.bookmarks.length === 0) {
            bookmarksList.innerHTML = `
                <div class="empty-state">
                    <span class="material-icons">bookmark_border</span>
                    <p>No bookmarked topics yet</p>
                    <p>Start learning and bookmark important topics!</p>
                </div>
            `;
            return;
        }
        
        bookmarksList.innerHTML = this.bookmarks.map(bookmark => `
            <div class="bookmark-item">
                <div class="bookmark-subject">${bookmark.subject} - ${bookmark.topic}</div>
                <div class="bookmark-text">${bookmark.text}</div>
                <div class="bookmark-date">${this.formatDate(bookmark.date)}</div>
            </div>
        `).join('');
    }
    
    renderProgress() {
        const progressVisualization = document.getElementById('progress-visualization');
        
        const progressHTML = Object.values(this.progressData).map(subject => {
            const totalChapters = subject.totalChapters || (subject.chapters ? subject.chapters.length : 0);
            const completedChapters = subject.completedChapters || 0;
            const progressPercentage = totalChapters > 0 ? (completedChapters / totalChapters) * 100 : 0;
            
            return `
                <div class="subject-progress">
                    <div class="subject-header">
                        <span class="subject-icon">${subject.icon}</span>
                        <div>
                            <div class="subject-name">${subject.name}</div>
                            <div class="subject-stats">
                                ${completedChapters}/${totalChapters} chapters completed (${Math.round(progressPercentage)}%)
                            </div>
                        </div>
                    </div>
                    
                    <div class="progress-path">
                        <div class="progress-line">
                            <div class="progress-line-filled" style="width: ${progressPercentage}%"></div>
                        </div>
                        <div class="progress-steps">
                            ${(subject.chapters || []).map((chapter, index) => `
                                <div class="progress-step">
                                    <div class="step-circle ${chapter.status}">
                                        ${chapter.status === 'completed' ? '✓' : 
                                          chapter.status === 'current' ? '●' : index + 1}
                                    </div>
                                    <div class="step-label">${chapter.name}</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        progressVisualization.innerHTML = progressHTML;
    }
    
    renderActivity() {
        const activityList = document.getElementById('activity-list');
        
        activityList.innerHTML = this.activityData.map(activity => `
            <div class="activity-item">
                <div class="activity-icon ${activity.type}">
                    <span class="material-icons">
                        ${activity.type === 'chat' ? 'chat' : 
                          activity.type === 'bookmark' ? 'bookmark' : 
                          activity.type === 'progress' ? 'trending_up' : 'circle'}
                    </span>
                </div>
                <div class="activity-content">
                    <div class="activity-title">${activity.title}</div>
                    <div class="activity-description">${activity.description}</div>
                </div>
                <div class="activity-time">${activity.time}</div>
            </div>
        `).join('');
    }
    
    updateStats() {
        console.log('🔍 Starting updateStats calculation');
        
        // Calculate real stats
        const activity = JSON.parse(localStorage.getItem('userActivity') || '[]');
        const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]');
        const progress = JSON.parse(localStorage.getItem('userProgress') || '{}');
        
        console.log('📊 Data loaded:', {
            activityCount: activity.length,
            bookmarksCount: bookmarks.length,
            progressKeys: Object.keys(progress)
        });

        // Debug: Show activity types
        const activityTypes = activity.map(a => a.type);
        console.log('🔍 Activity types found:', activityTypes);
        console.log('💬 Chat activities:', activity.filter(a => a.type === 'chat'));
        
        // Debug: Show raw localStorage content
        console.log('🗃️ Raw userActivity from localStorage:', localStorage.getItem('userActivity'));
        
        // Study sessions: total study activities
        const studySessions = activity.filter(a => a.type === 'chat' || a.type === 'study').length;
        
        // Topics studied: count unique subject-topic combinations
        const uniqueTopics = new Set();
        activity.forEach(a => {
            if (a.subject && a.topic) {
                uniqueTopics.add(`${a.subject}-${a.topic}`);
            }
        });
        
        // Current streak: consecutive days with activity (simplified calculation)
        let streak = 0;
        const today = new Date().toDateString();
        const recentActivity = activity.filter(a => {
            const activityDate = new Date(a.timestamp || Date.now()).toDateString();
            return activityDate === today;
        });
        if (recentActivity.length > 0) streak = 1; // Simplified: 1 if active today
        
        // Questions asked: total chat activities
        const questionsAsked = activity.filter(a => a.type === 'chat').length;
        console.log('❓ Questions asked:', questionsAsked);
        
        // Study time: get actual tracked time from new system
        let studyTimeMs = 0;
        try {
            const sessions = JSON.parse(localStorage.getItem('studySessions') || '[]');
            const today = new Date().toDateString();
            const todaySession = sessions.find(s => s.date === today);
            studyTimeMs = todaySession ? todaySession.totalTime : 0;
        } catch (error) {
            console.error('Error reading study sessions:', error);
        }
        
        const studyTimeHours = studyTimeMs / (1000 * 60 * 60); // Convert to hours
        console.log('⏱️ Study time:', { 
            milliseconds: studyTimeMs, 
            hours: studyTimeHours,
            formatted: this.formatStudyTime(studyTimeMs)
        });
        
        // Completion rate: percentage of completed chapters
        let totalChapters = 0;
        let completedChapters = 0;
        Object.values(progress).forEach(subject => {
            if (subject.totalChapters) {
                totalChapters += subject.totalChapters;
                completedChapters += subject.completedChapters || 0;
            }
        });
        const completionRate = totalChapters > 0 ? Math.round((completedChapters / totalChapters) * 100) : 0;
        console.log('🎯 Completion rate:', completionRate, '%');
        
        // Achievements: bookmarks + completed chapters
        const achievements = bookmarks.length + completedChapters;
        console.log('🏆 Achievements:', achievements);
        
        console.log('📊 About to update DOM elements...');
        
        // Update welcome section stats
        document.getElementById('total-sessions').textContent = studySessions || '0';
        document.getElementById('total-topics').textContent = uniqueTopics.size || '0';
        document.getElementById('current-streak').textContent = streak || '0';
        
        // Update insights stats
        document.getElementById('questions-asked').textContent = questionsAsked || '0';
        document.getElementById('study-time').textContent = this.formatStudyTime(studyTimeMs);
        document.getElementById('completion-rate').textContent = `${completionRate}%`;
        document.getElementById('achievements').textContent = achievements || '0';
        
        console.log('✅ Stats updated successfully!');
    }

    formatStudyTime(milliseconds) {
        if (milliseconds === 0) return '0m';
        
        const hours = Math.floor(milliseconds / (1000 * 60 * 60));
        const minutes = Math.floor((milliseconds % (1000 * 60 * 60)) / (1000 * 60));
        
        if (hours > 0) {
            return minutes > 0 ? `${hours}h ${minutes}m` : `${hours}h`;
        } else if (minutes > 0) {
            return `${minutes}m`;
        } else {
            return '<1m';
        }
    }

    refreshStats() {
        // Reload data and update display
        this.loadBookmarks();
        this.loadActivityData();
        this.loadProgressData();
        this.updateStats();
    }
    
    clearBookmarks() {
        if (confirm('Are you sure you want to clear all bookmarks?')) {
            this.bookmarks = [];
            localStorage.removeItem('bookmarks');
            this.renderBookmarks();
            this.showToast('All bookmarks cleared!');
        }
    }
    
    filterProgress(subjectId) {
        const progressVisualization = document.getElementById('progress-visualization');
        
        if (subjectId === 'all') {
            this.renderProgress();
            return;
        }
        
        const subject = this.progressData[subjectId];
        if (!subject) return;
        
        const progressPercentage = (subject.completedChapters / subject.totalChapters) * 100;
        
        progressVisualization.innerHTML = `
            <div class="subject-progress">
                <div class="subject-header">
                    <span class="subject-icon">${subject.icon}</span>
                    <div>
                        <div class="subject-name">${subject.name}</div>
                        <div class="subject-stats">
                            ${subject.completedChapters}/${subject.totalChapters} chapters completed (${Math.round(progressPercentage)}%)
                        </div>
                    </div>
                </div>
                
                <div class="progress-path">
                    <div class="progress-line">
                        <div class="progress-line-filled" style="width: ${progressPercentage}%"></div>
                    </div>
                    <div class="progress-steps">
                        ${subject.chapters.map((chapter, index) => `
                            <div class="progress-step">
                                <div class="step-circle ${chapter.status}">
                                    ${chapter.status === 'completed' ? '✓' : 
                                      chapter.status === 'current' ? '●' : index + 1}
                                </div>
                                <div class="step-label">${chapter.name}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`;
        
        return date.toLocaleDateString();
    }
    
    showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 24px;
            right: 24px;
            background-color: var(--surface-color);
            color: var(--text-color);
            padding: 12px 16px;
            border-radius: 8px;
            box-shadow: var(--shadow-elevated);
            border: 1px solid var(--border-color);
            z-index: 1000;
            animation: slideInUp 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOutDown 0.3s ease';
            setTimeout(() => {
                if (document.body.contains(toast)) {
                    document.body.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }

    // Static method to track user activity from other pages
    static trackActivity(type, title, description, subject = null, topic = null) {
        const activity = JSON.parse(localStorage.getItem('userActivity') || '[]');
        const timeAgo = DashboardManager.getTimeAgo(new Date());
        
        const newActivity = {
            type: type, // 'chat', 'bookmark', 'progress', 'study'
            title: title,
            description: description,
            time: timeAgo,
            timestamp: new Date().toISOString(),
            subject: subject,
            topic: topic,
            icon: DashboardManager.getActivityIcon(type)
        };
        
        activity.unshift(newActivity); // Add to beginning
        
        // Keep only last 20 activities
        if (activity.length > 20) {
            activity.splice(20);
        }
        
        localStorage.setItem('userActivity', JSON.stringify(activity));
    }

    // Static method to update subject progress
    static updateProgress(subject, topic, action = 'study') {
        const progress = JSON.parse(localStorage.getItem('userProgress') || '{}');
        const subjectKey = subject.toLowerCase();
        
        if (progress[subjectKey]) {
            // Update study sessions
            progress[subjectKey].studySessions = (progress[subjectKey].studySessions || 0) + 1;
            progress[subjectKey].lastStudied = new Date().toISOString();
            
            // Find and update chapter if topic matches
            const chapter = progress[subjectKey].chapters.find(ch => 
                ch.name.toLowerCase().includes(topic.toLowerCase()) || 
                topic.toLowerCase().includes(ch.name.toLowerCase())
            );
            
            if (chapter && chapter.status === 'pending') {
                chapter.status = 'current';
            }
            
            // Update completed chapters count
            progress[subjectKey].completedChapters = progress[subjectKey].chapters
                .filter(ch => ch.status === 'completed').length;
            
            localStorage.setItem('userProgress', JSON.stringify(progress));
            
            // Track progress activity
            DashboardManager.trackActivity(
                'progress',
                `Studied ${subject}`,
                `Practiced ${topic}`,
                subject,
                topic
            );
        }
    }

    // Helper methods
    static getActivityIcon(type) {
        const icons = {
            'chat': '💬',
            'bookmark': '🔖',
            'progress': '📈',
            'study': '📚',
            'welcome': '👋'
        };
        return icons[type] || '📝';
    }

    static getTimeAgo(date) {
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);
        
        if (diffInSeconds < 60) return 'just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
        if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
        return `${Math.floor(diffInSeconds / 604800)} weeks ago`;
    }
}

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardManager = new DashboardManager();
});

// Global function to refresh dashboard from other pages
window.refreshDashboard = function() {
    if (window.dashboardManager) {
        window.dashboardManager.refreshStats();
    }
};

// Global function to force update stats for debugging
window.testStatsUpdate = function() {
    console.log('🧪 Manual stats update test');
    if (window.dashboardManager) {
        window.dashboardManager.updateStats();
    } else {
        console.log('❌ dashboardManager not available');
    }
};

// Global function to check localStorage data
window.checkLocalStorage = function() {
    console.log('🔍 LocalStorage Debug:');
    console.log('userActivity:', JSON.parse(localStorage.getItem('userActivity') || '[]'));
    console.log('bookmarks:', JSON.parse(localStorage.getItem('bookmarks') || '[]'));
    console.log('userProgress:', JSON.parse(localStorage.getItem('userProgress') || '{}'));
};

// Add CSS animations for toast
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInUp {
        from {
            transform: translateY(100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutDown {
        from {
            transform: translateY(0);
            opacity: 1;
        }
        to {
            transform: translateY(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);