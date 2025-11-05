from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import puzzles_router, games_router, websocket_game_endpoint, auth
from services.puzzle_generator import ensure_minimum_puzzles
from db import create_tables


app = FastAPI(
    title="Sudoku API",
    description="A FastAPI backend for managing Sudoku puzzles and games with real-time WebSocket communication.",
    version="1.0.0",
    contact={
        "name": "Sudoku Support",
        "email": "support@sudokuapp.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    on_startup=[ensure_minimum_puzzles, create_tables]
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(puzzles_router, prefix="", tags=["Puzzles"])
app.include_router(games_router, prefix="", tags=["Games"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# WebSocket endpoint
app.add_api_websocket_route("/ws/games/{game_id}", websocket_game_endpoint)