// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';
import Statistics from './components/Statistics';
import { api } from './services/api';

function App() {
  const [stats, setStats] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [exampleQueries] = useState([
    "Compare the average annual rainfall in Punjab and Haryana for the last 5 years",
    "What are the top 5 crops by production volume in Maharashtra?",
    "Show me the production trend of wheat in Uttar Pradesh over the last decade",
    "Identify the district with highest rice production in West Bengal",
    "Analyze the correlation between rainfall and crop production in Karnataka"
  ]);

  useEffect(() => {
    // Check connection and load stats
    checkConnection();
    loadStats();
  }, []);

  const checkConnection = async () => {
    try {
      await api.healthCheck();
      setIsConnected(true);
    } catch (error) {
      console.error('Connection failed:', error);
      setIsConnected(false);
    }
  };

  const loadStats = async () => {
    try {
      const data = await api.getStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const handleExampleClick = (query) => {
    // This will be handled by ChatInterface component
    const event = new CustomEvent('exampleQuery', { detail: query });
    window.dispatchEvent(event);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">🌾 Project Samarth</h1>
        <p className="app-subtitle">
          Intelligent Q&A System for India's Agricultural Economy & Climate Data
        </p>
        <div style={{ 
          marginTop: '10px', 
          fontSize: '0.9rem',
          color: isConnected ? '#10b981' : '#ef4444'
        }}>
          {isConnected ? '● Connected to data.gov.in' : '● Connecting...'}
        </div>
      </header>

      <div className="main-content">
        <div className="chat-section">
          <ChatInterface onStatsUpdate={loadStats} />
        </div>

        <div className="sidebar">
          {stats && <Statistics stats={stats} />}
          
          <div className="example-queries">
            <h3>📝 Example Queries</h3>
            {exampleQueries.map((query, index) => (
              <div
                key={index}
                className="example-query"
                onClick={() => handleExampleClick(query)}
              >
                {query}
              </div>
            ))}
          </div>
        </div>
      </div>

      <footer className="footer">
        <p>Powered by data.gov.in | Built for Agricultural Policy & Research</p>
        <p style={{ fontSize: '0.8rem', marginTop: '5px' }}>
          Data sourced from Ministry of Agriculture & India Meteorological Department
        </p>
      </footer>
    </div>
  );
}

export default App;