

// import { useNavigate } from "react-router-dom";
// import "./CSS/Adopt.css";
// import React, { useState, useEffect } from "react";
// import axios from "axios";

// const Adopt = () => {
//   const navigate = useNavigate();
//   const [childrenData, setChildrenData] = useState([]);
//   const [selectedChild, setSelectedChild] = useState(null);
//   const [popupType, setPopupType] = useState(null); // "adopt", "confirm", "more"
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState("");

//   // const handleBack = () => navigate("/");

// useEffect(() => {
//   axios.get("http://127.0.0.1:8000/api/children/")
//     .then((res) => {
//       console.log("Children API response:", res.data); // 👀 debug
//       // if no status in model, just set all children
//       const available = res.data.filter(c => !c.status || c.status === "Available");
//       setChildrenData(available);
//     })
//     .catch((err) => {
//       console.error("Error fetching children:", err);
//       setError("Failed to load children");
//     })
//     .finally(() => {
//       setLoading(false);   // ✅ ensure loading stops always
//     });
// }, []);



//   const openAdoptPopup = (child) => {
//     setSelectedChild(child);
//     setPopupType("adopt");
  
//   };

//   const confirmAdoption = () => {
//     setPopupType("confirm");
//       axios.post("http://127.0.0.1:8000/api/adopt/", {
//         child: selectedChild.id,
//         user: 1, // replace with logged-in user
//     })
//     .then(() => {
//       setPopupType("confirm");
//       setChildrenData(prev => prev.filter(c => c.id !== selectedChild.id)); // hide child
//     })
//     .catch(err => {
//       console.error(err);
//       alert("Failed to submit application");
//     });
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
//       {/* <button className="back-btn" onClick={handleBack}>
//         ← Back
//       </button> */}

//       <h1>Meet Our Children</h1>
//       <p>These children are looking for loving families.</p>

//       {/* Show loader, error, or children */}
//       {loading ? (
//         <p className="loading-text">Loading children...</p>
//       ) : error ? (
//         <p className="error-text">{error}</p>
//       ) : childrenData.length === 0 ? (
//         <p className="empty-text">No children available.</p>
//       ) : (
//         <div className="child-grid">
//           {childrenData.map((child) => (
//             <div className="child-card" key={child.id}>
//               <img src={child.image} alt={child.name} />
//               <h3>{child.name}</h3>
//               <p>Age: {child.age}</p>
//               <p>Gender: {child.gender}</p>
//               <p>Location: {child.location}</p>
//               <div className="card-buttons">
//                 <button
//                   className="adopt-btn"
//                   onClick={() => openAdoptPopup(child)}
//                 >
//                   Adopt
//                 </button>
//                 <button
//                   className="more-btn"
//                   onClick={() => openMorePopup(child)}
//                 >
//                   More
//                 </button>
//               </div>
//             </div>
//           ))}
//         </div>
//       )}

//       {/* Popup Overlay */}
//       {popupType && (
//         <div className="popup-overlay" onClick={closePopup}>
//           <div className="popup-box" onClick={(e) => e.stopPropagation()}>
//             {popupType === "adopt" && (
//               <>
//                 <h2>Confirm Adoption</h2>
//                 <p>
//                   Are you sure you're interested in adopting{" "}
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
//                 <img src={selectedChild.image} alt={selectedChild.name} className="popup-image" />
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



// import { useNavigate } from "react-router-dom";
// import "./CSS/Adopt.css";
// import React, { useState, useEffect } from "react";
// import axios from "axios";

// const Adopt = () => {
//   const navigate = useNavigate();
//   const [childrenData, setChildrenData] = useState([]);
//   const [selectedChild, setSelectedChild] = useState(null);
//   const [popupType, setPopupType] = useState(null); // "adopt", "confirm", "more"
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState("");

//   // Load children
//   useEffect(() => {
//     axios
//       .get("http://127.0.0.1:8000/api/children/")
//       .then((res) => {
//         const available = res.data.filter(
//           (c) => !c.status || c.status === "Available"
//         );
//         setChildrenData(available);
//       })
//       .catch((err) => {
//         console.error("Error fetching children:", err);
//         setError("Failed to load children");
//       })
//       .finally(() => {
//         setLoading(false);
//       });
//   }, []);

