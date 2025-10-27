import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./TrackerMain.css";

function TrackerMain() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [formData, setFormData] = useState({
    company: "",
    position: "",
    link: "",
    type: "",
    time: "",
    status: "",
  });

  useEffect(() => {
    // Check if there is a logged in user
    const token = localStorage.getItem("token");
    const userData = localStorage.getItem("user");

    if (token && userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogout = async () => {
    const token = localStorage.getItem("token");

    if (token) {
      try {
        await fetch("http://localhost:8000/accounts/logout/", {
          method: "POST",
          headers: {
            Authorization: `Token ${token}`,
            "Content-Type": "application/json",
          },
        });
      } catch (error) {
        console.error("Login failed:", error);
        console.log("Logout request failed, but continue to clear local data");
      }
    }

    // Clear local storage
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
    // TODO: call backend api to store those data
  };

  return (
    <div className="tracker-container">
      {/* Header with title and user info */}
      <div className="header-section">
        <div className="title-group">
          <h1>Job Application Tracker</h1>
          <p className="subtitle">
            Track your job applications and their progress
          </p>
        </div>

        {user ? (
          <div className="user-profile-section">
            <div
              className="profile-widget"
              onClick={() => navigate("/profile")}
            >
              <div className="profile-avatar">
                {user.username.charAt(0).toUpperCase()}
              </div>
              <span className="profile-username">{user.username}</span>
            </div>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        ) : (
          <Link to="/login" className="get-started-btn">
            Get Started
          </Link>
        )}
      </div>

      {/* Main content - Application Form */}
      <div className="main-content">
        <div className="form-section">
          <h2>Add New Application</h2>

          <form onSubmit={handleSubmit} className="application-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="company">Company</label>
                <input
                  type="text"
                  id="company"
                  name="company"
                  value={formData.company}
                  onChange={handleInputChange}
                  placeholder="Enter company name"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="position">Position</label>
                <input
                  type="text"
                  id="position"
                  name="position"
                  value={formData.position}
                  onChange={handleInputChange}
                  placeholder="Enter position title"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="link">Link</label>
                <input
                  type="url"
                  id="link"
                  name="link"
                  value={formData.link}
                  onChange={handleInputChange}
                  placeholder="Enter application link"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="type">Type</label>
                <select
                  id="type"
                  name="type"
                  value={formData.type}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select type</option>
                  <option value="fulltime">Full Time</option>
                  <option value="intern">Intern</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="time">Time</label>
                <input
                  type="date"
                  id="time"
                  name="time"
                  value={formData.time}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="status">Status</label>
                <select
                  id="status"
                  name="status"
                  value={formData.status}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select status</option>
                  <option value="applied">Applied</option>
                  <option value="oa">OA</option>
                  <option value="interview">Interview</option>
                  <option value="offer">Offer</option>
                  <option value="rejected">Rejected</option>
                </select>
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="submit-btn">
                Add Application
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default TrackerMain;
