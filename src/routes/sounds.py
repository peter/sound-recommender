from pydantic import BaseModel
from fastapi import APIRouter, Response, status
from typing import Any
import src.models.sound as sound_model
from src.models.sound import Sound
import src.db.pg as pg

router = APIRouter()

# Admin create sound(s) (one or more sounds)
class SoundsCreateBody(BaseModel):
    data: list[Sound]
@router.post("/admin/sounds")
def sounds_create(body: SoundsCreateBody):
    for sound in body.data:
        id = pg.create(sound_model.TABLE_NAME, sound.to_db())
        sound.id = id
    return { 'data': body.data }

# Admin update sound
@router.put("/admin/sounds/{id}")
def sounds_update(id: int, body: Sound):
    result = pg.update(sound_model.TABLE_NAME, id, body.to_db())
    if result.rowcount > 0:
        data = { **body.model_dump(), 'id': id }
        return { 'data': data }
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

# Admin delete sound
@router.delete("/admin/sounds/{id}")
def sounds_delete(id: int):
    result = pg.delete(sound_model.TABLE_NAME, id)
    status_code = status.HTTP_200_OK if result.rowcount > 0 else status.HTTP_404_NOT_FOUND
    return Response(status_code=status_code)
    
# List sounds
class SoundsResponseBody(BaseModel):
    data: list[Sound]
@router.get("/sounds")
def sounds_list(limit: int | None = 100, offset: int | None = 0, query: str | None = None) -> SoundsResponseBody:
    filter = { 'description': { 'value': query, 'op': 'contains' } } if query else None
    data = pg.find(sound_model.TABLE_NAME, limit=limit, offset=offset, filter=filter)
    return { 'data': data }

# Get sound
class SoundResponseBody(BaseModel):
    data: Sound
@router.get("/sounds/{id}")
def sounds_get(id: int) -> SoundResponseBody:
    data = pg.find_one(sound_model.TABLE_NAME, id)
    if not data:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return { 'data': data }
