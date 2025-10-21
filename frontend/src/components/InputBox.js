// frontend/src/components/
import React, { useState, useRef, useEffect } from 'react';
import './InputBox.css';

const InputBox = ({ onSend, isLoading }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [input]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSend(input);
      setInput('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="input-box">
      <textarea
        ref={textareaRef}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask about crop production, rainfall patterns, or their correlation..."
        disabled={isLoading}
        rows={1}
        className="input-textarea"
      />
      <button
        type="submit"
        disabled={!input.trim() || isLoading}
        className="send-button"
      >
        {isLoading ? '⏳' : '🚀'}
      </button>
    </form>
  );
};

export default InputBox;