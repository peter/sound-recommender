from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

# Root - redirects to OpenAPI documentation
@app.get("/")
def root():
    return RedirectResponse(url='/docs')

# Create sound(s)
@app.post("/admin/sounds")
def sounds_create():
    return { 'data': [ { 'id': 1, 'title': 'Hallelujah' } ] }

# List sounds
@app.get("/sounds")
def sounds_list():
    return { 'data': [ { 'id': 1, 'title': 'Hallelujah' } ] }

# Create playlist(s)
@app.post("/playlists")
def playlists_create():
    return { 'data': [] }

# Get recommended sounds from playlist
@app.get("/sounds/recommended")
def sounds_recommended():
    return { 'data': [] }
