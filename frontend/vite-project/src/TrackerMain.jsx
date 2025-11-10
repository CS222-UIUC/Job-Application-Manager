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
  const [jdData, setJdData] = useState(null);
  const [jdLoading, setJdLoading] = useState(false);
  const [jdError, setJdError] = useState("");

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
      const response = await fetch("http://localhost:8000/applications/", {
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
        "http://localhost:8000/applications/create/",
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

  const handleFetchJobDescription = async () => {
    if (!formData.link) {
      setJdError("Please enter a job posting URL first");
      return;
    }

    const token = localStorage.getItem("token");
    setJdLoading(true);
    setJdError("");
    setJdData(null);

    try {
      const jdResponse = await fetch("http://localhost:8000/extraction/extract_jd/", {
        method: "POST",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: formData.link }),
      });

      if (!jdResponse.ok) {
        throw new Error("Failed to fetch job description");
      }

      const jdResult = await jdResponse.json();

      const skillsResponse = await fetch("http://localhost:8000/extraction/extract_skills/", {
        method: "POST",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: formData.link }),
      });

      if (!skillsResponse.ok) {
        throw new Error("Failed to fetch skills");
      }

      const skillsResult = await skillsResponse.json();

      setJdData({
        url: skillsResult.url,
        jobTitle: skillsResult.job_title,
        company: skillsResult.company,
        location: skillsResult.location,
        responsibilities: skillsResult.responsibilities || [],
        requirements: skillsResult.requirements || [],
        categories: skillsResult.categories || [],
        flat: skillsResult.flat || [],
      });
    } catch (error) {
      console.error("Error fetching job description:", error);
      setJdError("Failed to fetch job description. Please check the URL and try again.");
    } finally {
      setJdLoading(false);
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
            <button
              onClick={() => navigate("/chat-ai")}
              className="chat-ai-btn"
            >
              Chat with AI
            </button>
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
                  <option value="offer">Offerred</option>
                  <option value="rejected">Rejected</option>
                </select>
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="submit-btn">
                Add Application
              </button>
              <button
                type="button"
                onClick={handleFetchJobDescription}
                className="fetch-jd-btn"
                disabled={jdLoading}
              >
                {jdLoading ? "Fetching..." : "Fetch Job Description"}
              </button>
            </div>
          </form>

          <div className="jd-section">
            {!jdData && !jdLoading && !jdError && (
              <p className="jd-placeholder">No job description fetched yet.</p>
            )}

            {jdLoading && (
              <div className="jd-loading">
                <div className="loading-spinner"></div>
                <p>Fetching job description...</p>
              </div>
            )}

            {jdError && (
              <div className="jd-error">
                <p>{jdError}</p>
              </div>
            )}

            {jdData && !jdLoading && (
              <div className="jd-card">
                <div className="jd-header">
                  <div className="jd-title-block">
                    <h3 className="jd-position">{jdData.jobTitle}</h3>
                    <div className="jd-meta">
                      <span className="jd-company">{jdData.company}</span>
                      {jdData.location && jdData.location !== "Not specified" && (
                        <>
                          <span className="jd-separator">•</span>
                          <span className="jd-location">{jdData.location}</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>

                <div className="jd-content">
                  <div className="jd-category-block">
                    <h3 className="jd-category-title">Requirements</h3>

                    {jdData.responsibilities && jdData.responsibilities.length > 0 && (
                      <div className="jd-summary-section">
                        <h4 className="jd-summary-label">Responsibilities</h4>
                        <ul className="jd-bullet-list">
                          {jdData.responsibilities.map((item, index) => (
                            <li key={index}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {jdData.requirements && jdData.requirements.length > 0 && (
                      <div className="jd-summary-section">
                        <h4 className="jd-summary-label">Qualifications</h4>
                        <ul className="jd-bullet-list">
                          {jdData.requirements.map((item, index) => (
                            <li key={index}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {jdData.categories && jdData.categories.length > 0 && (
                      <div className="jd-summary-section">
                        <h4 className="jd-summary-label">Technical Skills</h4>
                        <div className="jd-skills-by-category">
                          {jdData.categories.map((category, idx) => (
                            category.skills && category.skills.length > 0 && (
                              <div key={idx} className="skill-category-item">
                                <span className="skill-category-name">{category.name}:</span>
                                <div className="skill-category-tags">
                                  {category.skills.map((skill, index) => (
                                    <span key={index} className="skill-badge">
                                      {skill}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="jd-footer">
                    <a href={jdData.url} target="_blank" rel="noopener noreferrer" className="jd-view-link">
                      View Full Job Posting →
                    </a>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Applications List */}
        <div className="applications-section">
          <h2>Your Applications</h2>
          {applications.length > 0 ? (
            <div className="applications-list">
              {applications.map((app, index) => (
                <div key={index} className="application-card">
                  <div className="app-header">
                    <h3>{app.company_name}</h3>
                    <span className={`status-badge status-${app.status}`}>
                      {app.status}
                    </span>
                  </div>
                  <p className="position">
                    <strong>Position:</strong> {app.position}
                  </p>
                  {app.company_website && (
                    <p className="link">
                      <strong>Link:</strong>{" "}
                      <a
                        href={app.company_website}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {app.company_website}
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
