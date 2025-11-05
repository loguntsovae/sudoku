from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import Game, Puzzle
from sqlalchemy.orm import selectinload
from schemas.game import NewGameRequest
from schemas.response import GameResponse, GameListResponse
from dependencies import get_db
import uuid

router = APIRouter()


@router.get("/games/{game_id}", response_model=GameResponse)
async def get_game(game_id: str, db: AsyncSession = Depends(get_db)):
    query = (
        select(Game)
        .options(selectinload(Game.puzzle))
        .where(Game.id == game_id)
    )
    game = (await db.execute(query)).scalar_one_or_none()

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    return GameResponse(
        id=game.id,
        puzzle_name=game.puzzle.name,
        current_state=game.current_state,
        solution=game.puzzle.solution,
    )

@router.post("/games", status_code=201)
async def create_game(request: NewGameRequest, db: AsyncSession = Depends(get_db)):
    query = select(Puzzle).where(Puzzle.id == request.puzzle_id)
    puzzle = (await db.execute(query)).scalar_one_or_none()

    if puzzle is None:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    game_id = str(uuid.uuid4())
    new_game = Game(
        id=game_id,
        puzzle_id=request.puzzle_id,
        current_state=puzzle.puzzle,
        initial_state=puzzle.puzzle,
    )
    db.add(new_game)
    await db.commit()
    await db.refresh(new_game)

    return {"game_id": new_game.id}

@router.get("/games", response_model=list[GameListResponse])
async def list_games(db: AsyncSession = Depends(get_db)):
    query = select(Game).join(Game.puzzle)
    games = (await db.execute(query)).scalars().all()

    return [
        GameListResponse(
            id=game.id,
            puzzle_name=game.puzzle.name,
            current_state=game.current_state,
        )
        for game in games
    ]