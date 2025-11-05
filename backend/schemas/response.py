from pydantic import BaseModel

class GameResponse(BaseModel):
    id: str
    puzzle_name: str
    current_state: str
    solution: str

class GameListResponse(BaseModel):
    id: str
    puzzle_name: str
    current_state: str