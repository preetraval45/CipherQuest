// ===== AI TUTOR JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
    initializeAITutor();
});

function initializeAITutor() {
    // Initialize chat functionality
    initializeChat();
    
    // Initialize voice controls
    initializeVoiceControls();
    
    // Initialize quick actions
    initializeQuickActions();
    
    // Initialize chat controls
    initializeChatControls();
    
    // Initialize typing effects
    initializeTypingEffects();
    
    // Initialize code copying
    initializeCodeCopying();
}

// ===== CHAT FUNCTIONALITY =====
function initializeChat() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendMessage');
    const chatMessages = document.getElementById('chatMessages');
    
    if (chatInput && sendButton) {
        // Auto-resize textarea
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
        
        // Send message on Enter (but allow Shift+Enter for new line)
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // Send message on button click
        sendButton.addEventListener('click', sendMessage);
    }
}

function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message
    addUserMessage(message);
    
    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Simulate AI response
    setTimeout(() => {
        hideTypingIndicator();
        generateAIResponse(message);
    }, 1500 + Math.random() * 2000);
}

function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-header">
                <span class="sender">You</span>
                <span class="timestamp">Just now</span>
            </div>
            <div class="message-text">
                <p>${escapeHtml(message)}</p>
            </div>
        </div>
        <div class="message-avatar">
            <i class="fas fa-user"></i>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    // Animate message in
    gsap.fromTo(messageDiv, {
        opacity: 0,
        x: 50,
        scale: 0.8
    }, {
        duration: 0.3,
        opacity: 1,
        x: 0,
        scale: 1,
        ease: 'back.out(1.7)'
    });
}

function generateAIResponse(userMessage) {
    const response = getAIResponse(userMessage);
    addAIMessage(response);
}

function addAIMessage(content) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai-message';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-header">
                <span class="sender">CyberSense AI</span>
                <span class="timestamp">Just now</span>
            </div>
            <div class="message-text">
                ${content}
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    // Animate message in
    gsap.fromTo(messageDiv, {
        opacity: 0,
        x: -50,
        scale: 0.8
    }, {
        duration: 0.3,
        opacity: 1,
        x: 0,
        scale: 1,
        ease: 'back.out(1.7)'
    });
    
    // Add typing effect to text content
    const textElement = messageDiv.querySelector('.message-text');
    typeText(textElement, content);
}

function typeText(element, content) {
    element.innerHTML = '';
    const words = content.split(' ');
    let currentIndex = 0;
    
    function typeNextWord() {
        if (currentIndex < words.length) {
            element.innerHTML += words[currentIndex] + ' ';
            currentIndex++;
            setTimeout(typeNextWord, 50 + Math.random() * 100);
        }
    }
    
    typeNextWord();
}

// ===== VOICE CONTROLS =====
function initializeVoiceControls() {
    const voiceToggle = document.getElementById('voiceToggle');
    let isListening = false;
    let recognition = null;
    
    // Check if speech recognition is supported
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('chatInput').value = transcript;
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            voiceToggle.classList.remove('active');
        };
        
        recognition.onend = function() {
            isListening = false;
            voiceToggle.classList.remove('active');
        };
    }
    
    if (voiceToggle) {
        voiceToggle.addEventListener('click', function() {
            if (!recognition) {
                showMessage('Speech recognition not supported in this browser', 'error');
                return;
            }
            
            if (isListening) {
                recognition.stop();
                isListening = false;
                this.classList.remove('active');
            } else {
                recognition.start();
                isListening = true;
                this.classList.add('active');
                showMessage('Listening... Speak now!', 'info');
            }
        });
    }
}

// ===== QUICK ACTIONS =====
function initializeQuickActions() {
    const quickActionButtons = document.querySelectorAll('.quick-action-btn');
    
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const prompt = this.dataset.prompt;
            if (prompt) {
                document.getElementById('chatInput').value = prompt;
                sendMessage();
            }
        });
    });
}

// ===== CHAT CONTROLS =====
function initializeChatControls() {
    const clearChatBtn = document.getElementById('clearChat');
    const exportChatBtn = document.getElementById('exportChat');
    
    if (clearChatBtn) {
        clearChatBtn.addEventListener('click', clearChat);
    }
    
    if (exportChatBtn) {
        exportChatBtn.addEventListener('click', exportChat);
    }
}

