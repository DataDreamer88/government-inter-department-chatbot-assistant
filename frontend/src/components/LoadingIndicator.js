// frontend/src/components/LoadingIndicator.js
import React from 'react';
import './LoadingIndicator.css';

const LoadingIndicator = () => {
  return (
    <div className="loading-indicator">
      <div className="loading-avatar">🤖</div>
      <div className="loading-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <div className="loading-text">Analyzing data from data.gov.in...</div>
    </div>
  );
};

export default LoadingIndicator;