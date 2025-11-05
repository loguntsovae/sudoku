import React, { useState } from 'react';
import './SudokuGrid.css';

const SudokuGrid = () => {
  const [completed, setCompleted] = useState(false);
  const grid = Array(9).fill(null).map(() => Array(9).fill(''));

  const handleComplete = () => {
    setCompleted(true);
    setTimeout(() => {
      alert('Congratulations! You completed the puzzle!');
    }, 500);
  };

  return (
    <div className="sudoku-container">
      <div className={`sudoku-grid ${completed ? 'completed' : ''}`}>
        {grid.map((row, rowIndex) => (
          <div key={rowIndex} className="sudoku-row">
            {row.map((cell, cellIndex) => (
              <input
                key={cellIndex}
                className="sudoku-cell"
                type="text"
                maxLength="1"
              />
            ))}
          </div>
        ))}
      </div>
      <div className="sidebar">
        <button onClick={handleComplete}>Complete</button>
        <button>Hint</button>
        <button>Reset</button>
      </div>
    </div>
  );
};

export default SudokuGrid;