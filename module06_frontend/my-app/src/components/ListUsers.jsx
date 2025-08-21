import React, { useEffect, useState } from 'react';

const ListUsers = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            setLoading(false);
            console.error("No token found, please login first.");
            alert("You must be logged in to view the users list.");
            window.location.href = "/login"; // Redirect to login page
            return;
        }
        fetch('http://localhost:8000/users',
             {headers: 
                {Authorization: `Bearer ${token}`, token: localStorage.getItem("token")},
            }
        )
            .then((res) => res.json())
            .then((data) => {
                setUsers(data);
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, []);

    if (loading) return <div>Loading users...</div>;

    return (
        <div>
            <h2>Registered Users</h2>
            {users.length === 0 ? (
                <p>No users found.</p>
            ) : (
                <ul>
                    {users.map((user) => (
                        <li key={user.id}>
                            {user.id}. {user.username} ({user.email})
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default ListUsers;