from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from contextlib import asynccontextmanager

import asyncio

# Initialize SQLite database
DATABASE_URL = "sqlite+aiosqlite:///sudoku.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

class Puzzle(Base):
    __tablename__ = 'puzzles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    puzzle = Column(String, nullable=False)
    solution = Column(String)

class Game(Base):
    __tablename__ = 'game'

    id = Column(String, primary_key=True, index=True)
    puzzle_id = Column(Integer, ForeignKey('puzzles.id'), nullable=False)
    current_state = Column(String, nullable=False)
    initial_state = Column(String)

    puzzle = relationship("Puzzle")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
