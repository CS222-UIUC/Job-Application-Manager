import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check if there is a logged in user
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogout = async () => {
    const token = localStorage.getItem('token');
    
    if (token) {
      try {
        await fetch('http://localhost:8000/accounts/logout/', {
          method: 'POST',
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
          },
        });
      } catch (error) {
        console.log('Logout request failed, but continue to clear local data');
      }
    }
    
    // Clear local storage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <div className="home-container">
      {/* Header with title and Get Started button */}
      <div className="header-section">
        <div className="title-group">
          <h1>Job Application Tracker</h1>
          <p className="subtitle">Keep track of all your job applications in one place</p>
        </div>
        
        {user ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <span>Welcome, {user.username}!</span>
            <button 
              onClick={handleLogout}
              style={{
                padding: '10px 20px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Logout
            </button>
          </div>
        ) : (
          <Link to="/login" className="get-started-btn">
            Get Started
          </Link>
        )}
      </div>

      {/* Main content */}
      <div className="main-content">
        <div className="features-section">
          <h2>What We Offer</h2>

          <div className="feature-cards">
            <div className="feature-card">
              <h3>Track Applications</h3>
              <p>Manage all your job applications and their status in one dashboard</p>
            </div>

            <div className="feature-card">
              <h3>AI Recommendations</h3>
              <p>Get personalized skill suggestions based on your applied positions</p>
            </div>

            <div className="feature-card">
              <h3>Practice Problems</h3>
              <p>Access recommended LeetCode problems to prepare for interviews</p>
            </div>

            <div className="feature-card">
              <h3>Resume Management</h3>
              <p>Upload and manage different versions of your resume</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;