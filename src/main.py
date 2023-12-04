import json
from typing import Union
from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import src.db.pg as pg
import src.models.sound as sound
from src.models.sound import Sound

pg.connect()
app = FastAPI()

# Root - redirects to OpenAPI documentation
@app.get("/")
def root():
    return RedirectResponse(url='/docs')

class SoundsCreateBody(BaseModel):
    data: list[Sound]

# Admin create sound(s) (one or more sounds)
@app.post("/admin/sounds")
# def sounds_create(data: list[Sound]):
def sounds_create(body: SoundsCreateBody):
    for sound in body.data:
        id = pg.create('sounds', sound.to_db_dict())
        sound.id = id
    return { 'data': body.data }

# Admin update sound
@app.put("/admin/sounds/{id}")
def sounds_update(id: int, sound: Sound):
    result = pg.update('sounds', id, sound.to_db_dict())
    if result.rowcount > 0:
        return { 'sound': sound }
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

# Admin delete sound
@app.delete("/admin/sounds/{id}")
def sounds_delete(id: int):
    result = pg.delete('sounds', id)
    status_code = status.HTTP_200_OK if result.rowcount > 0 else status.HTTP_404_NOT_FOUND
    return Response(status_code=status_code)
    
# List sounds
@app.get("/sounds")
def sounds_list():
    sounds = pg.find('sounds')
    return { 'data': sounds }

# Get sound
@app.get("/sounds/{id}")
def sounds_get(id: int):
    sound = pg.find_one('sounds', id)
    return { 'data': sound }

# Create playlist(s) (one or more playlists)
@app.post("/playlists")
def playlists_create():
    return { 'data': [] }

# Get recommended sounds from playlist
@app.get("/sounds/recommended")
def sounds_recommended():
    return { 'data': [] }
