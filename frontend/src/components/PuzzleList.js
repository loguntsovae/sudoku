import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './PuzzleList.css';

function PuzzleList() {
  const [puzzles, setPuzzles] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch puzzles from the backend with pagination
    fetch(`http://localhost:8004/puzzles?page=${page}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data.items && Array.isArray(data.items)) {
          setPuzzles(data.items);
          setTotalPages(data.pages);
        } else {
          console.error('Unexpected response format:', data);
        }
      })
      .catch((error) => console.error('Error fetching puzzles:', error));
  }, [page]);

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

  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1);
    }
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1);
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
      <div className="pagination-controls">
        <button onClick={handlePreviousPage} disabled={page === 1}>
          Previous
        </button>
        <span>
          Page {page} of {totalPages}
        </span>
        <button onClick={handleNextPage} disabled={page === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
}

export default PuzzleList;