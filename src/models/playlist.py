import json
from pydantic import BaseModel
import src.db.pg as pg

SCHEMA_SQL_CREATE = '''
  CREATE TABLE IF NOT EXISTS playlists (
      id serial PRIMARY KEY,
      title text NOT NULL
  );

  CREATE TABLE IF NOT EXISTS playlists_sounds (
      playlist_id integer references playlists(id) on delete cascade,
      sound_id integer references sounds(id) on delete cascade
  );
'''

SCHEMA_SQL_DROP = '''
  DROP TABLE IF EXISTS playlists_sounds;
  DROP TABLE IF EXISTS playlists;
'''

class Playlist(BaseModel):
    id: int | None = None
    title: str
    sounds: list[int]

def create_schema():
  pg.execute(SCHEMA_SQL_CREATE)

def drop_schema():
  pg.execute(SCHEMA_SQL_DROP)
