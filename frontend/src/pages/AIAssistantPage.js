import React, { useState, useRef, useEffect } from 'react';
import './AIAssistantPage.css';

const AIAssistantPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      content: "Hello! I'm your CyberAI Tutor. I can help you learn about cybersecurity, cryptography, web security, and more. What would you like to know?",
      timestamp: new Date(),
      type: 'ai'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef(null);

  const quickActions = [
    'Explain encryption',
    'What is SQL injection?',
    'Tell me about XSS',
    'Network security basics',
    'CTF challenges'
  ];

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      content: inputMessage,
      timestamp: new Date(),
      type: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate AI response delay
    setTimeout(() => {
      const aiResponse = generateAIResponse(inputMessage);
      setMessages(prev => [...prev, aiResponse]);
      setIsTyping(false);
    }, 1500);
  };

  const generateAIResponse = (userInput) => {
    const responses = {
      'encryption': {
        content: `**Encryption** is the process of converting plain text into ciphertext to protect sensitive information.\n\n**Types of Encryption:**\n• **Symmetric**: Same key for encryption/decryption (AES, DES)\n• **Asymmetric**: Public/private key pairs (RSA, ECC)\n\n**Example (Caesar Cipher):**\n\`\`\`python\n# Simple Caesar cipher implementation\ndef caesar_encrypt(text, shift):\n    result = ""\n    for char in text:\n        if char.isalpha():\n            ascii_offset = 65 if char.isupper() else 97\n            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)\n        else:\n            result += char\n    return result\n\`\`\``,
        type: 'ai'
      },
      'sql injection': {
        content: `**SQL Injection** is a code injection technique that exploits vulnerabilities in database queries.\n\n**Common Types:**\n• Union-based\n• Boolean-based\n• Time-based\n• Error-based\n\n**Prevention:**\n• Use parameterized queries\n• Input validation\n• Least privilege principle\n• WAF (Web Application Firewall)\n\n**Example Prevention:**\n\`\`\`python\n# Vulnerable code\nquery = f"SELECT * FROM users WHERE id = {user_input}"\n\n# Secure code\nquery = "SELECT * FROM users WHERE id = %s"\ncursor.execute(query, (user_input,))\n\`\`\``,
        type: 'ai'
      },
      'xss': {
        content: `**Cross-Site Scripting (XSS)** allows attackers to inject malicious scripts into web pages.\n\n**Types:**\n• **Reflected XSS**: Script reflected in response\n• **Stored XSS**: Script stored in database\n• **DOM XSS**: Script executed in DOM\n\n**Prevention:**\n• Input sanitization\n• Output encoding\n• Content Security Policy (CSP)\n• HttpOnly cookies\n\n**Example:**\n\`\`\`html\n<!-- Vulnerable -->\n<div id="user-input">${userInput}</div>\n\n<!-- Secure -->\n<div id="user-input">${userInput.replace(/[&<>"']/g, (match) => {\n  const escapeMap = {\n    '&': '&amp;',\n    '<': '&lt;',\n    '>': '&gt;',\n    '"': '&quot;',\n    "'": '&#39;'\n  };\n  return escapeMap[match];\n})}</div>\n\`\`\``,
        type: 'ai'
      },
      'network security': {
        content: `**Network Security** protects network infrastructure and data from unauthorized access.\n\n**Key Concepts:**\n• **Firewalls**: Control traffic flow\n• **VPNs**: Secure remote access\n• **IDS/IPS**: Intrusion detection/prevention\n• **Encryption**: Data protection\n\n**Common Threats:**\n• Man-in-the-Middle attacks\n• DDoS attacks\n• Packet sniffing\n• ARP spoofing\n\n**Best Practices:**\n• Regular security updates\n• Network segmentation\n• Access control\n• Monitoring and logging`,
        type: 'ai'
      },
      'ctf': {
        content: `**Capture The Flag (CTF)** challenges test cybersecurity skills in a competitive environment.\n\n**Challenge Types:**\n• **Web**: Web application vulnerabilities\n• **Forensics**: File analysis and recovery\n• **Crypto**: Cryptography challenges\n• **Pwn**: Binary exploitation\n• **Reverse**: Reverse engineering\n\n**Example Challenge:**\n\`\`\`\nFlag format: CTF{...}\nChallenge: Decrypt this message\nCiphertext: "KHOOR ZRUOG"\nHint: Think about shifting letters\n\`\`\`\n\n**Tools:**\n• Burp Suite (Web)\n• Wireshark (Network)\n• Ghidra (Reverse)\n• CyberChef (Crypto)`,
        type: 'ai'
      }
    };

    const lowerInput = userInput.toLowerCase();
    for (const [key, response] of Object.entries(responses)) {
      if (lowerInput.includes(key)) {
        return {
          id: Date.now(),
          content: response.content,
          timestamp: new Date(),
          type: response.type
        };
      }
    }

    // Default response
    return {
      id: Date.now(),
      content: `I understand you're asking about "${userInput}". This is a great cybersecurity topic! Let me provide you with some information and resources to help you learn more.\n\n**Key Points:**\n• Always practice ethical hacking\n• Stay updated with latest threats\n• Use proper tools and techniques\n• Follow responsible disclosure\n\nWould you like me to elaborate on any specific aspect of this topic?`,
      timestamp: new Date(),
      type: 'ai'
    };
  };

  const handleQuickAction = (action) => {
    setInputMessage(action);
  };

  const handleVoiceInput = () => {
    setIsListening(!isListening);
    // In a real app, this would integrate with Web Speech API
    if (!isListening) {
      // Simulate voice input
      setTimeout(() => {
        setInputMessage('Explain network security');
        setIsListening(false);
      }, 2000);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatMessage = (content) => {
    // Simple markdown-like formatting
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br>');
  };

  return (
    <div className="ai-assistant-page">
      {/* Header */}
      <div className="ai-header glass-effect">
        <div className="ai-header-content">
          <div className="ai-avatar">
            <span className="ai-icon">🤖</span>
          </div>
          <div className="ai-info">
            <h2 className="ai-name">CyberAI Tutor</h2>
            <p className="ai-status">
              {isTyping ? 'Typing...' : 'Online'}
            </p>
          </div>
        </div>
        <div className="ai-controls">
          <button className="control-btn" title="Export Chat">
            📥
          </button>
          <button className="control-btn" title="Clear Chat">
            🗑️
          </button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        {quickActions.map((action) => (
          <button
            key={`action-${action}`}
            className="quick-action-btn"
            onClick={() => handleQuickAction(action)}
          >
            {action}
          </button>
        ))}
      </div>

      {/* Chat Container */}
      <div className="chat-container glass-effect">
        <div className="messages-container">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.type}`}
            >
              <div className="message-avatar">
                {message.type === 'ai' ? '🤖' : '👤'}
              </div>
              <div className="message-content">
                <div 
                  className="message-text"
                  dangerouslySetInnerHTML={{ 
                    __html: formatMessage(message.content) 
                  }}
                />
                <div className="message-timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="message ai">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="input-container glass-effect">
        <div className="input-wrapper">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything about cybersecurity..."
            className="message-input"
            rows="1"
          />
          <div className="input-actions">
            <button
              className={`voice-btn ${isListening ? 'listening' : ''}`}
              onClick={handleVoiceInput}
              title="Voice Input"
            >
              {isListening ? '🔴' : '🎤'}
            </button>
            <button
              className="send-btn"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim()}
            >
              ➤
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAssistantPage; 