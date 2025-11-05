from fastapi import APIRouter, HTTPException
from db import cursor

router = APIRouter()

@router.get("/puzzles")
async def get_puzzles():
    cursor.execute("SELECT id, name FROM puzzles")
    puzzles = cursor.fetchall()
    return [{"id": row[0], "name": row[1]} for row in puzzles]

@router.get("/puzzles/{puzzle_id}")
async def get_puzzle(puzzle_id: int):
    cursor.execute("SELECT id, name, puzzle FROM puzzles WHERE id = ?", (puzzle_id,))
    puzzle = cursor.fetchone()
    if puzzle is None:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    return {"id": puzzle[0], "name": puzzle[1], "puzzle": puzzle[2]}