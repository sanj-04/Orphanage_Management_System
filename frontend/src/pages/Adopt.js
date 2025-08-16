import { useNavigate } from "react-router-dom";
import "./CSS/Adopt.css";
import React, { useState, useEffect } from "react";
import axios from "axios";


// const childrenData = [
//   {
//     id: 1,
//     name: "Aadhya",
//     age: 6,
//     gender: "Female",
//     location: "Bangalore",
//     image: "images/Aadhya.jpeg",
//     health: "Healthy, regular check-ups.",
//     background: "Orphaned at age 4, currently in foster care."
//   },
//   {
//     id: 2,
//     name: "Diya",
//     age: 5,
//     gender: "Female",
//     location: "Chennai",
//     image: "images/Diya.jpg",
//     health: "Mild seasonal allergies.",
//     background: "From a rural area, enjoys drawing and dancing."
//   },
//   {
//     id: 3,
//     name: "Rahul",
//     age: 7,
//     gender: "Male",
//     location: "Hyderabad",
//     image: "images/Arav.jpg",
//     health: "Excellent health.",
//     background: "Lost parents in an accident, very active and cheerful."
//   },
//   {
//     id: 4,
//     name: "Aadhya",
//     age: 6,
//     gender: "Female",
//     location: "Bangalore",
//     image: "images/Aadhya.jpeg",
//     health: "Healthy, regular check-ups.",
//     background: "Orphaned at age 4, currently in foster care."
//   },
//   {
//     id: 5,
//     name: "Diya",
//     age: 5,
//     gender: "Female",
//     location: "Chennai",
//     image: "images/Diya.jpg",
//     health: "Mild seasonal allergies.",
//     background: "From a rural area, enjoys drawing and dancing."
//   },
//   {
//     id: 6,
//     name: "Rahul",
//     age: 7,
//     gender: "Male",
//     location: "Hyderabad",
//     image: "images/Arav.jpg",
//     health: "Excellent health.",
//     background: "Lost parents in an accident, very active and cheerful."
//   }
// ];

const Adopt = () => {
  const navigate = useNavigate();
  const [childrenData, setChildrenData] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [popupType, setPopupType] = useState(null); // "adopt", "confirm", "more"

  const handleBack = () => navigate("/");

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/children/") // Django API endpoint
      .then((res) => setChildrenData(res.data))
      .catch((err) => console.error(err));
  }, []);

  const openAdoptPopup = (child) => {
    setSelectedChild(child);
    setPopupType("adopt");
  };

  const confirmAdoption = () => {
    setPopupType("confirm");
  };

  const openMorePopup = (child) => {
    setSelectedChild(child);
    setPopupType("more");
  };

  const closePopup = () => {
    setSelectedChild(null);
    setPopupType(null);
  };

  return (
    <div className="adopt-container">
      {/* /*<button className="back-btn" onClick={handleBack}>
        ← Back
      </button>// */}

      <h1>Meet Our Children</h1>
      <p>These children are looking for loving families.</p>

      <div className="child-grid">
        {childrenData.map((child) => (
          <div className="child-card" key={child.id}>
            <img src={`http://127.0.0.1:8000${child.image}`} alt={child.name} />
            <h3>{child.name}</h3>
            <p>Age: {child.age}</p>
            <p>Gender: {child.gender}</p>
            <p>Location: {child.location}</p>
            <div className="card-buttons">
            <button className="adopt-btn" onClick={() => openAdoptPopup(child)}>
              Adopt
            </button>
            <button className="more-btn" onClick={() => openMorePopup(child)}>
              More
            </button></div>

          </div>
        ))}
      </div>

      {/* Popup Overlay */}
      {popupType && (
        <div className="popup-overlay" onClick={closePopup}>
          <div className="popup-box" onClick={(e) => e.stopPropagation()}>
            {popupType === "adopt" && (
              <>
                <h2>Confirm Adoption</h2>
                <p>
                  Are you sure you're interested in adopting
                  <strong>{selectedChild.name}</strong>?
                </p>
                <div className="popup-buttons">
                  <button className="yes-btn" onClick={confirmAdoption}>
                    Yes
                  </button>
                  <button className="no-btn" onClick={closePopup}>
                    No
                  </button>
                </div>
              </>
            )}

            {popupType === "confirm" && (
              <>
                <h2>Adoption Request Sent</h2>
                <p>You will be contacted by organisation.</p>
                <button className="ok-btn" onClick={closePopup}>
                  OK
                </button>
              </>
            )}

            {popupType === "more" && (
              <>
                <h2>{selectedChild.name}</h2>
                <img
                  src={`http://127.0.0.1:8000${selectedChild.image}`} alt={selectedChild.name} className="popup-image" 
                />
                <p>Age: {selectedChild.age}</p>
                <p>Gender: {selectedChild.gender}</p>
                <p>Location: {selectedChild.location}</p>
                <h4>Health History:</h4>
                <p>{selectedChild.health}</p>
                <h4>Background:</h4>
                <p>{selectedChild.background}</p>
                <button className="close-btn" onClick={closePopup}>
                  Close
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Adopt;




