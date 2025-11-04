import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './PuzzleList.css';

function PuzzleList() {
  const [puzzles, setPuzzles] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch puzzles from the backend
    fetch('http://localhost:8004/puzzles')
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (Array.isArray(data)) {
          setPuzzles(data);
        } else {
          console.error('Unexpected response format:', data);
        }
      })
      .catch((error) => console.error('Error fetching puzzles:', error));
  }, []);

  const handlePuzzleClick = async (id) => {
    try {
      // Create a new game for the selected puzzle
      const response = await fetch(`http://localhost:8004/games`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ puzzle_id: id }),
      });

      if (!response.ok) {
        throw new Error(`Failed to create game: ${response.status}`);
      }

      const game = await response.json();

      // Navigate to the game page with the game ID
      navigate(`/solve/${game.game_id}`);
    } catch (error) {
      console.error('Error creating game:', error);
    }
  };

  return (
    <div className="puzzle-list">
      <h2>Available Puzzles</h2>
      <ul>
        {puzzles.map((puzzle) => (
          <li key={puzzle.id} onClick={() => handlePuzzleClick(puzzle.id)}>
            {puzzle.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PuzzleList;