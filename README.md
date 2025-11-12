# Sudoku — portfolio project

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![CI](https://github.com/loguntsovae/sudoku/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/loguntsovae/sudoku/actions/workflows/ci.yml)

Quick summary: an interactive Sudoku app with a React frontend and a FastAPI backend. The app supports selecting puzzles, step-by-step solving, an auto-solver, and real-time updates via WebSocket.

## What's included
- Frontend: React (Create React App)
- Backend: FastAPI
- Database: SQLite (local)
- Communication: WebSockets for real-time updates

## Screenshot / Demo
Add a screenshot or a short GIF of the app to `./assets` and reference it here: `![demo](./assets/demo.png)`.

## Quick start (development)
Terminal: zsh (macOS)

1) Start the backend

```bash
cd backend
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
# Install the backend package (pyproject.toml declares dependencies)
python -m pip install -e .
# Run the server
uvicorn main:app --reload --port 8004
```

2) Start the frontend

```bash
cd frontend
npm install
npm start
# Open http://localhost:3000
```

## Production build

1) Build the frontend

```bash
cd frontend
npm ci
npm run build
# The static build will be available in frontend/build
```

2) Deploying the backend

You can deploy the FastAPI backend to any platform (Heroku, Railway, DigitalOcean, etc.). For production, run the app behind a process manager (uvicorn/gunicorn) and a reverse proxy (nginx) and use environment variables for DB and secrets.

## Architecture & contract
- The frontend communicates with the backend via WebSocket and REST. Key entry points:
  - WebSocket: see `backend/routers/websocket_routes.py`
  - REST endpoints: see files in `backend/routers/`

Simplified contract:
- The client sends events with the current board state and receives auto-solver steps in response.

## Who is this for
- A good showcase of skills: React, FastAPI, WebSockets, project structure and deployment.

## Contributing
To propose improvements, open an issue or a pull request. See `CONTRIBUTING.md` for basic guidelines.

## License
This project is licensed under the MIT License — see `LICENSE`.

## Contact
Author: Aleksei Loguntsov — add your email or GitHub profile link here.

---
If you'd like, I can also add a `Dockerfile`, example `docker-compose.yml`, or a demo GIF — tell me which you'd prefer.