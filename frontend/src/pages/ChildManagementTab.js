import React, { useEffect, useState } from "react";
import axios from "axios";

const ChildTab = () => {
  const [children, setChildren] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    name: "",
    age: "",
    gender: "",
    location: "",
    health: "",
    background: "",
    image: null,
  });
  const [editingId, setEditingId] = useState(null);

  // Fetch children
  const fetchChildren = async () => {
    try {
      const res = await axios.get("/api/children/");
      setChildren(res.data);
    } catch (err) {
      console.error("Error fetching children:", err);
    } finally {
      setLoading(false);
    }
  };

  // Handle form changes
  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: files ? files[0] : value,
    }));
  };

  // Submit new or edited child
  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = new FormData();
    for (let key in formData) {
      if (formData[key] !== null) {
        payload.append(key, formData[key]);
      }
    }

    try {
      if (editingId) {
        await axios.put(`/api/children/${editingId}/`, payload, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        setEditingId(null);
      } else {
        await axios.post("/api/children/", payload, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      }
      setFormData({
        name: "",
        age: "",
        gender: "",
        location: "",
        health: "",
        background: "",
        image: null,
      });
      fetchChildren();
    } catch (err) {
      console.error("Error saving child:", err);
    }
  };

  // Edit child
  const handleEdit = (child) => {
    setFormData({
      name: child.name,
      age: child.age,
      gender: child.gender,
      location: child.location,
      health: child.health,
      background: child.background,
      image: null, // Don't pre-fill file input
    });
    setEditingId(child.id);
  };

  // Delete child
  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this child?")) return;
    try {
      await axios.delete(`/api/children/${id}/`);
      fetchChildren();
    } catch (err) {
      console.error("Error deleting child:", err);
    }
  };

  useEffect(() => {
    fetchChildren();
  }, []);

  if (loading) return <p>Loading children...</p>;

  return (
    <div className="child-tab">
      <h2>Child Management</h2>

      {/* Add/Edit Child Form */}
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
        <input type="number" name="age" placeholder="Age" value={formData.age} onChange={handleChange} required />
        <input type="text" name="gender" placeholder="Gender" value={formData.gender} onChange={handleChange} required />
        <input type="text" name="location" placeholder="Location" value={formData.location} onChange={handleChange} required />
        <textarea name="health" placeholder="Health Details" value={formData.health} onChange={handleChange} required />
        <textarea name="background" placeholder="Background" value={formData.background} onChange={handleChange} required />
        <input type="file" name="image" accept="image/*" onChange={handleChange} />
        <button type="submit">{editingId ? "Update Child" : "Add Child"}</button>
      </form>

      {/* Children Table */}
      {children.length === 0 ? (
        <p>No children found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Photo</th>
              <th>Name</th>
              <th>Age</th>
              <th>Gender</th>
              <th>Location</th>
              <th>Health</th>
              <th>Background</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {children.map((child) => (
              <tr key={child.id}>
                <td>
                  {child.image && (
                    <img src={child.image} alt={child.name} style={{ height: "50px" }} />
                  )}
                </td>
                <td>{child.name}</td>
                <td>{child.age}</td>
                <td>{child.gender}</td>
                <td>{child.location}</td>
                <td>{child.health}</td>
                <td>{child.background}</td>
                <td>
                  <button onClick={() => handleEdit(child)} style={{ marginRight: "5px" }}>Edit</button>
                  <button onClick={() => handleDelete(child.id)} style={{ backgroundColor: "red", color: "white" }}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ChildTab;
