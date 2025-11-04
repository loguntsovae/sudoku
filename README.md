# Sudoku App

## Overview
This is a Sudoku application with a React frontend and FastAPI backend. Users can select puzzles, solve them, and interact with the backend in real-time using WebSockets. The app also features an auto-solver for users who want assistance in completing puzzles.

## Features
- Display a list of Sudoku puzzles.
- Create and solve Sudoku games.
- Real-time updates using WebSockets.
- Auto-solver feature to automatically solve puzzles step-by-step.

## Installation

### Backend
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8004
   ```

### Frontend
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm start
   ```

## Usage
1. Open the frontend in your browser at `http://localhost:3000`.
2. Select a puzzle and start solving.
3. Enable the auto-solver if you want the app to assist you in solving the puzzle.

## Development
### Backend
- Python 3.9+
- FastAPI
- SQLite

### Frontend
- React
- WebSockets

## License
MIT