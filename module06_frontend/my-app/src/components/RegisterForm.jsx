import { useState } from "react";

export default function RegisterForm() {
  const [formData, setFormData] = useState({
    username: "",
    fullname: "",
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");

  const fields = [
    { name: "username", label: "Username", type: "text" },
    { name: "fullname", label: "Full Name", type: "text" },
    { name: "email", label: "Email", type: "text" },
    { name: "password", label: "Password", type: "password" },
  ];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const res = await fetch("http://localhost:8000/users/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Registration failed");
      }

      setMessage(`User ${data.username} registered!`);
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {fields.map((field) => (
        <div key={field.name} className="flex flex-col">
          &nbsp;&nbsp;<label htmlFor={field.name} className="mb-1 font-medium">
            {field.label}
          </label>
          &nbsp;&nbsp;
          <input
            id={field.name}
            name={field.name}
            type={field.type}
            value={formData[field.name]}
            onChange={handleChange}
            required
            className="p-2 border rounded"
          />
        </div>
      ))}
        <br />
        &nbsp;&nbsp;
      <button type="submit" className="bg-blue-600 text-white p-2 rounded w-full">
        Register
      </button>

      {message && <p className="text-center mt-2">{message}</p>}
    </form>
  );
}
