from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import Dict
import uuid
from sudoku_generator import SudokuGenerator
from random_word import RandomWords
import asyncio

# Initialize SQLite database
conn = sqlite3.connect("sudoku.db")
cursor = conn.cursor()

# Create puzzles table
cursor.execute("""
CREATE TABLE IF NOT EXISTS puzzles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    puzzle TEXT NOT NULL,
    solution TEXT
)
""")

# Create game table
cursor.execute("""
CREATE TABLE IF NOT EXISTS game (
    id TEXT PRIMARY KEY,
    puzzle_id INTEGER NOT NULL,
    current_state TEXT NOT NULL,
    initial_state TEXT,
    FOREIGN KEY (puzzle_id) REFERENCES puzzles (id)
)
""")

# Ensure at least 6 puzzles exist in the database
cursor.execute("SELECT COUNT(*) FROM puzzles")
puzzle_count = cursor.fetchone()[0]

if puzzle_count < 6:
    generator = SudokuGenerator()
    word_generator = RandomWords()
    for _ in range(6 - puzzle_count):
        puzzle, solution = generator.generate_sudoku()
        unique_name = None

        # Generate a unique name for the puzzle
        while not unique_name:
            name = word_generator.get_random_word()
            cursor.execute("SELECT COUNT(*) FROM puzzles WHERE name = ?", (name,))
            if cursor.fetchone()[0] == 0:
                unique_name = name

        cursor.execute(
            "INSERT INTO puzzles (name, puzzle, solution) VALUES (?, ?, ?)",
            (unique_name, ''.join(map(str, [num for row in puzzle for num in row])), ''.join(map(str, [num for row in solution for num in row])))
        )
    conn.commit()

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/puzzles")
async def get_puzzles():
    cursor.execute("SELECT id, name FROM puzzles")
    puzzles = cursor.fetchall()
    return [{"id": row[0], "name": row[1]} for row in puzzles]

@app.get("/puzzles/{puzzle_id}")
async def get_puzzle(puzzle_id: int):
    cursor.execute("SELECT id, name, puzzle FROM puzzles WHERE id = ?", (puzzle_id,))
    puzzle = cursor.fetchone()
    if puzzle is None:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    return {"id": puzzle[0], "name": puzzle[1], "puzzle": puzzle[2]}

@app.get("/games/{game_id}")
async def get_game(game_id: str):
    cursor.execute("""
        SELECT game.id, puzzles.name, game.current_state, puzzles.solution
        FROM game
        JOIN puzzles ON game.puzzle_id = puzzles.id
        WHERE game.id = ?
    """, (game_id,))
    game = cursor.fetchone()

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"id": game[0], "puzzle_name": game[1], "current_state": game[2], "solution": game[3]}

class NewGameRequest(BaseModel):
    puzzle_id: int

# Update the create_game endpoint to store the initial state separately
@app.post("/games", status_code=201)
async def create_game(request: NewGameRequest):
    cursor.execute("SELECT puzzle FROM puzzles WHERE id = ?", (request.puzzle_id,))
    puzzle = cursor.fetchone()
    if puzzle is None:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    # Generate a UUID for the new game
    game_id = str(uuid.uuid4())

    # Insert a new game with the initial state set to the puzzle
    cursor.execute(
        "INSERT INTO game (id, puzzle_id, current_state, initial_state) VALUES (?, ?, ?, ?)",
        (game_id, request.puzzle_id, puzzle[0], puzzle[0])
    )
    conn.commit()

    return {"game_id": game_id}


active_connections: Dict[int, WebSocket] = {}

@app.websocket("/ws/games/{game_id}")
async def websocket_game_endpoint(websocket: WebSocket, game_id: str):
    await websocket.accept()
    active_connections[game_id] = websocket
    auto_solver_tasks: dict[str, asyncio.Task] = {}

    async def run_auto_solver():
        try:
            while True:
                # получить текущее состояние и решение
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

                # если нет пустых ячеек — завершить
                if '0' not in current_state:
                    await websocket.send_json({"message": "all is done"})
                    break

                empty_index = current_state.index('0')
                correct_value = solution[empty_index]
                current_state[empty_index] = correct_value
                updated_state = "".join(current_state)

                cursor.execute(
                    "UPDATE game SET current_state = ? WHERE id = ?",
                    (updated_state, game_id)
                )
                conn.commit()

                await websocket.send_json({"index": empty_index, "value": correct_value})
                await asyncio.sleep(3)
        except asyncio.CancelledError:
            await websocket.send_text("Auto solver stopped")
        except Exception as e:
            print(f"Auto solver error: {e}")

    try:
        while True:
            data = await websocket.receive_json()

            # обработка обычных ходов
            if "index" in data and "value" in data:
                index = data["index"]
                value = data["value"]

                cursor.execute(
                    """
                    SELECT game.current_state, game.initial_state, puzzles.solution
                    FROM game
                    JOIN puzzles ON game.puzzle_id = puzzles.id
                    WHERE game.id = ?
                    """,
                    (game_id,)
                )
                game = cursor.fetchone()
                if not game:
                    await websocket.send_text("Game not found")
                    continue

                current_state = list(game[0])
                initial_state = game[1]
                solution = game[2]

                # запрет на изменение исходных значений
                if initial_state[index] != '0':
                    await websocket.send_text("Cannot modify initial puzzle values")
                    continue

                # проверка корректности
                if value and solution[index] != value:
                    await websocket.send_json({"message": "Incorrect value"})
                    continue

                current_state[index] = value if value else '0'
                updated_state = "".join(current_state)

                cursor.execute(
                    "UPDATE game SET current_state = ? WHERE id = ?",
                    (updated_state, game_id)
                )
                conn.commit()

                if updated_state == solution:
                    await websocket.send_json({"message": "all is done"})

                await websocket.send_json({"updated_state": updated_state})

            # включить авто-решатель
            elif data.get("autoSolver") == "ON":
                if game_id not in auto_solver_tasks or auto_solver_tasks[game_id].done():
                    task = asyncio.create_task(run_auto_solver())
                    auto_solver_tasks[game_id] = task
                    await websocket.send_text("Auto solver started")

            # выключить авто-решатель
            elif data.get("autoSolver") == "OFF":
                task = auto_solver_tasks.get(game_id)
                if task and not task.done():
                    task.cancel()
                await websocket.send_text("Auto solver stopped")

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if game_id in active_connections:
            del active_connections[game_id]
        task = auto_solver_tasks.get(game_id)
        if task and not task.done():
            task.cancel()


@app.get("/games")
async def get_all_games():
    cursor.execute("""
        SELECT game.id, puzzles.name, game.current_state, puzzles.solution
        FROM game
        JOIN puzzles ON game.puzzle_id = puzzles.id
    """)
    games = cursor.fetchall()
    return [
        {
            "id": game[0],
            "puzzle_name": game[1],
            "status": "solved" if game[2] == game[3] else "unsolved"
        }
        for game in games
    ]