function clearChat() {
    const chatMessages = document.getElementById('chatMessages');
    const messages = chatMessages.querySelectorAll('.message:not(:first-child)');
    
    gsap.to(messages, {
        duration: 0.3,
        opacity: 0,
        x: -100,
        stagger: 0.05,
        ease: 'power2.in',
        onComplete: () => {
            messages.forEach(msg => msg.remove());
            showMessage('Chat cleared successfully', 'success');
        }
    });
}

function exportChat() {
    const chatMessages = document.getElementById('chatMessages');
    const messages = chatMessages.querySelectorAll('.message');
    let exportText = 'CipherQuest AI Tutor Chat Export\n';
    exportText += 'Generated on: ' + new Date().toLocaleString() + '\n\n';
    
    messages.forEach(message => {
        const sender = message.querySelector('.sender').textContent;
        const text = message.querySelector('.message-text').textContent;
        exportText += `${sender}: ${text}\n\n`;
    });
    
    // Create download link
    const blob = new Blob([exportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'cipherquest-chat.txt';
    a.click();
    URL.revokeObjectURL(url);
    
    showMessage('Chat exported successfully', 'success');
}

// ===== TYPING EFFECTS =====
function initializeTypingEffects() {
    // Typing indicator animation
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        const dots = typingIndicator.querySelectorAll('.typing-dots span');
        dots.forEach((dot, index) => {
            gsap.to(dot, {
                duration: 0.6,
                y: -10,
                ease: 'power2.inOut',
                repeat: -1,
                yoyo: true,
                delay: index * 0.2
            });
        });
    }
}

function showTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.style.display = 'flex';
        gsap.fromTo(typingIndicator, {
            opacity: 0,
            y: 20
        }, {
            duration: 0.3,
            opacity: 1,
            y: 0,
            ease: 'power2.out'
        });
        scrollToBottom();
    }
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        gsap.to(typingIndicator, {
            duration: 0.3,
            opacity: 0,
            y: 20,
            ease: 'power2.in',
            onComplete: () => {
                typingIndicator.style.display = 'none';
            }
        });
    }
}

// ===== CODE COPYING =====
function initializeCodeCopying() {
    document.addEventListener('click', function(e) {
        if (e.target.closest('.copy-btn')) {
            const copyBtn = e.target.closest('.copy-btn');
            const codeBlock = copyBtn.closest('.code-block');
            const code = codeBlock.querySelector('code').textContent;
            
            navigator.clipboard.writeText(code).then(() => {
                // Show success feedback
                const originalIcon = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                copyBtn.style.color = 'var(--primary-color)';
                
                setTimeout(() => {
                    copyBtn.innerHTML = originalIcon;
                    copyBtn.style.color = '';
                }, 2000);
            });
        }
    });
}

