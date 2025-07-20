class ChatApp {
    constructor() {
        this.apiUrl = 'http://localhost:5122';
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.showTypingIndicator();
        this.setInputDisabled(true);
        
        try {
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.status === 'success') {
                if (data.type === 'report') {
                    this.addReportMessage(data.message, data.report_data);
                } else {
                    this.addMessage(data.message, 'bot');
                }
            } else {
                this.addMessage('Sorry, I encountered an error processing your request.', 'bot');
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('Sorry, I\'m having trouble connecting to the server. Please make sure the backend service is running.', 'bot');
        } finally {
            this.hideTypingIndicator();
            this.setInputDisabled(false);
            this.messageInput.focus();
        }
    }
    
    addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="message-content">
                    ${this.escapeHtml(message)}
                    <i class="fas fa-user ms-2"></i>
                </div>
                <small class="message-time">${currentTime}</small>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <i class="fas fa-robot me-2"></i>
                    ${this.escapeHtml(message)}
                </div>
                <small class="message-time">${currentTime}</small>
            `;
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addReportMessage(message, reportData) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message report-message';
        
        const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const summary = reportData.summary || {};
        
        messageDiv.innerHTML = `
            <div class="message-content report-content">
                <div class="report-header">
                    <i class="fas fa-chart-line me-2"></i>
                    <strong>Sustainability Report Generated</strong>
                </div>
                
                <div class="report-summary">
                    ${summary.sustainability_score !== 'N/A' ? 
                        `<div class="score-badge">
                            <span class="score-label">Sustainability Score:</span>
                            <span class="score-value">${summary.sustainability_score}/100</span>
                        </div>` : ''
                    }
                    ${summary.data_points_analyzed !== 'N/A' ? 
                        `<div class="data-points">
                            <i class="fas fa-database me-1"></i>
                            ${summary.data_points_analyzed} data points analyzed
                        </div>` : ''
                    }
                </div>
                
                <div class="report-analysis">
                    ${this.escapeHtml(message)}
                </div>
                
                ${summary.key_recommendations && summary.key_recommendations.length > 0 ? `
                    <div class="recommendations">
                        <strong><i class="fas fa-lightbulb me-1"></i>Key Recommendations:</strong>
                        <ul>
                            ${summary.key_recommendations.map(rec => `<li>${this.escapeHtml(rec)}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                <div class="report-actions">
                    <button class="btn btn-sm btn-outline-success" onclick="this.downloadReport('${reportData.generated_at}')">
                        <i class="fas fa-download me-1"></i>Download Report
                    </button>
                    <button class="btn btn-sm btn-outline-info" onclick="this.viewDetailedData('${reportData.generated_at}')">
                        <i class="fas fa-eye me-1"></i>View Details
                    </button>
                </div>
            </div>
            <small class="message-time">${currentTime}</small>
        `;
        
        // Store report data for later access
        messageDiv.reportData = reportData;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'block';
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    setInputDisabled(disabled) {
        this.messageInput.disabled = disabled;
        this.sendBtn.disabled = disabled;
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;")
            .replace(/\n/g, "<br>");
    }
    
    async checkBackendHealth() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            if (response.ok) {
                console.log('Backend service is healthy');
                return true;
            }
        } catch (error) {
            console.warn('Backend service is not available:', error);
        }
        return false;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const chatApp = new ChatApp();
    chatApp.checkBackendHealth();
});