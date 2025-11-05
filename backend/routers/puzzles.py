from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from dependencies import get_db
from db import Puzzle
from schemas import PuzzleOut

router = APIRouter()

@router.get("/puzzles", response_model=Page[PuzzleOut])
async def get_puzzles(db: AsyncSession = Depends(get_db)):
    query = select(Puzzle)
    return await paginate(db, query)

@router.get("/puzzles/{puzzle_id}", response_model=PuzzleOut)
async def get_puzzle(puzzle_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Puzzle).where(Puzzle.id == puzzle_id)
    puzzle = (await db.execute(query)).scalar_one_or_none()
    if puzzle is None:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    return PuzzleOut.from_orm(puzzle)