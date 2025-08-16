// src/pages/Paid.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

const Paid = () => {
  const navigate = useNavigate();

  const handlePaid = () => {
    navigate('/donate?payment=done');
  };

  return (
    <div style={{ textAlign: 'center', padding: '50px', display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '15px' }}>
      <h2>Payment Confirmation</h2>
      <button
        onClick={handlePaid}
        style={{
          padding: '10px 14px', // reduced size
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          fontSize: '16px', // smaller text
          cursor: 'pointer',
          height:'40px',
          width:'100px',
          position: 'relative',
          left: '-110px' // move slightly left
        }}
      >
        Paid
      </button>
    </div>
  );
};

export default Paid;
