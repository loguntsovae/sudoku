import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="logo">Sudoku App</div>
      <nav className="nav">
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/puzzles" className="nav-link">Puzzles</Link>
        <Link to="/leaderboard" className="nav-link">Leaderboard</Link>
        <Link to="/profile" className="nav-link">Profile</Link>
        <Link to="/login" className="nav-link">Login</Link>
        <Link to="/register" className="nav-link">Register</Link>
      </nav>
    </header>
  );
};

export default Header;