// ===== AI RESPONSE GENERATOR =====
function getAIResponse(userMessage) {
    const message = userMessage.toLowerCase();
    
    // Simple response system (in real app, this would connect to an AI API)
    if (message.includes('sql injection')) {
        return `
            <p>Great question! SQL injection is a critical web security vulnerability. Let me explain:</p>
            
            <h4>What is SQL Injection?</h4>
            <p>SQL injection occurs when an attacker inserts malicious SQL code into input fields, tricking the application into executing unintended database commands.</p>
            
            <h4>Basic Example:</h4>
            <div class="code-block">
                <div class="code-header">
                    <span>Vulnerable Query</span>
                    <button class="copy-btn">
                        <i class="fas fa-copy"></i>
                    </button>
                </div>
                <pre><code>SELECT * FROM users WHERE username = '$input' AND password = '$password'</code></pre>
            </div>
            
            <h4>Attack Vector:</h4>
            <p>If a user enters: <code>' OR '1'='1</code></p>
            <p>The query becomes: <code>SELECT * FROM users WHERE username = '' OR '1'='1' AND password = '$password'</code></p>
            
            <p>This would return all users because <code>'1'='1'</code> is always true!</p>
            
            <h4>Prevention:</h4>
            <ul>
                <li>Use parameterized queries</li>
                <li>Input validation and sanitization</li>
                <li>Least privilege database accounts</li>
                <li>Web Application Firewalls (WAF)</li>
            </ul>
            
            <p>Would you like me to show you some practical examples or help you practice this in our CTF labs?</p>
        `;
    } else if (message.includes('xss')) {
        return `
            <p>Cross-Site Scripting (XSS) is another critical web vulnerability. Here's what you need to know:</p>
            
            <h4>What is XSS?</h4>
            <p>XSS allows attackers to inject malicious scripts into web pages viewed by other users.</p>
            
            <h4>Types of XSS:</h4>
            <ul>
                <li><strong>Reflected XSS:</strong> Script is reflected off the web server</li>
                <li><strong>Stored XSS:</strong> Script is stored on the server</li>
                <li><strong>DOM-based XSS:</strong> Script is executed in the browser</li>
            </ul>
            
            <h4>Example:</h4>
            <div class="code-block">
                <div class="code-header">
                    <span>Vulnerable Code</span>
                    <button class="copy-btn">
                        <i class="fas fa-copy"></i>
                    </button>
                </div>
                <pre><code>&lt;div&gt;Hello, &lt;?php echo $_GET['name']; ?&gt;&lt;/div&gt;</code></pre>
            </div>
            
            <p>If someone visits: <code>?name=&lt;script&gt;alert('XSS')&lt;/script&gt;</code></p>
            
            <p>Want to learn more about XSS prevention techniques?</p>
        `;
    } else if (message.includes('cryptography') || message.includes('crypto')) {
        return `
            <p>Cryptography is fascinating! It's the science of securing information through mathematical techniques.</p>
            
            <h4>Key Concepts:</h4>
            <ul>
                <li><strong>Symmetric Encryption:</strong> Same key for encryption and decryption</li>
                <li><strong>Asymmetric Encryption:</strong> Public/private key pairs</li>
                <li><strong>Hashing:</strong> One-way transformation of data</li>
                <li><strong>Digital Signatures:</strong> Verify authenticity and integrity</li>
            </ul>
            
            <h4>Common Algorithms:</h4>
            <ul>
                <li>AES (Advanced Encryption Standard)</li>
                <li>RSA (Rivest-Shamir-Adleman)</li>
                <li>SHA-256 (Secure Hash Algorithm)</li>
                <li>ECC (Elliptic Curve Cryptography)</li>
            </ul>
            
            <p>Would you like to explore any specific cryptographic concept or try some crypto challenges?</p>
        `;
    } else {
        return `
            <p>I'm here to help you with cybersecurity! Here are some topics I can assist with:</p>
            
            <ul>
                <li><strong>Web Security:</strong> SQL injection, XSS, CSRF, authentication</li>
                <li><strong>Network Security:</strong> Penetration testing, vulnerability scanning</li>
                <li><strong>Cryptography:</strong> Encryption, hashing, digital signatures</li>
                <li><strong>Forensics:</strong> Digital evidence analysis, incident response</li>
                <li><strong>Reverse Engineering:</strong> Malware analysis, binary analysis</li>
            </ul>
            
            <p>Just ask me about any of these topics, or use the quick action buttons on the right!</p>
        `;
    }
}

// ===== UTILITY FUNCTIONS =====
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showMessage(message, type) {
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `ai-message ${type}`;
    messageDiv.innerHTML = `
        <i class="fas fa-${getMessageIcon(type)}"></i>
        <span>${message}</span>
    `;
    
    // Add to page
    const aiTutorContent = document.querySelector('.ai-tutor-content');
    aiTutorContent.appendChild(messageDiv);
    
    // Animate in
    gsap.fromTo(messageDiv, {
        opacity: 0,
        y: -20
    }, {
        duration: 0.3,
        opacity: 1,
        y: 0,
        ease: 'power2.out'
    });
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        gsap.to(messageDiv, {
            duration: 0.3,
            opacity: 0,
            y: -20,
            ease: 'power2.in',
            onComplete: () => messageDiv.remove()
        });
    }, 3000);
}

function getMessageIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-circle';
        case 'info': return 'info-circle';
        default: return 'info-circle';
    }
}

// ===== EXPORT FOR MODULE USE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeAITutor,
        sendMessage,
        generateAIResponse,
        clearChat,
        exportChat
    };
} 