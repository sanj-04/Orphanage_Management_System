import React, { useState } from "react";
import axios from "axios";
import'./CSS/Register.css';

const Register = () => {
  const initialFormData = {
    father_name: "",
    father_email: "",
    father_phone: "",
    father_aadhar: "",
    father_age: "",
    mother_name: "",
    mother_email: "",
    mother_phone: "",
    mother_aadhar: "",
    mother_age: "",
    address: "",
    reason: "",
    document: null,
  };

  const [formData, setFormData] = useState(initialFormData);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "file" ? files[0] : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessMessage("");
    setErrorMessage("");

    const formPayload = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      formPayload.append(key, value);
    });

    try {
      const res = await axios.post("http://127.0.0.1:8000/register/", formPayload, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSuccessMessage(res.data.message || "Registration successful!");
      setFormData(initialFormData);
    } catch (err) {
      if (err.response?.data) {
        const errorData = err.response.data;
        const formatted = Object.entries(errorData)
          .map(([key, val]) => {
            const message = Array.isArray(val) ? val.join(", ") : val;
            return `${key.replaceAll("_", " ")}: ${message}`;
          })
          .join("\n");
        setErrorMessage(formatted);
      } else {
        setErrorMessage("Something went wrong. Please try again.");
      }
    }
  };

  return (
          <div className="register-page">
            <div className="register-card">
              <h2>Parent Registration</h2>

              {errorMessage && (
                <div style={{ color: "red", whiteSpace: "pre-line", marginBottom: 10 }}>{errorMessage}</div>
              )}
              {successMessage && (
                <div style={{ color: "green", marginBottom: 10 }}>{successMessage}</div>
              )}

              <form onSubmit={handleSubmit} encType="multipart/form-data">
              <div className="parent-section">
                <div className="column">
                  <h4>Father's Details</h4>
                  <input type="text" name="father_name" placeholder="Father's Name" value={formData.father_name} onChange={handleChange} />
                  <input type="email" name="father_email" placeholder="Father's Email" value={formData.father_email} onChange={handleChange} />
                  <input type="text" name="father_phone" placeholder="Father's Phone" value={formData.father_phone} onChange={handleChange} maxLength={10} />
                  <input type="text" name="father_aadhar" placeholder="Father's Aadhar" value={formData.father_aadhar} onChange={handleChange} />
                  <input type="number" name="father_age" placeholder="Father's Age" value={formData.father_age} onChange={handleChange} />
                </div>
                <div className="column">
                  <h4>Mother's Details</h4>
                  <input type="text" name="mother_name" placeholder="Mother's Name" value={formData.mother_name} onChange={handleChange} />
                  <input type="email" name="mother_email" placeholder="Mother's Email" value={formData.mother_email} onChange={handleChange} />
                  <input type="text" name="mother_phone" placeholder="Mother's Phone" value={formData.mother_phone} onChange={handleChange} maxLength={10} />
                  <input type="text" name="mother_aadhar" placeholder="Mother's Aadhar" value={formData.mother_aadhar} onChange={handleChange} />
                  <input type="number" name="mother_age" placeholder="Mother's Age" value={formData.mother_age} onChange={handleChange} />
                </div>
              </div>
              <div className="additional-section">
                <h4>Home & Adoption Details</h4>
                <textarea name="address" placeholder="Home Address" value={formData.address} onChange={handleChange} required />
                <textarea name="reason" placeholder="Reason for Adoption" value={formData.reason} onChange={handleChange} required />

                <label>Upload Document (PDF, JPG, PNG)</label>
                <input type="file" name="document" accept=".pdf,.jpg,.jpeg,.png" onChange={handleChange} required />
              </div>
                <button type="submit">Submit Registration</button>
              </form>
            </div>
          </div>
  );
};

export default Register;
