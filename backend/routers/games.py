from fastapi import APIRouter, HTTPException
from db import cursor, conn
from schemas.game import NewGameRequest
import uuid

router = APIRouter()

@router.get("/games/{game_id}")
async def get_game(game_id: str):
    cursor.execute(
        """
        SELECT game.id, puzzles.name, game.current_state, puzzles.solution
        FROM game
        JOIN puzzles ON game.puzzle_id = puzzles.id
        WHERE game.id = ?
        """,
        (game_id,)
    )
    game = cursor.fetchone()

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"id": game[0], "puzzle_name": game[1], "current_state": game[2], "solution": game[3]}

@router.post("/games", status_code=201)
async def create_game(request: NewGameRequest):
    cursor.execute("SELECT puzzle FROM puzzles WHERE id = ?", (request.puzzle_id,))
    puzzle = cursor.fetchone()
    if puzzle is None:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    game_id = str(uuid.uuid4())

    cursor.execute(
        "INSERT INTO game (id, puzzle_id, current_state, initial_state) VALUES (?, ?, ?, ?)",
        (game_id, request.puzzle_id, puzzle[0], puzzle[0])
    )
    conn.commit()

    return {"game_id": game_id}

@router.get("/games")
async def list_games():
    """Endpoint to list all games with their IDs, puzzle names, and current states."""
    cursor.execute(
        """
        SELECT game.id, puzzles.name, game.current_state
        FROM game
        JOIN puzzles ON game.puzzle_id = puzzles.id
        """
    )
    games = cursor.fetchall()

    return [
        {"id": game[0], "puzzle_name": game[1], "current_state": game[2]}
        for game in games
    ]