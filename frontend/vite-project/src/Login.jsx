import React, { useState } from "react";
import "./login.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    alert(`Logging...\nEmail: ${username}\nPassword: ${password}`);
  };

  const handleRegister = () => {
    alert("Goes to registration page");
  };

  const handleForgotPassword = () => {
    alert("Goes to password recovery page");
  };

  return (
    <div className="login-container">
      <h2 className="login-title">User Login</h2>

      <input
        type="text"
        placeholder="Email"
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
        <button className="login-btn" onClick={handleLogin}>Login</button>
        <button className="register-btn" onClick={handleRegister}>SignUp</button>
        <button className="forgot-btn" onClick={handleForgotPassword}>Forget Password?</button>
      </div>
    </div>
  );
}

export default Login;
