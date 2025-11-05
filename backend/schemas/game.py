from pydantic import BaseModel

class NewGameRequest(BaseModel):
    puzzle_id: int