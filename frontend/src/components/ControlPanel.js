import React from 'react';
import './ControlPanel.css';

function ControlPanel() {
  const handleFillSudoku = () => {
    alert('Fill Sudoku button clicked!');
  };

  return (
    <div className="control-panel">
      <button onClick={handleFillSudoku}>Fill Sudoku</button>
    </div>
  );
}

export default ControlPanel;