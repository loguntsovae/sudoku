import React from 'react';
import './MainLayout.css';

const MainLayout = () => {
  return (
    <div className="main-layout">
      <div className="left-column">
        <h2>Available Puzzles</h2>
        {/* Add puzzle preview icons here */}
      </div>
      <div className="center-column">
        <h2>Puzzle Details</h2>
        {/* Add puzzle details like difficulty, rating, and Play button */}
      </div>
      <div className="right-column">
        <h2>Recent Games</h2>
        {/* Add recent or saved games here */}
      </div>
    </div>
  );
};

export default MainLayout;