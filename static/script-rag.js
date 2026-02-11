class EduAssist {
    constructor() {
        this.checkAuthentication();
        this.currentSubject = 'Mathematics';
        this.currentTopic = 'Algebra';
        this.subjects = [];
        this.isRecording = false;
        this.eli5Mode = false;
        this.sessionId = null;
        this.apiBaseUrl = 'http://localhost:8000/api';  // Backend API URL
        
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
        
        // File upload for PDFs
        this.setupFileUpload();
    }
    
    setupFileUpload() {
        const attachBtn = document.querySelector('.attach-btn');
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.pdf';
        fileInput.style.display = 'none';
        document.body.appendChild(fileInput);
        
        attachBtn.addEventListener('click', () => {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (file) {
                await this.uploadPDF(file);
            }
        });
    }
    
    async uploadPDF(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('subject', this.currentSubject);
            
            // Show upload progress
            this.showToast(`Uploading ${file.name}...`);
            
            const response = await fetch(`${this.apiBaseUrl}/upload-document`, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showToast(`Successfully uploaded ${file.name}! ${result.chunks_count} chunks processed.`);
                
                // Add notification message
                this.addMessage('ai', `📄 I've processed your PDF "${file.name}" and added it to my knowledge base! I can now answer questions based on its content. What would you like to know about it?`);
            } else {
                const error = await response.json();
                this.showToast(`Upload failed: ${error.detail}`, 'error');
            }
            
        } catch (error) {
            console.error('Upload error:', error);
            this.showToast('Upload failed. Please try again.', 'error');
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('message-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Clear input and add user message
        input.value = '';
        this.addMessage('student', message);
        
        // Show typing indicator
        const typingIndicator = this.showTypingIndicator();
        
        try {
            // Send message to backend
            const response = await this.sendToBackend(message);
            
            // Remove typing indicator
            this.removeTypingIndicator(typingIndicator);
            
            // Add AI response with sources
            this.addMessage('ai', response.response, response.sources);
            
            // Store session ID
            if (response.session_id) {
                this.sessionId = response.session_id;
            }
            
        } catch (error) {
            // Remove typing indicator
            this.removeTypingIndicator(typingIndicator);
            
            // Show error message
            this.addMessage('ai', 'I apologize, but I am experiencing some technical difficulties. Please try again in a moment.');
            console.error('Error sending message:', error);
        }
    }
    
    async sendToBackend(message) {
        const requestData = {
            message: message,
            subject: this.currentSubject,
            eli5_mode: this.eli5Mode,
            session_id: this.sessionId
        };
        
        const response = await fetch(`${this.apiBaseUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message ai-message typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <span class="material-icons">smart_toy</span>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-animation">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        return typingDiv;
    }
    
    removeTypingIndicator(typingIndicator) {
        if (typingIndicator && typingIndicator.parentNode) {
            typingIndicator.parentNode.removeChild(typingIndicator);
        }
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
    
    addMessage(type, text, sources = []) {
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
                        ${sources.length > 0 ? this.renderSources(sources) : ''}
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
        
        // Update XP for student messages
        if (type === 'student') {
            this.updateXP(5);
        }
    }
    
    renderSources(sources) {
        if (!sources || sources.length === 0) return '';
        
        return `
            <div class="sources-section">
                <h5>Sources:</h5>
                <ul class="sources-list">
                    ${sources.map(source => `
                        <li class="source-item">
                            <span class="source-type">[${source.type}]</span>
                            <span class="source-name">${source.source}</span>
                            ${source.url ? `<a href="${source.url}" target="_blank" class="source-link">🔗</a>` : ''}
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
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
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
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
        
        const xpProgress = document.querySelector('.xp-progress');
        const xpFill = document.querySelector('.xp-fill');
        const maxXP = 500;
        
        xpProgress.textContent = `${newXP} / ${maxXP} XP`;
        xpFill.style.width = `${(newXP / maxXP) * 100}%`;
        
        this.showToast(`+${points} XP!`);
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
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
            max-width: 300px;
        `;
        
        if (type === 'error') {
            toast.style.backgroundColor = '#f44336';
            toast.style.color = 'white';
        }
        
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
    
    addRippleEffects() {
        const buttons = document.querySelectorAll('button, .nav-button, .input-btn');
        buttons.forEach(button => {
            button.classList.add('ripple');
        });
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    new EduAssist();
});

// Add CSS for typing animation and sources
const style = document.createElement('style');
style.textContent = `
    .typing-animation {
        display: flex;
        gap: 4px;
        align-items: center;
        padding: 8px 0;
    }
    
    .typing-animation span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--text-secondary);
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-animation span:nth-child(1) { animation-delay: -0.32s; }
    .typing-animation span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% {
            transform: scale(0.8);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .sources-section {
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid var(--border-color);
    }
    
    .sources-section h5 {
        margin: 0 0 8px 0;
        font-size: 12px;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
    }
    
    .sources-list {
        list-style: none;
        margin: 0;
        padding: 0;
    }
    
    .source-item {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
        font-size: 12px;
    }
    
    .source-type {
        background: var(--primary-color);
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 500;
        font-size: 10px;
    }
    
    .source-name {
        flex: 1;
        color: var(--text-secondary);
    }
    
    .source-link {
        color: var(--primary-color);
        text-decoration: none;
    }
    
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