//   const openAdoptPopup = (child) => {
//     setSelectedChild(child);
//     setPopupType("adopt");
//   };

//   const confirmAdoption = () => {
//   if (!selectedChild) return;

//   const token = localStorage.getItem("token"); // ✅ get token from login
//   const userId = localStorage.getItem("user_id"); // ✅ store user_id after login

//   axios.post(
//     "http://127.0.0.1:8000/api/adopt/",
//     {
//       child: selectedChild.id,
//       user: userId, // use actual logged-in user id
//     },
//     {
//       headers: {
//         Authorization: `Token ${token}`, // ✅ required for IsAuthenticated
//       },
//     }
//   )
//   .then(() => {
//     setPopupType("confirm");

//     // ✅ Refresh children list after adoption
//     axios.get("http://127.0.0.1:8000/api/children/")
//       .then((res) => {
//         const available = res.data.filter(c => !c.status || c.status === "Available");
//         setChildrenData(available);
//       })
//       .catch((err) => {
//         console.error("Error refreshing children:", err);
//         setError("Failed to refresh children list");
//       });
//   })
//   .catch(err => {
//     console.error("Adoption error:", err.response?.data || err.message);
//     alert("Failed to submit application");
//   });
// };


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
//       <h1>Meet Our Children</h1>
//       <p>These children are looking for loving families.</p>

//       {/* Show loader, error, or children */}
//       {loading ? (
//         <p className="loading-text">Loading children...</p>
//       ) : error ? (
//         <p className="error-text">{error}</p>
//       ) : childrenData.length === 0 ? (
//         <p className="empty-text">No children available.</p>
//       ) : (
//         <div className="child-grid">
//           {childrenData.map((child) => (
//             <div className="child-card" key={child.id}>
//               <img src={child.image} alt={child.name} />
//               <h3>{child.name}</h3>
//               <p>Age: {child.age}</p>
//               <p>Gender: {child.gender}</p>
//               <p>Location: {child.location}</p>
//               <div className="card-buttons">
//                 <button
//                   className="adopt-btn"
//                   onClick={() => openAdoptPopup(child)}
//                 >
//                   Adopt
//                 </button>
//                 <button
//                   className="more-btn"
//                   onClick={() => openMorePopup(child)}
//                 >
//                   More
//                 </button>
//               </div>
//             </div>
//           ))}
//         </div>
//       )}

//       {/* Popup Overlay */}
//       {popupType && (
//         <div className="popup-overlay" onClick={closePopup}>
//           <div className="popup-box" onClick={(e) => e.stopPropagation()}>
//             {popupType === "adopt" && (
//               <>
//                 <h2>Confirm Adoption</h2>
//                 <p>
//                   Are you sure you're interested in adopting{" "}
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
//                   src={selectedChild.image}
//                   alt={selectedChild.name}
//                   className="popup-image"
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

  // Load children
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/children/")
      .then((res) => {
        const available = res.data.filter(
          (c) => !c.status || c.status === "Available"
        );
        setChildrenData(available);
      })
      .catch((err) => {
        console.error("Error fetching children:", err);
        setError("Failed to load children");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const openAdoptPopup = (child) => {
    setSelectedChild(child);
    setPopupType("adopt");
  };

  const confirmAdoption = () => {
  if (!selectedChild) return;

  const token = localStorage.getItem("token"); // ✅ from login

  axios.post(
    "http://127.0.0.1:8000/api/adopt/",
    { child: selectedChild.id }, // ✅ only child needed
    {
      headers: {
        Authorization: `Token ${token}`, // ✅ backend will know user
      },
    }
  )
  .then(() => {
    setPopupType("confirm");

    // Refresh children list
    axios.get("http://127.0.0.1:8000/api/children/")
      .then((res) => {
        const available = res.data.filter(c => !c.status || c.status === "Available");
        setChildrenData(available);
      })
      .catch((err) => {
        console.error("Error refreshing children:", err);
        setError("Failed to refresh children list");
      });
  })
  .catch(err => {
    console.error("Adoption error:", err.response?.data || err.message);
    alert("Failed to submit application");
  });
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
                  src={selectedChild.image}
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
