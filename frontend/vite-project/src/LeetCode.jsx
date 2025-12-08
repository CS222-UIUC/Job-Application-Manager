import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./LeetCode.css";

function LeetCode() {
  const navigate = useNavigate();
  const [problemNumber, setProblemNumber] = useState("");
  const [records, setRecords] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const fetchRecords = async (token) => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/leetcode/records/", {
        method: "GET",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch records");
      }

      const responseData = await response.json();
      const recordsList = responseData.results || responseData;
      const sortedRecords = Array.isArray(recordsList)
        ? recordsList.sort(
            (a, b) => a.problem.problem_id - b.problem.problem_id,
          )
        : [];
      setRecords(sortedRecords);
    } catch (error) {
      console.error("Error fetching records:", error);
      setError("Failed to load records");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetchRecords(token);
    } else {
      navigate("/login");
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    const number = parseInt(problemNumber.trim());
    if (isNaN(number) || number <= 0) {
      setError("Please enter a valid positive integer for the problem number.");
      setSubmitting(false);
      return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
      setError("Please login first.");
      setSubmitting(false);
      navigate("/login");
      return;
    }

    if (records.some((record) => record.problem.problem_id === number)) {
      setError(`Problem #${number} already exists in your records.`);
      setSubmitting(false);
      return;
    }

    try {
      const recordResponse = await fetch(
        "http://localhost:8000/leetcode/records/",
        {
          method: "POST",
          headers: {
            Authorization: `Token ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            problem_id: number,
          }),
        },
      );

      if (!recordResponse.ok) {
        let errorData;
        try {
          errorData = await recordResponse.json();
        } catch (e) {
          errorData = {};
        }

        if (recordResponse.status === 400) {
          let errorMsg = errorData.detail;

          if (!errorMsg && errorData.problem_id) {
            if (Array.isArray(errorData.problem_id)) {
              errorMsg = errorData.problem_id[0];
            } else {
              errorMsg = errorData.problem_id;
            }
          }
          
          if (!errorMsg && errorData.non_field_errors) {
            if (Array.isArray(errorData.non_field_errors)) {
              errorMsg = errorData.non_field_errors[0];
            } else {
              errorMsg = errorData.non_field_errors;
            }
          }

          if (!errorMsg) {
            errorMsg = `Problem #${number} may already exist in your records, or does not exist in the database.`;
          }

          setError(errorMsg);
        } else if (recordResponse.status === 404) {
          setError(`Problem #${number} does not exist in the database. Please ensure the problem is loaded.`);
        } else {
          setError(`Failed to create record (status: ${recordResponse.status}). Please try again later.`);
        }
        setSubmitting(false);
        return;
      }

      await fetchRecords(token);
      setProblemNumber("");
      setError("");
    } catch (error) {
      console.error("Error creating record:", error);
      setError("Failed to create record. Please try again later.");
    } finally {
      setSubmitting(false);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case "Easy":
        return "#28a745";
      case "Medium":
        return "#ffc107";
      case "Hard":
        return "#dc3545";
      default:
        return "#6c757d";
    }
  };

  return (
    <div className="leetcode-container">
      <div className="leetcode-header">
        <button onClick={() => navigate("/tracker")} className="back-btn">
          ← Back
        </button>
        <h1>LeetCode Tracker</h1>
      </div>

      <div className="leetcode-content">
        {/* Input Section */}
        <div className="input-section">
          <form onSubmit={handleSubmit} className="problem-input-form">
            <div className="input-group">
              <label htmlFor="problem-number">Problem Number</label>
              <input
                id="problem-number"
                type="text"
                value={problemNumber}
                onChange={(e) => {
                  setProblemNumber(e.target.value);
                  setError("");
                }}
                placeholder="Please enter the problem number"
                className="problem-input"
                disabled={submitting}
              />
              {error && <div className="error-message">{error}</div>}
            </div>
            <button
              type="submit"
              className="submit-btn"
              disabled={submitting}
            >
              {submitting ? "Submitting..." : "Confirm"}
            </button>
          </form>
        </div>

        {/* Records Section */}
        <div className="records-section">
          <h2>Completed Problems</h2>
          {loading ? (
            <div className="empty-state">
              <p>Loading...</p>
            </div>
          ) : records.length === 0 ? (
            <div className="empty-state">
              <p>No records</p>
              <p className="hint">Please enter a problem number to add a record.</p>
            </div>
          ) : (
            <div className="records-list">
              {records.map((record) => {
                const problem = record.problem;
                const solvedAt = record.solved_at
                  ? new Date(record.solved_at).toLocaleString("en-US", {
                      year: "numeric",
                      month: "2-digit",
                      day: "2-digit",
                      hour: "2-digit",
                      minute: "2-digit",
                      second: "2-digit",
                    })
                  : "Not recorded";

                return (
                  <div
                    key={`record-${problem.problem_id}`}
                    className="record-card"
                  >
                    <div className="record-header">
                      <div className="record-number">#{problem.problem_id}</div>
                      <div
                        className="difficulty-badge"
                        style={{
                          backgroundColor: getDifficultyColor(problem.difficulty),
                        }}
                      >
                        {problem.difficulty}
                      </div>
                    </div>
                    <div className="record-name">
                      {problem.url ? (
                        <a
                          href={problem.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{
                            color: "#007bff",
                            textDecoration: "none",
                          }}
                        >
                          {problem.title}
                        </a>
                      ) : (
                        problem.title
                      )}
                    </div>
                    {problem.tags && problem.tags.length > 0 && (
                      <div className="record-topics">
                        <span className="topics-label">Tags:</span>
                        <div className="topics-list">
                          {problem.tags.map((tag, index) => (
                            <span key={index} className="topic-tag">
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    <div className="record-time">Solved at: {solvedAt}</div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default LeetCode;
