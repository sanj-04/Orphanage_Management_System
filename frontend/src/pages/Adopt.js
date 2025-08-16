// import { useNavigate } from "react-router-dom";
// import "./CSS/Adopt.css";
// import React, { useState, useEffect } from "react";
// import axios from "axios";

// const Adopt = () => {
//   const navigate = useNavigate();
//   const [childrenData, setChildrenData] = useState([]);
//   const [selectedChild, setSelectedChild] = useState(null);
//   const [popupType, setPopupType] = useState(null); // "adopt", "confirm", "more"

//   const handleBack = () => navigate("/");

//   useEffect(() => {
//     axios.get("http://127.0.0.1:8000/children/") // Django API endpoint
//       .then((res) => setChildrenData(res.data))
//       .catch((err) => console.error(err));
//   }, []);

//   const openAdoptPopup = (child) => {
//     setSelectedChild(child);
//     setPopupType("adopt");
//   };

//   const confirmAdoption = () => {
//     setPopupType("confirm");
//   };

//   const openMorePopup = (child) => {
//     setSelectedChild(child);
//     setPopupType("more");
//   };

//   const closePopup = () => {
//     setSelectedChild(null);
//     setPopupType(null);
//   };

//   return (
//     <div className="adopt-container">
//       {/* /*<button className="back-btn" onClick={handleBack}>
//         ← Back
//       </button>// */}

//       <h1>Meet Our Children</h1>
//       <p>These children are looking for loving families.</p>

//       <div className="child-grid">
//         {childrenData.map((child) => (
//           <div className="child-card" key={child.id}>
//             <img src={`http://127.0.0.1:8000${child.image}`} alt={child.name} />
//             <h3>{child.name}</h3>
//             <p>Age: {child.age}</p>
//             <p>Gender: {child.gender}</p>
//             <p>Location: {child.location}</p>
//             <div className="card-buttons">
//             <button className="adopt-btn" onClick={() => openAdoptPopup(child)}>
//               Adopt
//             </button>
//             <button className="more-btn" onClick={() => openMorePopup(child)}>
//               More
//             </button></div>

//           </div>
//         ))}
//       </div>

//       {/* Popup Overlay */}
//       {popupType && (
//         <div className="popup-overlay" onClick={closePopup}>
//           <div className="popup-box" onClick={(e) => e.stopPropagation()}>
//             {popupType === "adopt" && (
//               <>
//                 <h2>Confirm Adoption</h2>
//                 <p>
//                   Are you sure you're interested in adopting
//                   <strong>{selectedChild.name}</strong>?
//                 </p>
//                 <div className="popup-buttons">
//                   <button className="yes-btn" onClick={confirmAdoption}>
//                     Yes
//                   </button>
//                   <button className="no-btn" onClick={closePopup}>
//                     No
//                   </button>
//                 </div>
//               </>
//             )}

//             {popupType === "confirm" && (
//               <>
//                 <h2>Adoption Request Sent</h2>
//                 <p>You will be contacted by organisation.</p>
//                 <button className="ok-btn" onClick={closePopup}>
//                   OK
//                 </button>
//               </>
//             )}

//             {popupType === "more" && (
//               <>
//                 <h2>{selectedChild.name}</h2>
//                 <img
//                   src={`http://127.0.0.1:8000${selectedChild.image}`} alt={selectedChild.name} className="popup-image" 
//                 />
//                 <p>Age: {selectedChild.age}</p>
//                 <p>Gender: {selectedChild.gender}</p>
//                 <p>Location: {selectedChild.location}</p>
//                 <h4>Health History:</h4>
//                 <p>{selectedChild.health}</p>
//                 <h4>Background:</h4>
//                 <p>{selectedChild.background}</p>
//                 <button className="close-btn" onClick={closePopup}>
//                   Close
//                 </button>
//               </>
//             )}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Adopt;

import { useNavigate } from "react-router-dom";
import "./CSS/Adopt.css";
import React, { useState, useEffect } from "react";
import axios from "axios";

const Adopt = () => {
  const navigate = useNavigate();
  const [childrenData, setChildrenData] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [popupType, setPopupType] = useState(null); // "adopt", "confirm", "more"
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // const handleBack = () => navigate("/");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/children-list/")// ✅ correct Django API endpoint
      .then((res) => {
        setChildrenData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching children:", err);
        setError("Failed to load children. Please try again later.");
        setLoading(false);
      });
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
      {/* <button className="back-btn" onClick={handleBack}>
        ← Back
      </button> */}

      <h1>Meet Our Children</h1>
      <p>These children are looking for loving families.</p>

      {/* Show loader, error, or children */}
      {loading ? (
        <p className="loading-text">Loading children...</p>
      ) : error ? (
        <p className="error-text">{error}</p>
      ) : childrenData.length === 0 ? (
        <p className="empty-text">No children available.</p>
      ) : (
        <div className="child-grid">
          {childrenData.map((child) => (
            <div className="child-card" key={child.id}>
              <img src={child.image} alt={child.name} />
              <h3>{child.name}</h3>
              <p>Age: {child.age}</p>
              <p>Gender: {child.gender}</p>
              <p>Location: {child.location}</p>
              <div className="card-buttons">
                <button
                  className="adopt-btn"
                  onClick={() => openAdoptPopup(child)}
                >
                  Adopt
                </button>
                <button
                  className="more-btn"
                  onClick={() => openMorePopup(child)}
                >
                  More
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Popup Overlay */}
      {popupType && (
        <div className="popup-overlay" onClick={closePopup}>
          <div className="popup-box" onClick={(e) => e.stopPropagation()}>
            {popupType === "adopt" && (
              <>
                <h2>Confirm Adoption</h2>
                <p>
                  Are you sure you're interested in adopting{" "}
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
                  src={`http://127.0.0.1:8000${selectedChild.image}`}
                  alt={selectedChild.name}
                  className="popup-image"
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



