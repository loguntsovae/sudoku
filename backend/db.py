import sqlite3

# Initialize SQLite database
conn = sqlite3.connect("sudoku.db", check_same_thread=False)
cursor = conn.cursor()

# Create puzzles table if it does not exist
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS puzzles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        puzzle TEXT NOT NULL,
        solution TEXT
    )
    """)

    # Create game table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS game (
        id TEXT PRIMARY KEY,
        puzzle_id INTEGER NOT NULL,
        current_state TEXT NOT NULL,
        initial_state TEXT,
        FOREIGN KEY (puzzle_id) REFERENCES puzzles (id)
    )
    """)

    conn.commit()

# Call the function to ensure tables are created
create_tables()