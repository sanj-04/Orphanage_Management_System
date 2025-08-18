import React, { useState, useContext } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './CSS/Login.css';
import { AuthContext } from '../context/AuthContext';   // ✅ import context



function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const { setIsLoggedIn } = useContext(AuthContext);   // ✅ use context

  const handleLogin = async (e) => {
    e.preventDefault();  // ✅ prevent form reload
    // console.log("Login attempt:", username, password);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login/", {
        username: username.trim(),
        password: password.trim(),
      });

      if (response.status === 200) {
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("user_id", response.data.user_id);
        localStorage.setItem("username", response.data.username);
        localStorage.setItem("full_name", response.data.full_name || "");
        localStorage.setItem("email", response.data.email || "");

          // ✅ Update context immediately
        setIsLoggedIn(true);

        setMessage("Login successful");
        navigate("/adopt");
      }
    } catch (error) {
      console.error("Login failed:", error.response?.data || error.message);
      setMessage("Login failed. Please check your credentials.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <label>Username:</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />

          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />

          <button type="submit">Login</button>
        </form>
         {/* ✅ Show success or error messages */}
        {message && (
          <p
            style={{
              color: message.includes('successful') ? 'green' : 'red',
              marginTop: '10px'
            }}
          >
            {message}
          </p>
        )}
       <p>Don't have an account? <a href="/register">Register</a></p>
     </div> 
    </div>
  );
}

export default Login;


