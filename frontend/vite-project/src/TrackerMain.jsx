import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./TrackerMain.css";

function TrackerMain() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [applications, setApplications] = useState([]);
  const [message, setMessage] = useState("");
  const [formData, setFormData] = useState({
    company: "",
    position: "",
    link: "",
    type: "",
    time: "",
    status: "",
  });

  useEffect(() => {
    const token = localStorage.getItem("token");
    const userData = localStorage.getItem("user");

    if (token && userData) {
      setUser(JSON.parse(userData));
      fetchApplications(token);
    }
  }, []);

  const fetchApplications = async (token) => {
    try {
      const response = await fetch("http://localhost:8000/api/applications/", {
        method: "GET",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch applications");
      }

      const data = await response.json();
      setApplications(data);
    } catch (error) {
      console.error("Error fetching applications:", error);
      setMessage("Failed to load applications");
    }
  };

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    try {
      const response = await fetch(
        "http://localhost:8000/api/applications/create/",
        {
          method: "POST",
          headers: {
            Authorization: `Token ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        },
      );

      if (!response.ok) {
        throw new Error("Failed to create application");
      }

      const newApp = await response.json();
      setApplications([...applications, newApp]);
      setFormData({
        company: "",
        position: "",
        link: "",
        type: "",
        time: "",
        status: "",
      });
      setMessage("Application created successfully");
      setTimeout(() => setMessage(""), 3000);
    } catch (error) {
      console.error("Error creating application:", error);
      setMessage("Failed to create application");
    }
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

      {/* Message display */}
      {message && (
        <div
          className={`message ${
            message.includes("Failed") || message.includes("failed")
              ? "error"
              : "success"
          }`}
        >
          {message}
        </div>
      )}

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

        {/* Applications List */}
        <div className="applications-section">
          <h2>Your Applications</h2>
          {applications.length > 0 ? (
            <div className="applications-list">
              {applications.map((app, index) => (
                <div key={index} className="application-card">
                  <div className="app-header">
                    <h3>{app.company}</h3>
                    <span className={`status-badge status-${app.status}`}>
                      {app.status}
                    </span>
                  </div>
                  <p className="position">
                    <strong>Position:</strong> {app.position}
                  </p>
                  {app.link && (
                    <p className="link">
                      <strong>Link:</strong>{" "}
                      <a
                        href={app.link}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {app.link}
                      </a>
                    </p>
                  )}
                  <p className="type">
                    <strong>Type:</strong> {app.type}
                  </p>
                  <p className="date">
                    <strong>Date:</strong> {app.time}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-apps">
              No applications yet. Add one above to get started!
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default TrackerMain;
