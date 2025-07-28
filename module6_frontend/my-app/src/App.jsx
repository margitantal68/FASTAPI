import { Routes, Route, Link } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import ListUsers from "./pages/UsersList";
import Home from "./pages/Home";
import React from "react";



export default function App() {
  return (
    <div className="p-6 font-sans">
  
      <div className="mt-16" />
      <nav className="space-x-4 mb-6">
        <Link to="/" className="text-blue-600 hover:underline">Home</Link>
        &nbsp; &nbsp;
        <Link to="/register" className="text-blue-600 hover:underline">Register</Link>
        &nbsp; &nbsp; 
        <Link to="/login" className="text-blue-600 hover:underline">Login</Link>
        &nbsp; &nbsp; 
        <Link to="/users" className="text-blue-600 hover:underline">Users</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/users" element={<ListUsers />} />
      </Routes>
    </div>
  );
}

