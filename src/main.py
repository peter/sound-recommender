from typing import Union
from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import numpy as np
import src.db.pg as pg
from src.embedding.similarity import cosine_similarity, euclidian_distance

import src.models.sound as sound
from src.models.sound import Sound

import src.models.playlist as playlist
from src.models.playlist import Playlist

pg.connect()
app = FastAPI()

##############################################
# API doc endpoints
##############################################

# Root - redirects to OpenAPI documentation
@app.get("/")
def root():
    return RedirectResponse(url='/docs')

##############################################
# Recommendation endpoints
##############################################

# Get recommended sounds from playlist
@app.get("/sounds/recommended")
def sounds_recommended(
    playlistId: int | None = None,
    soundId: int | None = None,
    strategy: str | None = 'pgvector',
    similarityMetric: str | None = 'cosine_similarity'
):
    if playlistId:
        playlist_obj = pg.find_one(playlist.TABLE_NAME, playlistId)
        if not playlist_obj or not playlist_obj['sounds']:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        # TODO: use average embedding of sounds in playlist?
        sound_ids = playlist_obj['sounds']
        sound_obj = pg.find_one(sound.TABLE_NAME, playlist_obj['sounds'][0])
    elif soundId:
        sound_ids = [soundId]
        sound_obj = pg.find_one(sound.TABLE_NAME, soundId)
    if not sound_obj or sound_obj['openai_embedding'] is None:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    openai_embedding = sound_obj['openai_embedding']
    if not similarityMetric in ('cosine_similarity', 'euclidian_distance'):
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if strategy == 'pgvector':
        # Use pgvector cosine similarity
        similarityOperator = '<=>' if similarityMetric == 'cosine_similarity' else '<->'
        data = pg.query(f'''
            SELECT *
            FROM {sound.TABLE_NAME}
            WHERE id not in %s
            AND openai_embedding is NOT NULL
            ORDER BY openai_embedding {similarityOperator} %s
            LIMIT 3
        ''', (tuple(sound_ids), openai_embedding,))
    elif strategy == 'all':
        # Fetch all sounds and manually sort them by cosine similarity
        data_unsorted = pg.query(f'''
            SELECT *
            FROM {sound.TABLE_NAME}
            WHERE id not in %s
            AND openai_embedding is NOT NULL
        ''', (tuple(sound_ids),))
        for doc in data_unsorted:
            doc['euclidian_distance'] = euclidian_distance(openai_embedding, doc['openai_embedding'])
            doc['cosine_similarity'] = cosine_similarity(openai_embedding, doc['openai_embedding'])
        data = list(sorted(data_unsorted, key=lambda doc: doc[similarityMetric]))
    else:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return { 'data': sound.format_response(data) }

##############################################
# Sound endpoints
##############################################

# Admin create sound(s) (one or more sounds)
class SoundsCreateBody(BaseModel):
    data: list[Sound]
@app.post("/admin/sounds")
# def sounds_create(data: list[Sound]):
def sounds_create(body: SoundsCreateBody):
    for sound_obj in body.data:
        id = pg.create(sound.TABLE_NAME, sound_obj.to_db())
        sound_obj.id = id
    return { 'data': body.data }

# Admin update sound
@app.put("/admin/sounds/{id}")
def sounds_update(id: int, body: Sound):
    result = pg.update(sound.TABLE_NAME, id, body.to_db())
    if result.rowcount > 0:
        data = { **body.model_dump(), 'id': id }
        return { 'data': data }
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

# Admin delete sound
@app.delete("/admin/sounds/{id}")
def sounds_delete(id: int):
    result = pg.delete(sound.TABLE_NAME, id)
    status_code = status.HTTP_200_OK if result.rowcount > 0 else status.HTTP_404_NOT_FOUND
    return Response(status_code=status_code)
    
# List sounds
@app.get("/sounds")
def sounds_list():
    data = pg.find(sound.TABLE_NAME)
    for doc in data:
        print(sound.sound_text(doc))
    return { 'data': sound.format_response(data) }

# Get sound
@app.get("/sounds/{id}")
def sounds_get(id: int):
    data = pg.find_one(sound.TABLE_NAME, id)
    return { 'data': sound.format_response(data) }

##############################################
# Playlist endpoints
##############################################

# Create playlist(s) (one or more playlists)
class PlaylistsCreateBody(BaseModel):
    data: list[Playlist]
@app.post("/playlists")
def playlists_create(body: PlaylistsCreateBody):
    for playlist_obj in body.data:
        id = pg.create(playlist.TABLE_NAME, playlist_obj.to_db())
        playlist_obj.id = id
    return { 'data': body.data }

# List playlists
@app.get("/playlists")
def playlists_list():
    playlists = pg.find(playlist.TABLE_NAME)
    return { 'data': playlists }

# Get playlist
@app.get("/playlists/{id}")
def playlists_get(id: int):
    playlist_obj = pg.find_one(playlist.TABLE_NAME, id)
    return { 'data': playlist_obj }

# Update playlist
@app.put("/playlists/{id}")
def playlists_update(id: int, body: Playlist):
    result = pg.update(playlist.TABLE_NAME, id, body.to_db())
    if result.rowcount > 0:
        data = { **body.model_dump(), 'id': id }
        return { 'data': data }
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

# Delete playlist
@app.delete("/playlists/{id}")
def playlists_delete(id: int):
    result = pg.delete(playlist.TABLE_NAME, id)
    status_code = status.HTTP_200_OK if result.rowcount > 0 else status.HTTP_404_NOT_FOUND
    return Response(status_code=status_code)
