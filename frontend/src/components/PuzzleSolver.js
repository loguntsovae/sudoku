import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './SudokuGrid.css';
import './PuzzleSolver.css';

function PuzzleSolver() {
  const { gameId } = useParams();
  const [puzzle, setPuzzle] = useState(null);
  const [socket, setSocket] = useState(null);
  const [notification, setNotification] = useState('');
  const [autoSolver, setAutoSolver] = useState(false);

  useEffect(() => {
    let ws;
    fetch(`http://localhost:8004/games/${gameId}`)
      .then((res) => res.json())
      .then((data) => {
        setPuzzle(data);
        ws = new WebSocket(`ws://localhost:8004/ws/games/${gameId}`);
        setSocket(ws);
        ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data);
            if (message.message === 'all is done') {
              setNotification('🎉 Puzzle completed!');
            } else if (message.message === 'Incorrect value') {
              setNotification('⚠️ Incorrect value!');
              setPuzzle((prev) => {
                const updated = prev.current_state.split('');
                updated[message.index] = 'X';
                return { ...prev, current_state: updated.join('') };
              });
            } else if (message.index !== undefined && message.value !== undefined) {
              setPuzzle((prev) => {
                const updated = prev.current_state.split('');
                updated[message.index] = message.value;
                return { ...prev, current_state: updated.join('') };
              });
            }
          } catch (err) {
            console.error('WebSocket message error:', err);
          }
        };
      })
      .catch((err) => console.error('Fetch error:', err));
    return () => ws && ws.close();
  }, [gameId]);

  useEffect(() => {
    if (!socket || socket.readyState !== WebSocket.OPEN) return;
    socket.send(JSON.stringify({ autoSolver: autoSolver ? 'ON' : 'OFF' }));
  }, [autoSolver, socket]);

  const handleInputChange = (index, value) => {
    if (!value.match(/^[1-9]?$/)) {
      setNotification('Enter 1–9 only');
      return;
    }
    setPuzzle((prev) => {
      const updated = prev.current_state.split('');
      updated[index] = value || '0';
      return { ...prev, current_state: updated.join('') };
    });
    socket?.send(JSON.stringify({ index, value }));
  };

  if (!puzzle) return <div className="loading">Loading...</div>;

  return (
    <div className="puzzle-container">
      <div className="main-panel">
        <h2 className="puzzle-title">{puzzle.puzzle_name}</h2>
        {notification && <div className="notification">{notification}</div>}
        <div className="sudoku-grid">
          {puzzle.current_state.split('').map((cell, i) => (
            <div
              key={i}
              className={`sudoku-cell ${cell !== '0' ? 'pre-filled' : ''}`}
              style={{ gridRow: Math.floor(i / 9) + 1, gridColumn: (i % 9) + 1 }}
            >
              {cell !== '0' ? (
                cell
              ) : (
                <input
                  type="text"
                  maxLength="1"
                  className="sudoku-input"
                  onChange={(e) => handleInputChange(i, e.target.value)}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="side-panel">
        <div className="side-box">
          <h3>Controls</h3>
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={autoSolver}
              onChange={() => setAutoSolver((p) => !p)}
            />
            Auto Solver
          </label>
          <button
            className="reset-btn"
            onClick={() => window.location.reload()}
          >
            🔁 Reset Game
          </button>
        </div>
      </div>
    </div>
  );
}

export default PuzzleSolver;