import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PuzzleList from './components/PuzzleList';
import PuzzleSolver from './components/PuzzleSolver';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Sudoku App</h1>
        <Routes>
          <Route path="/" element={<PuzzleList />} />
          <Route path="/solve/:gameId" element={<PuzzleSolver />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;