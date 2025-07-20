import React, { useState, useRef, useEffect } from 'react';
import './AIAssistantPage.css';

const MODEL_OPTIONS = [
  { label: 'GPT-3.5 Turbo', value: 'gpt-3.5-turbo' },
  { label: 'GPT-4', value: 'gpt-4' },
];

const DEFAULT_MODEL = 'gpt-3.5-turbo';
const DEFAULT_TEMPERATURE = 0.7;

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
  const [error, setError] = useState(null);
  const [model, setModel] = useState(DEFAULT_MODEL);
  const [temperature, setTemperature] = useState(DEFAULT_TEMPERATURE);
  const [streaming, setStreaming] = useState(false);
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
    if (!inputMessage.trim() || isTyping) return;
    setError(null);

    const userMessage = {
      id: Date.now(),
      content: inputMessage,
      timestamp: new Date(),
      type: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: userMessage.content,
          model,
          temperature,
          stream: streaming
        })
      });
      const data = await response.json();
      if (!response.ok || data.error) {
        setError(data.error || 'An error occurred.');
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          content: `❌ ${data.error || 'An error occurred.'}`,
          timestamp: new Date(),
          type: 'ai'
        }]);
      } else {
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          content: data.response,
          timestamp: new Date(),
          type: 'ai'
        }]);
      }
    } catch (err) {
      setError('Network error. Please try again.');
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        content: '❌ Network error. Please try again.',
        timestamp: new Date(),
        type: 'ai'
      }]);
    } finally {
      setIsTyping(false);
    }
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

  const handleClearChat = () => {
    setMessages([
      {
        id: 1,
        content: "Hello! I'm your CyberAI Tutor. I can help you learn about cybersecurity, cryptography, web security, and more. What would you like to know?",
        timestamp: new Date(),
        type: 'ai'
      }
    ]);
    setError(null);
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
          <button className="control-btn" title="Export Chat" disabled>
            📥
          </button>
          <button className="control-btn" title="Clear Chat" onClick={handleClearChat}>
            🗑️
          </button>
        </div>
      </div>

      {/* Settings */}
      <div className="ai-settings glass-effect">
        <div className="setting-group">
          <label htmlFor="model-select">Model:</label>
          <select
            id="model-select"
            value={model}
            onChange={e => setModel(e.target.value)}
            disabled={isTyping}
          >
            {MODEL_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>
        <div className="setting-group">
          <label htmlFor="temperature-range">Temperature: {temperature}</label>
          <input
            id="temperature-range"
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={temperature}
            onChange={e => setTemperature(Number(e.target.value))}
            disabled={isTyping}
          />
        </div>
        <div className="setting-group">
          <label htmlFor="streaming-checkbox">Streaming:</label>
          <input
            id="streaming-checkbox"
            type="checkbox"
            checked={streaming}
            onChange={e => setStreaming(e.target.checked)}
            disabled={isTyping}
          />
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        {quickActions.map((action) => (
          <button
            key={`action-${action}`}
            className="quick-action-btn"
            onClick={() => handleQuickAction(action)}
            disabled={isTyping}
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

      {/* Error Message */}
      {error && (
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <div className="error-message">{error}</div>
        </div>
      )}

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
            disabled={isTyping}
          />
          <div className="input-actions">
            <button
              className={`voice-btn ${isListening ? 'listening' : ''}`}
              onClick={handleVoiceInput}
              title="Voice Input"
              disabled={isTyping}
            >
              {isListening ? '🔴' : '🎤'}
            </button>
            <button
              className="send-btn"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isTyping}
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