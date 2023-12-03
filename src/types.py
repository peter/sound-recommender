from pydantic import BaseModel

class Credit(BaseModel):
    name: str
    role: str

class Sound(BaseModel):
    id: int | None = None
    title: str
    genres: list[str]
    bpm: int | None = None
    duration_in_seconds: int | None = None
    credits: list[Credit]
