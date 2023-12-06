from fastapi import FastAPI
from src.routes import api_docs, recommender, sounds, playlists
import src.db.pg as pg

pg.connect()

app = FastAPI()

app.include_router(api_docs.router)
app.include_router(recommender.router)
app.include_router(sounds.router)
app.include_router(playlists.router)
