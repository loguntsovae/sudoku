import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PuzzleList from './components/PuzzleList';
import PuzzleSolver from './components/PuzzleSolver';
import GameList from './components/GameList';
import './index.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <header className="app-header">
          <h1>Sudoku App</h1>
          <p>Challenge your mind with our exciting puzzles!</p>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<><PuzzleList /><GameList /></>} />
            <Route path="/solve/:gameId" element={<PuzzleSolver />} />
          </Routes>
        </main>
        <footer className="app-footer">
          <p>&copy; 2025 Sudoku App. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));