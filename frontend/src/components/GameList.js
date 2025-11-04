import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './GameList.css';

function GameList() {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8004/games")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch games");
        }
        return response.json();
      })
      .then((data) => {
        setGames(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading games...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="game-list">
      <h1>Game List</h1>
      {games.length === 0 ? (
        <p>No games available. Start a new game to see it here!</p>
      ) : (
        <ul>
          {games.map((game) => (
            <li key={game.id}>
              <Link to={`/solve/${game.id}`}>{game.puzzle_name}</Link> - {game.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default GameList;