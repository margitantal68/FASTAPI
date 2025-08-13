import { Routes, Route, Link } from "react-router-dom";

import Register from "./pages/Register";
import Login from "./pages/Login";
import ListUsers from "./pages/UsersList";
import Home from "./pages/Home";

import React from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

const GITHUB_AUTH_URL = "http://localhost:8000/auth/github/login"; // backend GitHub login URL


function OAuthCallbackHandler() {
  const location = useLocation();         
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const token = params.get("token");
    console.log("OAuthCallbackHandler token:", token);

    if (token) {
      localStorage.setItem("token", token);
      navigate("/");
    } else {
      console.error("GitHub login failed or no token found.");
      navigate("/login");
    }
  }, [location, navigate]); // ✅ include location in dependency list

  return <p>Logging in with GitHub...</p>;
}




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
        &nbsp; &nbsp; 
        <button
          onClick={() => window.location.href = GITHUB_AUTH_URL}
          className="text-white bg-black px-3 py-1 rounded hover:bg-gray-800 ml-4"
        >
          Login with GitHub
        </button>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/users" element={<ListUsers />} />
        <Route path="/oauth/callback" element={<OAuthCallbackHandler />} />
      </Routes>
    </div>
  );
}

