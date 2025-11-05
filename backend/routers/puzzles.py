from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import SessionLocal, Puzzle

router = APIRouter()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

@router.get("/puzzles")
async def get_puzzles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Puzzle.id, Puzzle.name))
    puzzles = result.all()
    return [{"id": row[0], "name": row[1]} for row in puzzles]

@router.get("/puzzles/{puzzle_id}")
async def get_puzzle(puzzle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Puzzle).where(Puzzle.id == puzzle_id))
    puzzle = result.scalar()
    if puzzle is None:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    return {"id": puzzle.id, "name": puzzle.name, "puzzle": puzzle.puzzle}