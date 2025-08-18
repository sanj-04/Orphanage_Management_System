import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './CSS/Donate.css';
import qr from "./images/qr.png";

const Donate = () => {
  const location = useLocation();
  const showSubmit = new URLSearchParams(location.search).get('payment') === 'done';
  const navigate = useNavigate();

  // State for form
  const [fullName, setFullName] = useState('');
  const [amount, setAmount] = useState('');
  const [transactionId, setTransactionId] = useState('');
  const [message, setMessage] = useState('');

  const handleClick = () => {
    navigate('/paid');
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/donate/", {
        full_name: fullName,
        amount: amount,
        payment_id: transactionId,
        email: localStorage.getItem("email") || ""
      });

      if (response.status === 201) {
        setMessage("✅ Donation submitted successfully. Thank you!");
        setFullName('');
        setAmount('');
        setTransactionId('');
      }
    } catch (error) {
      console.error("Donation error:", error.response?.data || error.message);
      setMessage("❌ Failed to submit donation. Try again.");
    }
  };

  // Form validation → all fields must be filled
  const isFormValid = fullName.trim() !== '' && amount.trim() !== '' && transactionId.trim() !== '';

  return (
    <div className="donate-container">
      <div className="donate-card">
        <h1>Make a Donation</h1>
        <p>Your generous donation helps provide food, shelter, and education to children in need.</p>

        <img
          src={qr}
          alt="QR Code to Paid Page"
          style={{ width: "200px", height: "200px" }}
          onClick={handleClick}
        />

        <p>Scan this QR code to proceed to payment</p>
        <p><strong>UPI ID:</strong> dummyupi@bank</p>

        {showSubmit ? (
          <>
            <p className="success-msg">✅ Payment Successful!</p>

            {/* Required textboxes */}
            <input
              type="text"
              placeholder="Enter your name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Enter amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Transaction ID"
              value={transactionId}
              onChange={(e) => setTransactionId(e.target.value)}
              required
            />

            {/* Submit enabled only if all fields filled */}
            <button
              className="submit-btn"
              onClick={handleSubmit}
              disabled={!isFormValid}
            >
              Submit
            </button>

            {message && <p>{message}</p>}
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
