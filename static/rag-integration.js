/**
 * RAG Integration Module for Edu Assist
 * This extends the existing Edu Assist functionality without breaking it
 */

class RAGIntegration {
    constructor(eduAssist) {
        this.eduAssist = eduAssist;
        this.apiBaseUrl = 'http://localhost:8000/api';
        this.sessionId = null;
        this.ragEnabled = false;
        
        this.init();
    }
    
    async init() {
        // Check if backend is available
        this.ragEnabled = await this.checkBackendHealth();
        
        if (this.ragEnabled) {
            console.log('🤖 RAG backend connected successfully!');
            this.setupRAGFeatures();
        } else {
            console.log('📱 Running in offline mode - using built-in responses');
        }
    }
    
    async checkBackendHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`, { 
                method: 'GET',
                timeout: 3000 
            });
            return response.ok;
        } catch (error) {
            return false;
        }
    }
    
    setupRAGFeatures() {
        // Add PDF upload functionality to existing attach button
        this.enhanceAttachButton();
        
        // Override the existing sendMessage method to use RAG when available
        this.enhanceSendMessage();
        
        // Add visual indicators for RAG features
        this.addRAGIndicators();
    }
    
    enhanceAttachButton() {
        const attachBtn = document.querySelector('.attach-btn');
        if (!attachBtn) return;
        
        // Create hidden file input
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.pdf';
        fileInput.style.display = 'none';
        fileInput.id = 'rag-file-input';
        document.body.appendChild(fileInput);
        
        // Add click handler to attach button
        const originalHandler = attachBtn.onclick;
        attachBtn.onclick = (e) => {
            if (this.ragEnabled) {
                fileInput.click();
            } else if (originalHandler) {
                originalHandler(e);
            }
        };
        
        // Handle file selection
        fileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (file) {
                await this.uploadPDF(file);
            }
        });
        
        // Add tooltip to show PDF upload is available
        if (this.ragEnabled) {
            attachBtn.title = 'Upload PDF document';
            attachBtn.style.color = 'var(--primary-color)';
        }
    }
    
    enhanceSendMessage() {
        // Store reference to original method
        const originalSendMessage = this.eduAssist.sendMessage.bind(this.eduAssist);
        
        // Override with RAG-enhanced version
        this.eduAssist.sendMessage = async () => {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Clear input and add user message (same as original)
            input.value = '';
            this.eduAssist.addMessage('student', message);
            
            if (this.ragEnabled) {
                // Use RAG backend
                await this.sendToRAG(message);
            } else {
                // Fall back to original behavior
                setTimeout(() => {
                    this.eduAssist.generateAIResponse(message);
                }, 1000);
            }
        };
    }
    
    async sendToRAG(message) {
        // Show typing indicator
        const typingIndicator = this.showTypingIndicator();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    subject: this.eduAssist.currentSubject || 'General',
                    eli5_mode: this.eduAssist.eli5Mode || false,
                    session_id: this.sessionId
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.sessionId = data.session_id;
                
                // Remove typing indicator
                this.removeTypingIndicator(typingIndicator);
                
                // Add AI response with sources
                this.addRAGMessage(data.response, data.sources);
            } else {
                throw new Error('Backend error');
            }
            
        } catch (error) {
            console.error('RAG error:', error);
            
            // Remove typing indicator
            this.removeTypingIndicator(typingIndicator);
            
            // Fall back to original behavior
            this.eduAssist.generateAIResponse(message);
            
            // Show subtle error indicator
            this.showRAGError();
        }
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
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return typingDiv;
    }
    
    removeTypingIndicator(indicator) {
        if (indicator && indicator.parentNode) {
            indicator.parentNode.removeChild(indicator);
        }
    }
    
    addRAGMessage(response, sources = []) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ai-message';
        
        let sourcesHtml = '';
        if (sources && sources.length > 0) {
            sourcesHtml = `
                <div class="rag-sources">
                    <small><strong>Sources:</strong></small>
                    ${sources.map(source => `
                        <div class="source-tag">
                            <span class="source-type">[${source.type}]</span>
                            <span class="source-name">${source.source}</span>
                            ${source.url ? `<a href="${source.url}" target="_blank">🔗</a>` : ''}
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <span class="material-icons">smart_toy</span>
                ${this.ragEnabled ? '<div class="rag-indicator">🧠</div>' : ''}
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <p>${response}</p>
                    ${sourcesHtml}
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
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Update XP (keeping existing behavior)
        if (this.eduAssist.updateXP) {
            // No XP for RAG responses to maintain balance
        }
    }
    
    async uploadPDF(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('subject', this.eduAssist.currentSubject || 'General');
            
            // Show upload status
            this.eduAssist.showToast(`📄 Uploading ${file.name}...`);
            
            const response = await fetch(`${this.apiBaseUrl}/upload-document`, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                this.eduAssist.showToast(`✅ ${file.name} processed! ${result.chunks_count} sections ready.`);
                
                // Add a message to chat
                this.eduAssist.addMessage('ai', `📚 I've processed "${file.name}" and can now answer questions about it! What would you like to know?`);
            } else {
                throw new Error('Upload failed');
            }
            
        } catch (error) {
            console.error('Upload error:', error);
            this.eduAssist.showToast('❌ Upload failed. Please try again.');
        }
    }
    
    addRAGIndicators() {
        // Add subtle indicator that RAG is active
        const logo = document.querySelector('.logo h1');
        if (logo && this.ragEnabled) {
            logo.style.position = 'relative';
            const indicator = document.createElement('span');
            indicator.innerHTML = '🧠';
            indicator.style.cssText = `
                position: absolute;
                top: -5px;
                right: -20px;
                font-size: 12px;
                opacity: 0.7;
                title: 'RAG mode active';
            `;
            logo.appendChild(indicator);
        }
        
        // Update attach button appearance
        const attachBtn = document.querySelector('.attach-btn');
        if (attachBtn && this.ragEnabled) {
            attachBtn.classList.add('rag-enabled');
        }
    }
    
    showRAGError() {
        // Subtle indication that we fell back to local mode
        const indicator = document.createElement('div');
        indicator.innerHTML = '📱 Offline mode';
        indicator.style.cssText = `
            position: fixed;
            top: 70px;
            right: 20px;
            background: #ff9800;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1001;
            opacity: 0.8;
        `;
        
        document.body.appendChild(indicator);
        setTimeout(() => {
            if (document.body.contains(indicator)) {
                document.body.removeChild(indicator);
            }
        }, 3000);
    }
}

