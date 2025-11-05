from fastapi import WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict
import asyncio
from db import Game, Puzzle
from dependencies import get_db

# Dictionary to keep track of active WebSocket connections
active_connections: Dict[int, WebSocket] = {}

async def fetch_game_data(game_id, db: AsyncSession):
    result = await db.execute(
        select(Game.current_state, Game.initial_state, Puzzle.solution)
        .join(Puzzle, Game.puzzle_id == Puzzle.id)
        .where(Game.id == game_id)
    )
    return result.one_or_none()

async def update_game_state(game_id, updated_state, db: AsyncSession):
    result = await db.execute(
        select(Game).where(Game.id == game_id)
    )
    game = result.scalar()
    if game:
        game.current_state = updated_state
        await db.commit()

async def handle_auto_solver(websocket, game_id, auto_solver_tasks, db: AsyncSession):
    """Run the auto-solver to fill in missing values in the puzzle."""
    try:
        while True:
            result = await db.execute(
                select(Game.current_state, Puzzle.solution)
                .join(Puzzle, Game.puzzle_id == Puzzle.id)
                .where(Game.id == game_id)
            )
            game = result.one_or_none()
            if not game:
                await websocket.send_text("Game not found")
                break

            current_state = list(game[0])
            solution = game[1]

            if '0' not in current_state:
                await websocket.send_json({"message": "all is done"})
                break

            empty_index = current_state.index('0')
            correct_value = solution[empty_index]
            current_state[empty_index] = correct_value
            updated_state = "".join(current_state)

            await update_game_state(game_id, updated_state, db)

            await websocket.send_json({"index": empty_index, "value": correct_value})
            await asyncio.sleep(3)
    except asyncio.CancelledError:
        await websocket.send_text("Auto solver stopped")
    except Exception as e:
        print(f"Auto solver error: {e}")

async def process_websocket_message(websocket, game_id, data, auto_solver_tasks, db: AsyncSession):
    """Process incoming WebSocket messages."""
    if "index" in data and "value" in data:
        index = data["index"]
        value = data["value"]

        game = await fetch_game_data(game_id, db)
        if not game:
            await websocket.send_text("Game not found")
            return

        current_state = list(game[0])
        initial_state = game[1]
        solution = game[2]

        if initial_state[index] != '0':
            await websocket.send_text("Cannot modify initial puzzle values")
            return

        if value and solution[index] != value:
            await websocket.send_json({"message": "Incorrect value"})
            return

        current_state[index] = value if value else '0'
        updated_state = "".join(current_state)

        await update_game_state(game_id, updated_state, db)

        if updated_state == solution:
            await websocket.send_json({"message": "all is done"})

        await websocket.send_json({"updated_state": updated_state})

    elif data.get("autoSolver") == "ON":
        if game_id not in auto_solver_tasks or auto_solver_tasks[game_id].done():
            task = asyncio.create_task(handle_auto_solver(websocket, game_id, auto_solver_tasks, db))
            auto_solver_tasks[game_id] = task
            await websocket.send_text("Auto solver started")

    elif data.get("autoSolver") == "OFF":
        task = auto_solver_tasks.get(game_id)
        if task and not task.done():
            task.cancel()
        await websocket.send_text("Auto solver stopped")

async def websocket_game_endpoint(websocket: WebSocket, game_id: str, db: AsyncSession = Depends(get_db)):
    """WebSocket endpoint for managing game interactions."""
    await websocket.accept()
    active_connections[game_id] = websocket
    auto_solver_tasks: dict[str, asyncio.Task] = {}

    try:
        while True:
            data = await websocket.receive_json()
            await process_websocket_message(websocket, game_id, data, auto_solver_tasks, db)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if game_id in active_connections:
            del active_connections[game_id]
        task = auto_solver_tasks.get(game_id)
        if task and not task.done():
            task.cancel()