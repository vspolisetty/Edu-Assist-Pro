class EduAssist {
    constructor() {
        this.checkAuthentication();
        this.currentSubject = 'Compliance Training';
        this.currentTopic = 'Company Policies';
        this.subjects = [];
        this.questionsData = {};
        this.topicsData = {};
        this.isRecording = false;
        this.eli5Mode = false;
        
        // Time tracking properties
        this.sessionStartTime = null;
        this.lastActivityTime = null;
        this.activityTimeout = 5 * 60 * 1000; // 5 minutes in milliseconds
        this.sessionTimer = null;
        this.totalSessionTime = 0;
        
        this.init();
    }
    
    checkAuthentication() {
        if (window.AUTH && !AUTH.isAuthenticated()) {
            window.location.href = 'login.html';
            return;
        }
    }

    setUserName() {
        const u = JSON.parse(localStorage.getItem('currentUser') || '{}');
        const name = u.name || u.username || u.user_id || 'User';
        const el = document.getElementById('userName');
        if (el) el.textContent = name;
    }
    
    async init() {
        await this.loadSubjects();
        await this.loadQuestions();
        await this.loadTopics();
        this.setupEventListeners();
        this.setupTheme();
        this.setUserName();
        this.renderSubjects();
        this.renderQuestions();
        this.renderTopics();
        this.addRippleEffects();
        this.startTimeTracking();
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
                    id: 'compliance',
                    name: 'Compliance Training',
                    icon: '�',
                    topics: ['Company Policies', 'Data Privacy', 'Workplace Safety', 'Ethics & Conduct']
                },
                {
                    id: 'security',
                    name: 'Security Awareness',
                    icon: '🔒',
                    topics: ['Cybersecurity Basics', 'Phishing Prevention', 'Password Management', 'Incident Reporting']
                },
                {
                    id: 'leadership',
                    name: 'Leadership Development',
                    icon: '�',
                    topics: ['Team Management', 'Communication Skills', 'Conflict Resolution', 'Performance Reviews']
                },
                {
                    id: 'technical',
                    name: 'Technical Skills',
                    icon: '⚙️',
                    topics: ['Tools & Systems', 'Process Documentation', 'Quality Standards', 'Best Practices']
                }
            ];
        }
    }
    
    async loadTopics() {
        try {
            const response = await fetch('topics_data.json');
            this.topicsData = await response.json();
            console.log('✅ Topics data loaded:', Object.keys(this.topicsData));
        } catch (error) {
            console.error('Failed to load topics data:', error);
            this.topicsData = {};
        }
    }

    async loadQuestions() {
        try {
            const response = await fetch('questions_data.json');
            this.questionsData = await response.json();
            console.log('✅ Questions data loaded:', Object.keys(this.questionsData));
        } catch (error) {
            console.error('Failed to load questions data:', error);
            this.questionsData = {};
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
    
    renderQuestions() {
        const questionsContainer = document.querySelector('.suggested-questions');
        if (!questionsContainer) {
            console.error('Questions container not found');
            return;
        }

        // Find the correct subject ID for the questions data
        let subjectKey = null;
        if (this.currentSubject === 'Mathematics') {
            subjectKey = 'mathematics';
        } else if (this.currentSubject === 'Science') {
            subjectKey = 'science';
        }

        // Clear existing questions
        questionsContainer.innerHTML = '';

        if (subjectKey && this.questionsData[subjectKey] && this.questionsData[subjectKey][this.currentTopic]) {
            const questions = this.questionsData[subjectKey][this.currentTopic];
            
            questions.forEach(question => {
                const questionBtn = document.createElement('button');
                questionBtn.className = 'question-btn ripple';
                questionBtn.textContent = question;
                questionBtn.addEventListener('click', () => {
                    this.askQuestion(question);
                });
                questionsContainer.appendChild(questionBtn);
            });
            
            console.log(`✅ Loaded ${questions.length} questions for ${this.currentSubject} - ${this.currentTopic}`);
        } else {
            // Show default message if no questions available
            questionsContainer.innerHTML = `
                <div class="no-questions">
                    <p>No suggested questions available for ${this.currentTopic}</p>
                    <p>Try asking your own question in the chat!</p>
                </div>
            `;
            console.log(`⚠️ No questions found for ${this.currentSubject} - ${this.currentTopic}`);
        }
    }

    renderTopics() {
        const topicsContainer = document.querySelector('.topic-list');
        if (!topicsContainer) {
            console.error('Topics container not found');
            return;
        }

        // Find the correct subject ID for the topics data
        let subjectKey = null;
        if (this.currentSubject === 'Mathematics') {
            subjectKey = 'mathematics';
        } else if (this.currentSubject === 'Science') {
            subjectKey = 'science';
        }

        // Clear existing topics
        topicsContainer.innerHTML = '';

        if (subjectKey && this.topicsData[subjectKey] && this.topicsData[subjectKey][this.currentTopic]) {
            const topics = this.topicsData[subjectKey][this.currentTopic];
            
            topics.forEach((topic, index) => {
                const topicItem = document.createElement('div');
                topicItem.className = 'topic-item-right';
                topicItem.innerHTML = `
                    <div class="topic-number">${index + 1}</div>
                    <div class="topic-content">
                        <h4>${topic}</h4>
                        <p>Click to explore this topic</p>
                    </div>
                `;
                topicItem.addEventListener('click', () => {
                    this.exploreSubtopic(topic);
                });
                topicsContainer.appendChild(topicItem);
            });
            
            console.log(`✅ Loaded ${topics.length} topics for ${this.currentSubject} - ${this.currentTopic}`);
        } else {
            // Show default message if no topics available
            topicsContainer.innerHTML = `
                <div class="no-topics">
                    <p>No related topics available for ${this.currentTopic}</p>
                    <p>Select a different topic to see related subjects!</p>
                </div>
            `;
            console.log(`⚠️ No topics found for ${this.currentSubject} - ${this.currentTopic}`);
        }
    }

    exploreSubtopic(subtopic) {
        // Fill the input with a question about the subtopic
        const messageInput = document.getElementById('message-input');
        messageInput.value = `Tell me about ${subtopic}`;
        this.sendMessage();
    }

    askQuestion(question) {
        // Fill the input with the question and send it
        const messageInput = document.getElementById('message-input');
        messageInput.value = question;
        this.sendMessage();
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
        
        // Render questions for the selected topic
        this.renderQuestions();
        
        // Render topics for the selected topic
        this.renderTopics();
        
        // Track study session - both methods for reliability
        if (typeof DashboardManager !== 'undefined' && DashboardManager.updateProgress) {
            DashboardManager.updateProgress(subject, topic, 'study');
        }
        
        // Direct localStorage tracking as backup
        try {
            let progress = JSON.parse(localStorage.getItem('userProgress') || '{}');
            if (!progress[subject]) progress[subject] = {};
            if (!progress[subject][topic]) progress[subject][topic] = { sessions: 0, lastStudied: null };
            
            progress[subject][topic].sessions++;
            progress[subject][topic].lastStudied = new Date().toISOString();
            localStorage.setItem('userProgress', JSON.stringify(progress));
            
            console.log('Topic selection tracked directly:', subject, topic, progress[subject][topic]);
        } catch (error) {
            console.error('Error tracking topic selection:', error);
        }
    }
    
    sendMessage() {
        const input = document.getElementById('message-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Clear input and add user message
        input.value = '';
        this.addMessage('student', message);
        
        // Track chat activity
        this.trackChatActivity(message);
        
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
                        ${this.formatMessageText(text)}
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
    
    async generateAIResponse(userMessage) {
        try {
            // Show typing indicator
            this.showTypingIndicator();
            
            // Prepare the request payload
            const requestBody = {
                message: userMessage,
                subject: this.currentSubject || "General",
                topic: this.currentTopic || "General",
                eli5_mode: this.eli5Mode || false,
                conversation_history: this.getRecentMessages()
            };
            
            // Call the RAG backend
            const response = await (window.AUTH ? AUTH.fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            }) : fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            }));
            
            this.hideTypingIndicator();
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            let aiResponse = data.response || "I'm sorry, I couldn't generate a response right now.";
            
            // Add ELI5 mode indicator if enabled
            if (this.eli5Mode && !aiResponse.includes("ELI5")) {
                aiResponse += "\n\n🧠 **ELI5 Mode**: This explanation is simplified for easy understanding!";
            }
            
            this.addMessage('ai', aiResponse);
            
        } catch (error) {
            console.error('Error getting AI response:', error);
            this.hideTypingIndicator();
            
            // Fallback to a helpful error message
            const fallbackResponse = `I'm having trouble connecting to my knowledge base right now. Please make sure the backend server is running on localhost:3000. In the meantime, I'd be happy to help with general questions about ${this.currentTopic || 'your studies'}!`;
            this.addMessage('ai', fallbackResponse);
        }
    }
    
    getRecentMessages() {
        // Get last 5 messages for context
        const messages = Array.from(document.querySelectorAll('.message')).slice(-5);
        return messages.map(msg => {
            const isUser = msg.classList.contains('student-message');
            const text = msg.querySelector('.message-bubble p')?.textContent || '';
            return {
                role: isUser ? 'user' : 'assistant',
                content: text
            };
        });
    }
    
    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'message ai-message typing-indicator';
        indicator.id = 'typing-indicator';
        indicator.innerHTML = `
            <div class="message-avatar">
                <span class="material-icons">smart_toy</span>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.appendChild(indicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    formatMessageText(text) {
        // Convert markdown-style formatting to HTML
        let formattedText = text
            // Convert double line breaks to paragraph breaks
            .replace(/\n\n/g, '</p><p>')
            // Convert single line breaks to <br>
            .replace(/\n/g, '<br>')
            // Convert **bold** to <strong>
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Convert bullet points (• or -) to proper list items
            .replace(/^[•\-]\s+(.+)$/gm, '<li>$1</li>')
            // Convert numbered lists
            .replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');
        
        // Wrap in paragraph tags if not already wrapped
        if (!formattedText.startsWith('<')) {
            formattedText = '<p>' + formattedText + '</p>';
        }
        
        // Convert sequences of <li> tags into proper <ul> lists
        formattedText = formattedText.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');
        
        return formattedText;
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
        
        // Track bookmark activity - both methods for reliability
        if (typeof DashboardManager !== 'undefined' && DashboardManager.trackActivity) {
            DashboardManager.trackActivity(
                'bookmark',
                'Bookmarked Message',
                `Saved: "${messageText.substring(0, 50)}${messageText.length > 50 ? '...' : ''}"`,
                this.currentSubject,
                this.currentTopic
            );
        }
        
        // Direct localStorage tracking as backup
        try {
            let activity = JSON.parse(localStorage.getItem('userActivity') || '[]');
            activity.push({
                type: 'bookmark',
                action: 'Bookmarked Message',
                details: `Saved: "${messageText.substring(0, 50)}${messageText.length > 50 ? '...' : ''}"`,
                subject: this.currentSubject,
                topic: this.currentTopic,
                timestamp: new Date().toISOString()
            });
            localStorage.setItem('userActivity', JSON.stringify(activity));
            console.log('Bookmark activity tracked directly:', activity[activity.length - 1]);
        } catch (error) {
            console.error('Error tracking bookmark activity:', error);
        }
        
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

    trackChatActivity(message) {
        // Track chat activity for dashboard
        console.log('🔍 Starting trackChatActivity for message:', message); // Enhanced debug log
        
        const subject = this.currentSubject || 'General';
        const topic = this.currentTopic || 'General Chat';
        
        // Create a meaningful title based on the message
        let title = 'Chat Session';
        if (message.toLowerCase().includes('what') || message.toLowerCase().includes('how')) {
            title = 'Asked Question';
        } else if (message.toLowerCase().includes('help') || message.toLowerCase().includes('explain')) {
            title = 'Requested Help';
        }
        
        const description = message.length > 50 ? 
            message.substring(0, 50) + '...' : message;

        console.log('📊 DashboardManager available?', typeof DashboardManager !== 'undefined');
        
        // Track with DashboardManager if available
        if (typeof DashboardManager !== 'undefined' && DashboardManager.trackActivity) {
            console.log('✅ Calling DashboardManager.trackActivity');
            DashboardManager.trackActivity(
                'chat',
                title,
                description,
                subject,
                topic
            );
        } else {
            console.log('⏳ DashboardManager not ready, retrying in 100ms');
            // If DashboardManager is not available, try again after a short delay
            setTimeout(() => {
                if (typeof DashboardManager !== 'undefined' && DashboardManager.trackActivity) {
                    console.log('✅ Retry: Calling DashboardManager.trackActivity');
                    DashboardManager.trackActivity(
                        'chat',
                        title,
                        description,
                        subject,
                        topic
                    );
                } else {
                    console.log('❌ DashboardManager still not available after retry');
                }
            }, 100);
        }
        
        // Directly save to localStorage (backup method)
        const activity = JSON.parse(localStorage.getItem('userActivity') || '[]');
        const newActivity = {
            type: 'chat',
            title: title,
            description: description,
            time: 'just now',
            timestamp: new Date().toISOString(),
            subject: subject,
            topic: topic,
            icon: '💬'
        };
        
        activity.unshift(newActivity);
        if (activity.length > 20) {
            activity.splice(20);
        }
        localStorage.setItem('userActivity', JSON.stringify(activity));
        
        console.log('💾 Activity saved to localStorage:', newActivity); // Enhanced debug log
        console.log('📈 Total activities in localStorage:', activity.length);
        
        // Trigger dashboard refresh if function is available
        if (typeof window.refreshDashboard === 'function') {
            console.log('🔄 Calling refreshDashboard');
            window.refreshDashboard();
        } else {
            console.log('❌ refreshDashboard function not available');
        }
    }

    startTimeTracking() {
        console.log('⏱️ Starting time tracking system');
        this.sessionStartTime = new Date();
        this.lastActivityTime = new Date();
        
        // Track session time every second
        this.sessionTimer = setInterval(() => {
            this.updateSessionTime();
        }, 1000);

        // Track user activity to reset timeout
        this.setupActivityListeners();
        
        // Save session start
        this.saveTimeSession('start');
        
        // Save session end when page unloads
        window.addEventListener('beforeunload', () => {
            this.endTimeTracking();
        });
    }

    setupActivityListeners() {
        // Track various user activities to reset the timeout
        const activities = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
        
        activities.forEach(activity => {
            document.addEventListener(activity, () => {
                this.resetActivityTimeout();
            }, true);
        });
    }

    resetActivityTimeout() {
        this.lastActivityTime = new Date();
    }

    updateSessionTime() {
        const now = new Date();
        const timeSinceLastActivity = now - this.lastActivityTime;
        
        // If user has been inactive for more than 5 minutes, don't count this time
        if (timeSinceLastActivity < this.activityTimeout) {
            // User is active, count this second
            this.totalSessionTime += 1000; // Add 1 second in milliseconds
            
            // Update localStorage every 10 seconds to avoid too many writes
            if (this.totalSessionTime % 10000 === 0) {
                this.saveTimeSession('update');
            }
        }
    }

    saveTimeSession(action = 'update') {
        const sessions = JSON.parse(localStorage.getItem('studySessions') || '[]');
        const today = new Date().toDateString();
        
        let todaySession = sessions.find(s => s.date === today);
        
        if (!todaySession) {
            todaySession = {
                date: today,
                totalTime: 0, // in milliseconds
                sessions: []
            };
            sessions.push(todaySession);
        }
        
        if (action === 'start') {
            // Record session start
            todaySession.sessions.push({
                startTime: this.sessionStartTime.toISOString(),
                endTime: null,
                duration: 0
            });
        } else if (action === 'end') {
            // Update the last session with end time and duration
            const lastSession = todaySession.sessions[todaySession.sessions.length - 1];
            if (lastSession && !lastSession.endTime) {
                lastSession.endTime = new Date().toISOString();
                lastSession.duration = this.totalSessionTime;
                todaySession.totalTime += this.totalSessionTime;
            }
        } else {
            // Update ongoing session
            const lastSession = todaySession.sessions[todaySession.sessions.length - 1];
            if (lastSession && !lastSession.endTime) {
                lastSession.duration = this.totalSessionTime;
                // Update total time for today (sum of all completed sessions + current session)
                const completedTime = todaySession.sessions
                    .filter(s => s.endTime)
                    .reduce((total, s) => total + s.duration, 0);
                todaySession.totalTime = completedTime + this.totalSessionTime;
            }
        }
        
        localStorage.setItem('studySessions', JSON.stringify(sessions));
        
        if (action === 'end' || this.totalSessionTime % 30000 === 0) { // Log every 30 seconds
            console.log(`⏱️ Time session ${action}:`, {
                sessionTime: this.formatTime(this.totalSessionTime),
                todayTotal: this.formatTime(todaySession.totalTime),
                lastActivity: new Date(this.lastActivityTime).toLocaleTimeString()
            });
        }
    }

    endTimeTracking() {
        if (this.sessionTimer) {
            clearInterval(this.sessionTimer);
            this.sessionTimer = null;
        }
        this.saveTimeSession('end');
        console.log('⏱️ Time tracking ended');
    }

    formatTime(milliseconds) {
        const hours = Math.floor(milliseconds / (1000 * 60 * 60));
        const minutes = Math.floor((milliseconds % (1000 * 60 * 60)) / (1000 * 60));
        
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else if (minutes > 0) {
            return `${minutes}m`;
        } else {
            return '<1m';
        }
    }

    // Static method to get today's study time for dashboard
    static getTodayStudyTime() {
        const sessions = JSON.parse(localStorage.getItem('studySessions') || '[]');
        const today = new Date().toDateString();
        const todaySession = sessions.find(s => s.date === today);
        
        return todaySession ? todaySession.totalTime : 0;
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