// Auto-initialize when page loads, but only if Edu Assist exists
document.addEventListener('DOMContentLoaded', () => {
    // Wait a moment for original Edu Assist to initialize
    setTimeout(() => {
        if (window.eduAssistInstance) {
            window.ragIntegration = new RAGIntegration(window.eduAssistInstance);
        }
    }, 1000);
});

// CSS for RAG features
const ragStyles = document.createElement('style');
ragStyles.textContent = `
    .rag-indicator {
        position: absolute;
        bottom: -2px;
        right: -2px;
        font-size: 10px;
        background: var(--primary-color);
        color: white;
        border-radius: 50%;
        width: 16px;
        height: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .rag-sources {
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid var(--border-color);
        font-size: 11px;
    }
    
    .source-tag {
        display: flex;
        align-items: center;
        gap: 4px;
        margin: 2px 0;
    }
    
    .source-type {
        background: var(--primary-color);
        color: white;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 9px;
        font-weight: 500;
    }
    
    .source-name {
        flex: 1;
        opacity: 0.8;
    }
    
    .attach-btn.rag-enabled {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .typing-animation {
        display: flex;
        gap: 3px;
        align-items: center;
    }
    
    .typing-animation span {
        width: 6px;
        height: 6px;
        background: var(--text-secondary);
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-animation span:nth-child(1) { animation-delay: -0.32s; }
    .typing-animation span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
`;
document.head.appendChild(ragStyles);
