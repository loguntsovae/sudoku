import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './SudokuGrid.css';

function PuzzleSolver() {
  const { gameId } = useParams(); // Updated to use gameId from URL
  const [puzzle, setPuzzle] = useState(null);
  const [socket, setSocket] = useState(null);
  const [notification, setNotification] = useState(''); // State for notifications
  const [autoSolver, setAutoSolver] = useState(false); // State for auto-solver

  useEffect(() => {
    let ws;

    fetch(`http://localhost:8004/games/${gameId}`)
      .then((response) => response.json())
      .then((data) => {
        setPuzzle(data);
        ws = new WebSocket(`ws://localhost:8004/ws/games/${gameId}`);
        setSocket(ws);

        ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data);
            if (message.message === 'all is done') {
              setNotification('Puzzle is complete!');
            } else if (message.message === 'Incorrect value') {
              setNotification('Warning: Incorrect value entered!');
              setPuzzle((prevPuzzle) => {
                const updated = prevPuzzle.current_state.split('');
                updated[message.index] = 'X';
                return { ...prevPuzzle, current_state: updated.join('') };
              });
            } else if (message.index !== undefined && message.value !== undefined) {
              setPuzzle((prevPuzzle) => {
                const updatedState = prevPuzzle.current_state.split('');
                updatedState[message.index] = message.value;
                return { ...prevPuzzle, current_state: updatedState.join('') };
              });
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };
      })
      .catch((error) => console.error('Error:', error));

    return () => {
      if (ws) ws.close();
    };
  }, [gameId]);

  useEffect(() => {
    if (autoSolver && socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ autoSolver: "ON" }));
    } else if (!autoSolver && socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ autoSolver: "OFF" }));
    }
  }, [autoSolver, socket]);

  const handleInputChange = (index, value) => {
    if (!value.match(/^[1-9]?$/)) {
      setNotification('Invalid input! Please enter a number between 1 and 9.');
      return;
    }

    setPuzzle((prevPuzzle) => {
      const updatedState = prevPuzzle.current_state.split('');
      updatedState[index] = value || '0'; // Reset to initial state if empty
      return { ...prevPuzzle, current_state: updatedState.join('') };
    });

    if (socket) {
      socket.send(JSON.stringify({ index, value }));
    }
  };

  const toggleAutoSolver = () => {
    setAutoSolver((prev) => !prev);
  };

  if (!puzzle || !puzzle.current_state || !puzzle.solution) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>{puzzle.puzzle_name}</h2>
      {notification && <div className="notification">{notification}</div>} {/* Display notification */}
      <div>
        <label>
          <input
            type="checkbox"
            checked={autoSolver}
            onChange={toggleAutoSolver}
          />
          Auto-Solver
        </label>
      </div>
      <div className="sudoku-grid">
        {puzzle.current_state.split('').map((cell, index) => (
          <div
            key={index}
            className={`sudoku-cell ${cell !== '0' ? 'pre-filled' : ''}`}
            style={{ gridRow: Math.floor(index / 9) + 1, gridColumn: (index % 9) + 1 }}
          >
            {cell !== '0' ? (
              cell
            ) : (
              <input
                type="text"
                maxLength="1"
                className="sudoku-input"
                onChange={(e) => handleInputChange(index, e.target.value)}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default PuzzleSolver;