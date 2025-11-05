import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PuzzleList from './components/PuzzleList';
import PuzzleSolver from './components/PuzzleSolver';
import Header from './components/Header';
import MainLayout from './components/MainLayout';
import Footer from './components/Footer';
import Login from './components/Login';
import Register from './components/Register';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<MainLayout />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/solve/:gameId" element={<PuzzleSolver />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;