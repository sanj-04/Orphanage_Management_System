import React, { useEffect, useState } from "react";
import axios from "axios";

const RegistrationTab = () => {
  const [registrations, setRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchRegistrations = async () => {
    try {
      const res = await axios.get("/api/registrations/");
      setRegistrations(res.data);
    } catch (err) {
      console.error("Error fetching registrations:", err);
    } finally {
      setLoading(false);
    }
  };

  const approveRegistration = async (id) => {
    try {
      await axios.post(`/api/registrations/${id}/approve/`);
      fetchRegistrations();
    } catch (err) {
      console.error("Error approving registration:", err);
    }
  };

  const denyRegistration = async (id) => {
    try {
      await axios.post(`/api/registrations/${id}/deny/`);
      fetchRegistrations();
    } catch (err) {
      console.error("Error denying registration:", err);
    }
  };

  useEffect(() => {
    fetchRegistrations();
  }, []);

  if (loading) return <p>Loading registrations...</p>;

  return (
    <div className="registration-tab">
      <h2>Registration Requests</h2>
      {registrations.length === 0 ? (
        <p>No registration requests found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Father</th>
              <th>Mother</th>
              <th>Emails</th
