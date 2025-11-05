from fastapi import WebSocket
from typing import Dict
import asyncio
from db import cursor, conn

# Dictionary to keep track of active WebSocket connections
active_connections: Dict[int, WebSocket] = {}

def fetch_game_data(game_id):
    """Fetch the current state, initial state, and solution for a game."""
    cursor.execute(
        """
        SELECT game.current_state, game.initial_state, puzzles.solution
        FROM game
        JOIN puzzles ON game.puzzle_id = puzzles.id
        WHERE game.id = ?
        """,
        (game_id,)
    )
    return cursor.fetchone()

def update_game_state(game_id, updated_state):
    """Update the current state of the game in the database."""
    cursor.execute(
        "UPDATE game SET current_state = ? WHERE id = ?",
        (updated_state, game_id)
    )
    conn.commit()

async def handle_auto_solver(websocket, game_id, auto_solver_tasks):
    """Run the auto-solver to fill in missing values in the puzzle."""
    try:
        while True:
            cursor.execute(
                """
                SELECT game.current_state, puzzles.solution
                FROM game
                JOIN puzzles ON game.puzzle_id = puzzles.id
                WHERE game.id = ?
                """,
                (game_id,)
            )
            game = cursor.fetchone()
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

            update_game_state(game_id, updated_state)

            await websocket.send_json({"index": empty_index, "value": correct_value})
            await asyncio.sleep(3)
    except asyncio.CancelledError:
        await websocket.send_text("Auto solver stopped")
    except Exception as e:
        print(f"Auto solver error: {e}")

async def process_websocket_message(websocket, game_id, data, auto_solver_tasks):
    """Process incoming WebSocket messages."""
    if "index" in data and "value" in data:
        index = data["index"]
        value = data["value"]

        game = fetch_game_data(game_id)
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

        update_game_state(game_id, updated_state)

        if updated_state == solution:
            await websocket.send_json({"message": "all is done"})

        await websocket.send_json({"updated_state": updated_state})

    elif data.get("autoSolver") == "ON":
        if game_id not in auto_solver_tasks or auto_solver_tasks[game_id].done():
            task = asyncio.create_task(handle_auto_solver(websocket, game_id, auto_solver_tasks))
            auto_solver_tasks[game_id] = task
            await websocket.send_text("Auto solver started")

    elif data.get("autoSolver") == "OFF":
        task = auto_solver_tasks.get(game_id)
        if task and not task.done():
            task.cancel()
        await websocket.send_text("Auto solver stopped")

async def websocket_game_endpoint(websocket: WebSocket, game_id: str):
    """WebSocket endpoint for managing game interactions."""
    await websocket.accept()
    active_connections[game_id] = websocket
    auto_solver_tasks: dict[str, asyncio.Task] = {}

    try:
        while True:
            data = await websocket.receive_json()
            await process_websocket_message(websocket, game_id, data, auto_solver_tasks)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if game_id in active_connections:
            del active_connections[game_id]
        task = auto_solver_tasks.get(game_id)
        if task and not task.done():
            task.cancel()