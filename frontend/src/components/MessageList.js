// frontend/src/components/MessageList.js
import React from 'react';
import ReactMarkdown from 'react-markdown';
import SourceCitation from './SourceCitation';
import './MessageList.css';

const MessageList = ({ messages }) => {
  const formatTimestamp = (date) => {
    return new Date(date).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="message-list">
      {messages.map((message) => (
        <div key={message.id} className={`message message-${message.type}`}>
          <div className="message-content">
            {message.type === 'user' && (
              <div className="message-avatar user-avatar">👤</div>
            )}
            {message.type === 'bot' && (
              <div className="message-avatar bot-avatar">🤖</div>
            )}
            {message.type === 'system' && (
              <div className="message-avatar system-avatar">ℹ️</div>
            )}
            {message.type === 'error' && (
              <div className="message-avatar error-avatar">⚠️</div>
            )}

            <div className="message-body">
              <div className="message-text">
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
              
              {message.sources && message.sources.length > 0 && (
                <div className="message-sources">
                  <h4>📚 Data Sources:</h4>
                  {message.sources.map((source, index) => (
                    <SourceCitation key={index} source={source} index={index} />
                  ))}
                </div>
              )}

              {message.queryInfo && message.queryInfo.query_type && (
                <div className="query-info">
                  <small>
                    Query Type: {message.queryInfo.query_type} | 
                    {message.queryInfo.states?.length > 0 && 
                      ` States: ${message.queryInfo.states.join(', ')}`}
                    {message.queryInfo.crops?.length > 0 && 
                      ` | Crops: ${message.queryInfo.crops.join(', ')}`}
                  </small>
                </div>
              )}

              <div className="message-timestamp">
                {formatTimestamp(message.timestamp)}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;