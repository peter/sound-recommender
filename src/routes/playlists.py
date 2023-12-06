from pydantic import BaseModel
from fastapi import APIRouter, Response, status
import src.models.playlist as playlist_model
from src.models.playlist import Playlist
import src.db.pg as pg

router = APIRouter()

# Create playlist(s) (one or more playlists)
class PlaylistsCreateBody(BaseModel):
    data: list[Playlist]
@router.post("/playlists")
def playlists_create(body: PlaylistsCreateBody):
    for playlist in body.data:
        id = pg.create(playlist_model.TABLE_NAME, playlist.to_db())
        playlist.id = id
    return { 'data': body.data }

# List playlists
@router.get("/playlists")
def playlists_list(limit: int | None = 100, offset: int | None = 0):
    playlists = pg.find(playlist_model.TABLE_NAME, limit=limit, offset=offset)
    return { 'data': playlists }

# Get playlist
@router.get("/playlists/{id}")
def playlists_get(id: int):
    data = pg.find_one(playlist_model.TABLE_NAME, id)
    if not data:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return { 'data': data }

# Update playlist
@router.put("/playlists/{id}")
def playlists_update(id: int, body: Playlist):
    result = pg.update(playlist_model.TABLE_NAME, id, body.to_db())
    if result.rowcount > 0:
        data = { **body.model_dump(), 'id': id }
        return { 'data': data }
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

# Delete playlist
@router.delete("/playlists/{id}")
def playlists_delete(id: int):
    result = pg.delete(playlist_model.TABLE_NAME, id)
    status_code = status.HTTP_200_OK if result.rowcount > 0 else status.HTTP_404_NOT_FOUND
    return Response(status_code=status_code)
