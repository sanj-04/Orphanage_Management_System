import React from 'react';
import './CSS/Home.css';
import bg from './images/Home.jpeg';
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div
      className="home-container"  style={{ backgroundImage: `url(${bg})` ,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      minHeight: '100vh',
      color: 'black',}} >

      <section className="hero">
        <h1>
          Welcome to <span className="brand">HopeHub</span>
        </h1>
        <p>Your support brings hope to every child.</p>
        <div className="hero-buttons">
          <Link to="/register">
            <button className="btn register-btn">Register</button>
          </Link>
          <Link to="/donate">
            <button className="btn donate-btn">Donate</button>
          </Link>
        </div>
     </section>
  </div>
  );
};

export default Home;




