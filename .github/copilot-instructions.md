# AI Coding Agent Instructions for Sudoku App

## Project Overview
This repository contains a Sudoku application with the following components:

- **Frontend**: A React-based user interface located in the `frontend/` directory. It communicates with the backend via WebSockets.
- **Backend**: A FastAPI server located in the `backend/` directory. It handles puzzle generation, solving logic, and real-time communication.

The app allows users to select, solve, and auto-solve Sudoku puzzles with real-time updates.

---

## Key Files and Directories

### Frontend
- `frontend/src/components/`: Contains React components such as `SudokuGrid` (renders the puzzle) and `ControlPanel` (user controls).
- `frontend/public/index.html`: The entry point for the React app.
- `frontend/src/index.js`: Initializes the React app.

### Backend
- `backend/main.py`: Entry point for the FastAPI server.
- `backend/sudoku_generator.py`: Contains logic for generating Sudoku puzzles.
- `backend/pyproject.toml`: Python project configuration.

---

## Developer Workflows

### Starting the Application
1. **Backend**:
   - Navigate to the `backend` directory.
   - Initialize the environment: `uv sync`.
   - Start the server: `uvicorn main:app --reload --port 8004`.

2. **Frontend**:
   - Navigate to the `frontend` directory.
   - Install dependencies: `npm install`.
   - Start the development server: `npm start`.

### Testing
- **Backend**: Add tests in the `backend/tests/` directory (if it exists). Use `pytest` to run tests.
- **Frontend**: Add tests in `frontend/src/__tests__/`. Use `npm test` to run tests.

### Debugging
- Use the `--reload` flag with `uvicorn` for live-reloading the backend.
- Use React Developer Tools for debugging the frontend.

---

## Project-Specific Conventions

### Backend
- Follow FastAPI conventions for defining routes and dependencies.
- Use SQLite as the default database for simplicity.
- WebSocket endpoints are defined in `main.py` for real-time communication.

### Frontend
- Use functional components with hooks (e.g., `useState`, `useEffect`).
- CSS files are colocated with their respective components for modular styling.
- WebSocket communication is managed in `PuzzleSolver.js`.

---

## Integration Points
- **WebSockets**: The frontend communicates with the backend in real-time using WebSockets. Ensure the WebSocket URL matches the backend server's address.
- **Auto-Solver**: The backend provides step-by-step solutions to puzzles, which the frontend renders dynamically.

---

## External Dependencies
- **Backend**:
  - FastAPI: Web framework.
  - SQLite: Database.
- **Frontend**:
  - React: UI library.
  - WebSocket API: Real-time communication.

---

## Examples

### Adding a New Backend Route
1. Define the route in `main.py`:
   ```python
   @app.get("/new-route")
   async def new_route():
       return {"message": "Hello, World!"}
   ```

2. Test the route using `curl`:
   ```bash
   curl http://localhost:8004/new-route
   ```

### Creating a New React Component
1. Create a new file in `frontend/src/components/` (e.g., `NewComponent.js`).
2. Define the component:
   ```javascript
   import React from 'react';

   const NewComponent = () => {
       return <div>New Component</div>;
   };

   export default NewComponent;
   ```
3. Import and use it in `App.js`.

---

For further details, refer to the `README.md` or explore the codebase.