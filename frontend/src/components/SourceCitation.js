// frontend/src/components/SourceCitation.js
import React, { useState } from 'react';
import './SourceCitation.css';

const SourceCitation = ({ source, index }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="source-citation">
      <div 
        className="source-header"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="source-info">
          <span className="source-number">[{index + 1}]</span>
          <span className="source-title">{source.source}</span>
          <span className="source-relevance">
            Relevance: {(source.relevance * 100).toFixed(1)}%
          </span>
        </div>
        <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
      </div>

      {isExpanded && (
        <div className="source-details">
          <div className="source-type">
            <strong>Type:</strong> {source.type}
          </div>
          <div className="source-content">
            <strong>Content:</strong>
            <p>{source.text}</p>
          </div>
          {source.metadata && (
            <div className="source-metadata">
              <strong>Metadata:</strong>
              <pre>{JSON.stringify(source.metadata, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SourceCitation;