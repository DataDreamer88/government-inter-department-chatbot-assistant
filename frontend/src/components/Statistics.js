// frontend/src/components/Statistics.js
import React from 'react';
import './Statistics.css';

const Statistics = ({ stats }) => {
  if (!stats) return null;

  return (
    <div className="statistics-panel">
      <h3 className="stats-title">📊 System Statistics</h3>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Documents Indexed</div>
          <div className="stat-value">
            {stats.vector_store?.total_documents || 0}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Vector Dimension</div>
          <div className="stat-value">
            {stats.vector_store?.embedding_dimension || 0}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Cache Size</div>
          <div className="stat-value">
            {stats.cache?.size || 0}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">System Status</div>
          <div className={`stat-status ${stats.is_indexed ? 'online' : 'offline'}`}>
            {stats.is_indexed ? '● Online' : '● Indexing'}
          </div>
        </div>
      </div>

      <div className="stats-info">
        <p>
          <strong>Data Source:</strong> data.gov.in
        </p>
        <p>
          <strong>Coverage:</strong> Agriculture & Climate
        </p>
      </div>
    </div>
  );
};

export default Statistics;