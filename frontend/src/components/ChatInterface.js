// frontend/src/components/ChatInterface.js
import React, { useState, useEffect, useRef } from 'react';
import MessageList from './MessageList';
import InputBox from './InputBox';
import LoadingIndicator from './LoadingIndicator';
import './ChatInterface.css';
import { api } from '../services/api';

const ChatInterface = ({ onStatsUpdate }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'system',
      content: '🌾 Welcome to Project Samarth! I can help you analyze India\'s agricultural economy and climate data from data.gov.in. Ask me anything about crop production, rainfall patterns, or their correlations!',
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Listen for example query events
  useEffect(() => {
    const handleExampleQuery = (event) => {
      handleSendMessage(event.detail);
    };

    window.addEventListener('exampleQuery', handleExampleQuery);
    return () => window.removeEventListener('exampleQuery', handleExampleQuery);
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (text) => {
    if (!text.trim() || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: text,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Send query to backend
      const response = await api.sendQuery(text);

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.answer,
        sources: response.sources,
        queryInfo: response.query_info,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);

      // Update stats
      if (onStatsUpdate) {
        onStatsUpdate();
      }
    } catch (error) {
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: `Error: ${error.message}. Please check if the backend server is running.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([{
      id: 1,
      type: 'system',
      content: 'Chat cleared. How can I help you with agricultural data today?',
      timestamp: new Date()
    }]);
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-header-content">
          <h2>🌾 Agricultural Data Assistant</h2>
          <button onClick={handleClearChat} className="clear-button">
            Clear Chat
          </button>
        </div>
      </div>

      <div className="chat-messages">
        <MessageList messages={messages} />
        {isLoading && <LoadingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <InputBox onSend={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default ChatInterface;