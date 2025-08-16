import React, { useEffect, useState } from "react";
import axios from "axios";

const AdoptionTab = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch applications
  const fetchApplications = async () => {
    try {
      const res = await axios.get("/api/adoptions/");
      setApplications(res.data);
    } catch (err) {
      console.error("Error fetching applications:", err);
    } finally {
      setLoading(false);
    }
  };

  // Approve or Reject application
  const updateStatus = async (id, status) => {
    try {
      await axios.patch(`/api/adoptions/${id}/`, { status });
      fetchApplications(); // refresh list
    } catch (err) {
      console.error("Error updating status:", err);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  if (loading) return <p>Loading applications...</p>;

  return (
    <div className="adoption-tab">
      <h2>Adoption Applications</h2>
      {applications.length === 0 ? (
        <p>No applications found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Applicant</th>
              <th>Child</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Status</th>
              <th>Submitted</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {applications.map(app => (
              <tr key={app.id}>
                <td>{app.full_name}</td>
                <td>{app.child_name}</td>
                <td>{app.email}</td>
                <td>{app.phone}</td>
                <td>{app.status}</td>
                <td>{new Date(app.created_at).toLocaleString()}</td>
                <td>
                  {app.status === "Pending" && (
                    <>
                      <button
                        onClick={() => updateStatus(app.id, "Approved")}
                        style={{ marginRight: "5px" }}
                      >
                        Approve
                      </button>
                      <button
                        onClick={() => updateStatus(app.id, "Rejected")}
                        style={{ backgroundColor: "red", color: "white" }}
                      >
                        Reject
                      </button>
                    </>
                  )}
                  {app.status !== "Pending" && <em>No actions</em>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AdoptionTab;
