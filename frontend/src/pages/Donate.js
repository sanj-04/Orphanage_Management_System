// src/pages/Donate.jsx
import React from 'react';
import { useLocation } from 'react-router-dom';
import './CSS/Donate.css';
import qr from "./images/qr.png";
import { useNavigate } from 'react-router-dom';

const Donate = () => {
  const location = useLocation();
  const showSubmit = new URLSearchParams(location.search).get('payment') === 'done';
  const navigate = useNavigate();

    const handleClick = () => {
      navigate('/paid');
    };

  return (
    <div className="donate-container">
      <div className="donate-card">
        <h1>Make a Donation</h1>
        <p>Your generous donation helps provide food, shelter, and education to children in need.</p>

        <img
        src={qr}
        alt="QR Code to Paid Page"
        style={{ width: "200px", height: "200px" }} onClick={handleClick}

      />
      
        <p>Scan this QR code to proceed to payment</p>
        <p><strong>UPI ID:</strong> dummyupi@bank</p>

        {showSubmit ? (
          <>
            <p className="success-msg">✅ Payment Successful!</p>
            <button className="submit-btn" onClick={() => alert('Payment submitted! Thank you!')}>
              Submit
            </button>
          </>
        ) : (
          <p className="paid-link">
            <a href="/paid">Click here if you have paid</a>
          </p>
        )}
      </div>
    </div>
  );
};

export default Donate;