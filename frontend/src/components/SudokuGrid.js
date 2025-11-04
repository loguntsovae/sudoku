import React from 'react';
import './SudokuGrid.css';

function SudokuGrid() {
  const grid = Array(9).fill(null).map(() => Array(9).fill(''));

  return (
    <div className="sudoku-grid">
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
  );
}

export default SudokuGrid;