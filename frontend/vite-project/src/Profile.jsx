import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import "./Profile.css";

function Profile() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
  });
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeInfo, setResumeInfo] = useState(null);

  const loadResumeInfo = useCallback(async () => {
    const token = localStorage.getItem("token");
    try {
      const response = await fetch(
        "http://localhost:8000/accounts/get-resume/",
        {
          method: "GET",
          headers: {
            Authorization: `Token ${token}`,
            "Content-Type": "application/json",
          },
        },
      );
      if (response.ok) {
        const data = await response.json();
        setResumeInfo(data);
      }
    } catch (error) {
      console.error("Error loading resume info:", error);
    }
  }, []);

  const loadProfile = useCallback(async () => {
    const token = localStorage.getItem("token");
    try {
      setLoading(true);
      const response = await fetch("http://localhost:8000/accounts/profile/", {
        method: "GET",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) throw new Error("Failed to fetch profile");

      const data = await response.json();
      setUser(data);
      setFormData({
        first_name: data.first_name || "",
        last_name: data.last_name || "",
        email: data.email || "",
      });
      loadResumeInfo();
    } catch (error) {
      setMessage("Failed to load profile");
      console.error("Error loading profile:", error);
    } finally {
      setLoading(false);
    }
  }, [loadResumeInfo]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }
    loadProfile();
  }, [navigate, loadProfile]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleResumeChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setResumeFile(file);
    }
  };

  const handleUploadResume = async () => {
    if (!resumeFile) {
      setMessage("Please select a file first");
      return;
    }

    const token = localStorage.getItem("token");
    const formDataForUpload = new FormData();
    formDataForUpload.append("resume", resumeFile);

    try {
      const response = await fetch(
        "http://localhost:8000/accounts/upload-resume/",
        {
          method: "POST",
          headers: {
            Authorization: `Token ${token}`,
          },
          body: formDataForUpload,
        },
      );

      if (!response.ok) throw new Error("Failed to upload resume");

      setMessage("Resume uploaded successfully");
      setResumeFile(null);
      await loadResumeInfo();
      setTimeout(() => setMessage(""), 3000);
    } catch (error) {
      setMessage("Failed to upload resume");
      console.error("Error uploading resume:", error);
    }
  };

  const handleViewResume = () => {
    if (resumeInfo?.resume_url) {
      window.open(resumeInfo.resume_url, "_blank");
    }
  };

  const handleSave = async () => {
    const token = localStorage.getItem("token");
    try {
      const response = await fetch("http://localhost:8000/accounts/profile/", {
        method: "PUT",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error("Failed to update profile");

      const data = await response.json();
      setUser(data.user || data);
      setIsEditing(false);
      setMessage("Profile updated successfully");
      setTimeout(() => setMessage(""), 3000);
    } catch (error) {
      setMessage("Failed to update profile");
      console.error("Error updating profile:", error);
    }
  };

  const handleLogout = async () => {
    const token = localStorage.getItem("token");
    try {
      await fetch("http://localhost:8000/accounts/logout/", {
        method: "POST",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
      });
    } catch (error) {
      console.error("Logout error:", error);
    }
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  };

  if (loading) {
    return (
      <div className="profile-container">
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="header-left">
          <button
            className="return-btn"
            onClick={() => navigate(-1)}
            aria-label="Go back to previous page"
          >
            ← Return
          </button>
          <h1>User Profile</h1>
        </div>
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </div>

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

      <div className="profile-content">
        {!isEditing ? (
          <div className="profile-view">
            <div className="info-row">
              <span className="label">Username:</span>
              <span className="value">{user?.username}</span>
            </div>
            <div className="info-row">
              <span className="label">First Name:</span>
              <span className="value">{user?.first_name || "-"}</span>
            </div>
            <div className="info-row">
              <span className="label">Last Name:</span>
              <span className="value">{user?.last_name || "-"}</span>
            </div>
            <div className="info-row">
              <span className="label">Email:</span>
              <span className="value">{user?.email || "-"}</span>
            </div>

            <div className="resume-section">
              <h3>Resume Upload</h3>
              {resumeInfo?.has_resume && (
                <div className="resume-info">
                  <p className="resume-status">✓ Resume uploaded</p>
                  {resumeInfo.uploaded_at && (
                    <p className="resume-date">
                      Uploaded:{" "}
                      {new Date(resumeInfo.uploaded_at).toLocaleDateString()}
                    </p>
                  )}
                  <button
                    className="view-resume-btn"
                    onClick={handleViewResume}
                  >
                    View Resume
                  </button>
                </div>
              )}
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={handleResumeChange}
                className="resume-input"
              />
              <button className="upload-btn" onClick={handleUploadResume}>
                {resumeInfo?.has_resume ? "Update Resume" : "Upload Resume"}
              </button>
            </div>

            <button className="edit-btn" onClick={() => setIsEditing(true)}>
              Edit Profile
            </button>
          </div>
        ) : (
          <div className="profile-edit">
            <div className="form-group">
              <label>First Name</label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleInputChange}
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label>Last Name</label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleInputChange}
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="form-input"
              />
            </div>
            <div className="button-group">
              <button className="save-btn" onClick={handleSave}>
                Save
              </button>
              <button
                className="cancel-btn"
                onClick={() => setIsEditing(false)}
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Profile;
