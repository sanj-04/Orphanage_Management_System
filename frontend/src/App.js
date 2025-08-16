import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Adopt from './pages/Adopt';
import Donate from './pages/Donate';
import Login from './pages/Login';
import Register from './pages/Register';
import Navbar from './components/Navbar'; // adjust path
import Paid from './pages/Paid';
function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/adopt" element={<Adopt />} />
        <Route path="/donate" element={<Donate />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/paid" element={<Paid />}/>
      </Routes>
    </Router>
  );
}

// const [isLoggedIn, setIsLoggedIn] = useState(false);

export default App;

