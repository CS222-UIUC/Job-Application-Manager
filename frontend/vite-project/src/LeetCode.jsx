import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LeetCode.css";

function LeetCode() {
  const navigate = useNavigate();
  const [problemNumber, setProblemNumber] = useState("");
  const [records, setRecords] = useState([
    // Example placeholder record
    {
      id: 1,
      number: 1,
      name: "Two Sum",
      difficulty: "Easy",
      topics: ["Array", "Hash Table"],
      completedAt: "2024-01-15 10:30:00",
    },
  ]);
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    const number = parseInt(problemNumber.trim());
    if (isNaN(number) || number <= 0) {
      setError("Please enter a valid positive integer for the problem number.");
      return;
    }

    if (records.some((record) => record.number === number)) {
      setError(`Problem #${number} already exists in your records.`);
      return;
    }

    const exampleNames = [
      "Two Sum",
      "Add Two Numbers",
      "Longest Substring Without Repeating Characters",
      "Median of Two Sorted Arrays",
      "Longest Palindromic Substring",
      "ZigZag Conversion",
      "Reverse Integer",
      "String to Integer (atoi)",
      "Palindrome Number",
      "Regular Expression Matching",
    ];

    const difficulties = ["Easy", "Medium", "Hard"];
    const allTopics = [
      "Array",
      "Hash Table",
      "Two Pointers",
      "String",
      "Dynamic Programming",
      "Math",
      "Tree",
      "Graph",
      "Backtracking",
      "Greedy",
      "Binary Search",
      "Stack",
      "Queue",
      "Linked List",
    ];

    const randomName =
      exampleNames[Math.floor(Math.random() * exampleNames.length)];
    const randomDifficulty =
      difficulties[Math.floor(Math.random() * difficulties.length)];
    const topicCount = Math.floor(Math.random() * 3) + 1; // 1-3 topics
    const shuffledTopics = [...allTopics].sort(() => 0.5 - Math.random());
    const randomTopics = shuffledTopics.slice(0, topicCount);

    const now = new Date();
    const completedAt = `${now.getFullYear()}-${String(
      now.getMonth() + 1,
    ).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")} ${String(
      now.getHours(),
    ).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}:${String(
      now.getSeconds(),
    ).padStart(2, "0")}`;

    const newRecord = {
      id: Date.now(),
      number: number,
      name: randomName,
      difficulty: randomDifficulty,
      topics: randomTopics,
      completedAt: completedAt,
    };

    setRecords([...records, newRecord].sort((a, b) => a.number - b.number));
    setProblemNumber("");
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
              <label htmlFor="problem-number">Problem number</label>
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
              />
              {error && <div className="error-message">{error}</div>}
            </div>
            <button type="submit" className="submit-btn">
              confirm
            </button>
          </form>
        </div>

        {/* Records Section */}
        <div className="records-section">
          <h2>Completed Problems</h2>
          {records.length === 0 ? (
            <div className="empty-state">
              <p>Null</p>
              <p className="hint">Please enter the problem number.</p>
            </div>
          ) : (
            <div className="records-list">
              {records.map((record) => (
                <div key={record.id} className="record-card">
                  <div className="record-header">
                    <div className="record-number">#{record.number}</div>
                    <div
                      className="difficulty-badge"
                      style={{
                        backgroundColor: getDifficultyColor(record.difficulty),
                      }}
                    >
                      {record.difficulty}
                    </div>
                  </div>
                  <div className="record-name">{record.name}</div>
                  <div className="record-topics">
                    <span className="topics-label">Topics:</span>
                    <div className="topics-list">
                      {record.topics.map((topic, index) => (
                        <span key={index} className="topic-tag">
                          {topic}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="record-time">Date: {record.completedAt}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default LeetCode;
