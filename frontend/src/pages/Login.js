import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './CSS/Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();  // ✅ prevent form reload
    // console.log("Login attempt:", username, password);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login/", {
        username,
        password,
      });

      if (response.status === 200) {
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("user_id", response.data.user_id);
        localStorage.setItem("username", response.data.username);
        localStorage.setItem("full_name", response.data.full_name || "");
        localStorage.setItem("email", response.data.email || "");

        setMessage("Login successful");
        navigate("/adopt");
      }
    } catch (error) {
      console.error("Login failed:", error.response?.data || error.message);
      setMessage("Login failed. Please check your credentials.");
    }
  };

  // const handleLogin = async (e) => {
    // e.preventDefault();

    // try {
    //   const response = await axios.post('http://127.0.0.1:8000/api/login/', {
    //     username,
    //     password
    //   });

    //   if (response.status === 200) {
    //     // ✅ Save token in localStorage
    //     localStorage.setItem('token', response.data.token);
    //     localStorage.setItem("user_id", response.data.user_id);
    //     localStorage.setItem('full_name', response.data.full_name || "");
    //     localStorage.setItem('email', response.data.email || "");
    //     localStorage.setItem('username', response.data.username); // keep true username
    //     setMessage('Login successful');
    //     console.log('Login successful:', response.data);

    //     // ✅ Redirect to Adopt page (or any page you want)
    //     navigate('/adopt');
    //   }
    // } catch (error) {
    //   console.error('Login failed:', error.response?.data || error.message);
    //   setMessage('Login failed. Please check your credentials.');
    // }


  //   axios.post("http://127.0.0.1:8000/api/login/", { username, password })
  // .then((response) => {
  //   if (response.status === 200) {
  //     localStorage.setItem("token", response.data.token);
  //     localStorage.setItem("user_id", response.data.user_id);
  //     localStorage.setItem("username", response.data.username);   // keep technical login (could be user_29)
  //     localStorage.setItem("full_name", response.data.full_name); // ✅ display name
  //     localStorage.setItem("email", response.data.email);         // ✅ real email

  //     setMessage("Login successful");
  //     navigate("/adopt");
  //   }
  // })
  // .catch(() => setMessage("Invalid credentials"));
  // };

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



// // src/pages/Login.jsx
// import React from 'react';


// const Login = () => {
//   return (
//     <div className="login-container">
//       <div className="login-card">
//         <h2>Login</h2>
//         <form>
//           <input type="text" placeholder="Username" required />
//           <input type="password" placeholder="Password" required />
//           <button type="submit">Login</button>
//         </form>
//         <p>Don't have an account? <a href="/register">Register</a></p>
//       </div>
//     </div>
//   );
// };

// export default Login;