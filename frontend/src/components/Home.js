import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const [username, setUsername] = useState(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchUsername = async () => {
      if (token) {
        const response = await fetch('http://localhost:8004/auth/me', {
          method: 'GET',
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.ok) {
          const data = await response.json();
          setUsername(data.username);
        }
      }
    };
    fetchUsername();
  }, [token]);

  return (
    <div className="home-container">
      <h1>Welcome to Sudoku App</h1>
      <p>Your ultimate destination for solving Sudoku puzzles!</p>

      {token ? (
        <div>
          <h2>Welcome back, {username || 'User'}!</h2>
          <button onClick={() => {
            localStorage.removeItem('token');
            window.location.reload();
          }}>Logout</button>
        </div>
      ) : (
        <div>
          <Link to="/login" className="home-link">Login</Link>
          <Link to="/register" className="home-link">Register</Link>
        </div>
      )}

      <div className="home-navigation">
        <Link to="/play" className="home-link">Play Sudoku</Link>
        <Link to="/puzzles" className="home-link">View Puzzles</Link>
      </div>

      <div className="home-info">
        <h3>How to Play</h3>
        <p>Fill the grid so that every row, column, and 3x3 box contains the digits 1 to 9 without repeating.</p>
      </div>
    </div>
  );
};

export default Home;