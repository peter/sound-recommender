import json
from typing import Union
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import src.db.pg as pg
from src.types import Sound

pg.connect()
pg.create_schema()
app = FastAPI()

# Root - redirects to OpenAPI documentation
@app.get("/")
def root():
    return RedirectResponse(url='/docs')

class SoundsCreateBody(BaseModel):
    data: list[Sound]

def sound_dict(sound: Sound) -> dict:
    doc = sound.model_dump()
    del doc['id']
    doc['credits'] = json.dumps(doc['credits'])
    return doc

# Create sound(s)
@app.post("/admin/sounds")
# def sounds_create(data: list[Sound]):
def sounds_create(body: SoundsCreateBody):
    for sound in body.data:
        id = pg.create('sounds', sound_dict(sound))
        sound.id = id
    return { 'data': body.data }

# List sounds
@app.get("/sounds")
def sounds_list():
    sounds = pg.find('sounds')
    return { 'data': sounds }

# Get sound
@app.get("/sounds/{id}")
def sounds_list(id: int):
    sound = pg.find_one('sounds', id)
    return { 'data': sound }

# Create playlist(s)
@app.post("/playlists")
def playlists_create():
    return { 'data': [] }

# Get recommended sounds from playlist
@app.get("/sounds/recommended")
def sounds_recommended():
    return { 'data': [] }
