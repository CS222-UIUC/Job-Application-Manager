import React, { useState } from "react";
import "./Login.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async () => {
    try {
      const response = await fetch("http://localhost:8000/accounts/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Login successful, save token to localStorage
        localStorage.setItem("token", data.token);
        localStorage.setItem("user", JSON.stringify(data.user));
        setMessage(`Login successful! Welcome ${data.user.username}`);
        // Redirect to tracker page after successful login
        setTimeout(() => {
          window.location.href = "/tracker";
        }, 1000);
      } else {
        setMessage(
          `Login failed: ${data.error || data.message || "Invalid username or password"}`,
        );
      }
    } catch (error) {
      console.error("Network error:", error);
      setMessage("Network error, please check if backend is running");
    }
  };

  const handleRegister = async () => {
    // Simple registration function
    const email = prompt("Please enter email:");
    const password = prompt("Please enter password:");
    const confirmPassword = prompt("Please confirm password:");

    if (!email || !password || !confirmPassword) {
      setMessage("Please fill in all information");
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/accounts/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: email,
          email: email,
          password: password,
          password_confirm: confirmPassword,
          first_name: "",
          last_name: "",
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`Registration successful! User: ${data.user.username}`);
      } else {
        setMessage(`Registration failed: ${JSON.stringify(data)}`);
      }
    } catch (error) {
      console.error("Network error:", error);
      setMessage("Network error, please check if backend is running");
    }
  };

  // const handleForgotPassword = () => {
  //   setMessage("Forgot password feature not implemented yet");
  // };

  return (
    <div className="login-page-wrapper">
      <div className="login-container">
        <h2 className="login-title">User Login</h2>

      {message && (
        <div
          className="message"
          style={{
            padding: "10px",
            margin: "10px 0",
            borderRadius: "4px",
            backgroundColor: message.includes("successful")
              ? "#d4edda"
              : "#f8d7da",
            color: message.includes("successful") ? "#155724" : "#721c24",
            border: `1px solid ${message.includes("successful") ? "#c3e6cb" : "#f5c6cb"}`,
          }}
        >
          {message}
        </div>
      )}

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="login-input"
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="login-input"
      />

      <div className="button-group">
        <button className="login-btn" onClick={handleLogin}>
          Login
        </button>
        <button className="register-btn" onClick={handleRegister}>
          SignUp
        </button>
        {/* <button className="forgot-btn" onClick={handleForgotPassword}>Forget Password?</button> */}
      </div>
      </div>
    </div>
  );
}

export default Login;
