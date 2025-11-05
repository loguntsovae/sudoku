from db import cursor, conn
from .sudoku_generator import SudokuGenerator
from random_word import RandomWords

def ensure_minimum_puzzles(min_puzzles=6):
    cursor.execute("SELECT COUNT(*) FROM puzzles")
    puzzle_count = cursor.fetchone()[0]

    if puzzle_count < min_puzzles:
        generator = SudokuGenerator()
        word_generator = RandomWords()
        for _ in range(min_puzzles - puzzle_count):
            puzzle, solution = generator.generate_sudoku()
            unique_name = None

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