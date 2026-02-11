class EduAssist {
    constructor() {
        this.checkAuthentication();
        this.currentSubject = 'Mathematics';
        this.currentTopic = 'Algebra';
        this.subjects = [];
        this.isRecording = false;
        this.eli5Mode = false;
        
        this.init();
    }
    
    checkAuthentication() {
        const userData = localStorage.getItem('currentUser');
        if (!userData) {
            return;
        }
    }
    
    async init() {
        await this.loadSubjects();
        this.setupEventListeners();
        this.setupTheme();
        this.renderSubjects();
        this.addRippleEffects();
    }
    
    async loadSubjects() {
        try {
            const response = await fetch('sidebar_data.json');
            this.subjects = await response.json();
        } catch (error) {
            console.error('Failed to load subjects data:', error);
            // Fallback data
            this.subjects = [
                {
                    id: 'math',
                    name: 'Mathematics',
                    icon: '📐',
                    topics: ['Algebra', 'Geometry', 'Calculus', 'Statistics']
                },
                {
                    id: 'science',
                    name: 'Science',
                    icon: '🧪',
                    topics: ['Physics', 'Chemistry', 'Biology', 'Earth Science']
                },
                {
                    id: 'english',
                    name: 'English',
                    icon: '📚',
                    topics: ['Grammar', 'Literature', 'Writing', 'Reading Comprehension']
                },
                {
                    id: 'history',
                    name: 'History',
                    icon: '🏛️',
                    topics: ['World History', 'American History', 'Ancient Civilizations', 'Modern History']
                }
            ];
        }
    }
    
    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // Message input
        const messageInput = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');
        
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Voice input
        const micBtn = document.getElementById('mic-btn');
        micBtn.addEventListener('click', () => this.toggleRecording());
        
        // ELI5 toggle
        const eli5Toggle = document.getElementById('eli5-toggle');
        eli5Toggle.addEventListener('change', (e) => {
            this.eli5Mode = e.target.checked;
            console.log('ELI5 mode:', this.eli5Mode);
        });
        
        // Tab switching
        const tabBtns = document.querySelectorAll('.tab-btn');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;
                this.switchTab(tabName);
            });
        });
        
        // Suggested questions
        const questionBtns = document.querySelectorAll('.question-btn');
        questionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.getElementById('message-input').value = e.target.textContent;
                this.sendMessage();
            });
        });
        
        // Message actions
        document.addEventListener('click', (e) => {
            if (e.target.closest('.action-btn')) {
                const button = e.target.closest('.action-btn');
                const action = button.title.toLowerCase();
                this.handleMessageAction(action, button);
            }
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
    
    renderSubjects() {
        const subjectsList = document.getElementById('subjects-list');
        subjectsList.innerHTML = '';
        
        this.subjects.forEach(subject => {
            const subjectDiv = document.createElement('div');
            subjectDiv.className = 'subject-item';
            subjectDiv.innerHTML = `
                <div class="subject-header ripple" data-subject="${subject.id}">
                    <span class="subject-icon">${subject.icon}</span>
                    <span class="subject-name">${subject.name}</span>
                    <span class="material-icons expand-icon">expand_more</span>
                </div>
                <div class="topics-list" id="topics-${subject.id}">
                    ${subject.topics.map(topic => `
                        <div class="topic-item ripple" data-subject="${subject.name}" data-topic="${topic}">
                            ${topic}
                        </div>
                    `).join('')}
                </div>
            `;
            
            subjectsList.appendChild(subjectDiv);
        });
        
        // Add event listeners
        document.querySelectorAll('.subject-header').forEach(header => {
            header.addEventListener('click', (e) => {
                const subjectId = e.currentTarget.dataset.subject;
                this.toggleSubject(subjectId);
            });
        });
        
        document.querySelectorAll('.topic-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const subject = e.currentTarget.dataset.subject;
                const topic = e.currentTarget.dataset.topic;
                this.selectTopic(subject, topic);
            });
        });
    }
    
    toggleSubject(subjectId) {
        const topicsList = document.getElementById(`topics-${subjectId}`);
        const header = document.querySelector(`[data-subject="${subjectId}"]`);
        const icon = header.querySelector('.expand-icon');
        
        topicsList.classList.toggle('expanded');
        icon.style.transform = topicsList.classList.contains('expanded') ? 'rotate(180deg)' : 'rotate(0deg)';
    }
    
    selectTopic(subject, topic) {
        this.currentSubject = subject;
        this.currentTopic = topic;
        
        // Update UI
        document.getElementById('current-subject').textContent = subject;
        document.getElementById('current-topic').textContent = topic;
        document.getElementById('welcome-subject').textContent = subject;
        
        // Update active states
        document.querySelectorAll('.topic-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-topic="${topic}"]`).classList.add('active');
        
        // Show topic change message
        this.addMessage('ai', `Great! Let's talk about ${topic} in ${subject}. What would you like to learn?`);
    }
    
    sendMessage() {
        const input = document.getElementById('message-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Clear input and add user message
        input.value = '';
        this.addMessage('student', message);
        
        // Generate AI response after a short delay
        setTimeout(() => {
            this.generateAIResponse(message);
        }, 1000);
    }
    
    addMessage(type, text) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const time = this.getCurrentTime();
        
        if (type === 'ai') {
            messageDiv.innerHTML = `
                <div class="message-avatar">
                    <span class="material-icons">smart_toy</span>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <p>${text}</p>
                    </div>
                    <div class="message-actions">
                        <button class="action-btn" title="Copy message">
                            <span class="material-icons">content_copy</span>
                        </button>
                        <button class="action-btn" title="Save message">
                            <span class="material-icons">bookmark</span>
                        </button>
                        <button class="action-btn" title="Like message">
                            <span class="material-icons">thumb_up</span>
                        </button>
                    </div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="message-bubble">
                        <p>${text}</p>
                    </div>
                    <div class="message-time">${time}</div>
                </div>
            `;
        }
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Update XP
        if (type === 'student') {
            this.updateXP(5);
        }
    }
    
    generateAIResponse(userMessage) {
        const responses = [
            `That's a great question about ${this.currentTopic}! Let me explain...`,
            `In ${this.currentSubject}, ${this.currentTopic} is a fascinating topic. Here's what you need to know:`,
            `I'd be happy to help you understand ${this.currentTopic} better!`,
            `Let's break down this ${this.currentTopic} concept step by step:`,
            `That's an excellent way to think about ${this.currentTopic}! Here's my take:`
        ];
        
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
        
        let fullResponse = randomResponse;
        
        // Add ELI5 mode response
        if (this.eli5Mode) {
            fullResponse += "\n\n🧠 **ELI5 Mode**: Think of it like this - imagine you're explaining this to a 5-year-old friend!";
        }
        
        // Add some topic-specific responses
        if (userMessage.toLowerCase().includes('formula')) {
            fullResponse += '\n\nHere\'s the key formula:\n<div class="formula-block"><code>y = mx + b</code></div>';
        }
        
        this.addMessage('ai', fullResponse);
    }
    
    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    toggleRecording() {
        const micBtn = document.getElementById('mic-btn');
        
        if (!this.isRecording) {
            this.startRecording();
            micBtn.classList.add('recording');
        } else {
            this.stopRecording();
            micBtn.classList.remove('recording');
        }
    }
    
    startRecording() {
        this.isRecording = true;
        console.log('Started recording...');
        
        // Simulate recording for demo
        setTimeout(() => {
            if (this.isRecording) {
                this.stopRecording();
                document.getElementById('message-input').value = "What is the quadratic formula?";
            }
        }, 3000);
    }
    
    stopRecording() {
        this.isRecording = false;
        const micBtn = document.getElementById('mic-btn');
        micBtn.classList.remove('recording');
        console.log('Stopped recording');
    }
    
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Update tab panels
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        document.getElementById(`${tabName}-panel`).classList.add('active');
    }
    
    handleMessageAction(action, button) {
        const message = button.closest('.message');
        const messageText = message.querySelector('.message-bubble p').textContent;
        
        switch (action) {
            case 'copy message':
                navigator.clipboard.writeText(messageText);
                this.showToast('Message copied to clipboard!');
                break;
            case 'save message':
                this.saveMessage(messageText);
                button.querySelector('.material-icons').textContent = 'bookmark_added';
                this.showToast('Message bookmarked!');
                break;
            case 'like message':
                button.querySelector('.material-icons').textContent = 'thumb_up';
                button.style.color = 'var(--primary-color)';
                this.showToast('Message liked!');
                this.updateXP(2);
                break;
        }
    }
    
    saveMessage(messageText) {
        const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]');
        bookmarks.push({
            text: messageText,
            subject: this.currentSubject,
            topic: this.currentTopic,
            date: new Date().toISOString()
        });
        localStorage.setItem('bookmarks', JSON.stringify(bookmarks));
        
        // Update bookmarks panel
        this.updateBookmarksPanel();
    }
    
    updateBookmarksPanel() {
        const bookmarksPanel = document.getElementById('bookmarks-panel');
        const bookmarksList = bookmarksPanel.querySelector('.bookmarks-list');
        const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]');
        
        bookmarksList.innerHTML = bookmarks.map(bookmark => `
            <div class="bookmark-item">
                <p><strong>Q:</strong> ${bookmark.text.substring(0, 100)}${bookmark.text.length > 100 ? '...' : ''}</p>
                <p><strong>Subject:</strong> ${bookmark.subject} - ${bookmark.topic}</p>
                <span class="bookmark-date">${new Date(bookmark.date).toLocaleDateString()}</span>
            </div>
        `).join('');
    }
    
    updateXP(points) {
        const currentXP = parseInt(localStorage.getItem('currentXP') || '240');
        const newXP = currentXP + points;
        
        localStorage.setItem('currentXP', newXP.toString());
        
        // Update XP display
        const xpProgress = document.querySelector('.xp-progress');
        const xpFill = document.querySelector('.xp-fill');
        const maxXP = 500;
        
        xpProgress.textContent = `${newXP} / ${maxXP} XP`;
        xpFill.style.width = `${(newXP / maxXP) * 100}%`;
        
        // Show XP gain
        this.showToast(`+${points} XP!`);
    }
    
    showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 100px;
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
                document.body.removeChild(toast);
            }, 300);
        }, 2000);
    }
    
    addRippleEffects() {
        const buttons = document.querySelectorAll('button, .nav-button, .input-btn');
        buttons.forEach(button => {
            button.classList.add('ripple');
        });
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    window.eduAssistInstance = new EduAssist();
});

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
