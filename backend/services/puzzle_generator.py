from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from db import Puzzle
from .sudoku_generator import SudokuGenerator
from random_word import RandomWords
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import AsyncSessionLocal

async def ensure_minimum_puzzles(min_puzzles=6):
    async with AsyncSessionLocal() as db:
        async with db.begin():
            result = await db.execute(select(Puzzle))
            puzzle_count = len(result.scalars().all())

            if puzzle_count < min_puzzles:
                generator = SudokuGenerator()
                word_generator = RandomWords()
                for _ in range(min_puzzles - puzzle_count):
                    puzzle, solution = generator.generate_sudoku()
                    unique_name = None

                    while not unique_name:
                        name = word_generator.get_random_word()
                        try:
                            await db.execute(select(Puzzle).where(Puzzle.name == name))
                        except NoResultFound:
                            unique_name = name

                    new_puzzle = Puzzle(
                        name=unique_name,
                        puzzle=''.join(map(str, [num for row in puzzle for num in row])),
                        solution=''.join(map(str, [num for row in solution for num in row]))
                    )
                    db.add(new_puzzle)
                await db.commit()