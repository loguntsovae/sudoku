from pydantic import BaseModel

class PuzzleOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
