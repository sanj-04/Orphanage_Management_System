// import React, { useContext } from 'react';
// import { Link } from 'react-router-dom';
// import { AuthContext } from '../context/AuthContext';
// import './navbar.css';

// const Navbar = () => {
//   const { isLoggedIn, setIsLoggedIn } = useContext(AuthContext);
//   const handleLogout = () => {
//     setIsLoggedIn(false);
//   };

//   return (
//     <nav className="navbar">
//       <div className="navbar-logo">🌟 HopesNest</div>
//       <div className="navbar-links">
//         <Link to="/">Home</Link>
//         {!isLoggedIn && <Link to="/login">Login</Link>}
//         {isLoggedIn && <Link to="/adopt">Adopt</Link>}
//         {isLoggedIn && <button onClick={handleLogout}>Logout</button>}
//       </div>
//     </nav>
//   );
// };

// export default Navbar;

import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './navbar.css';

const Navbar = () => {
  const { isLoggedIn, setIsLoggedIn } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear all stored user data
    localStorage.clear();

    // Update context state
    setIsLoggedIn(false);

    // Redirect to home or login
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">🌟 HopesNest</div>
      <div className="navbar-links">
        <Link to="/">Home</Link>
        {!isLoggedIn && <Link to="/login">Login</Link>}
        {isLoggedIn && <Link to="/adopt">Adopt</Link>}
        {isLoggedIn && (
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;



