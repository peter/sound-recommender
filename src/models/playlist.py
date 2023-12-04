import json
from pydantic import BaseModel

TABLE_NAME = 'playlists'

SCHEMA_CREATE = f'''
  CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
      id serial PRIMARY KEY,
      title text NOT NULL,
      sounds jsonb NOT NULL
  );
'''

SCHEMA_DROP = f'''
  DROP TABLE IF EXISTS {TABLE_NAME};
'''

class Playlist(BaseModel):
    id: int | None = None
    title: str
    sounds: list[int]

    def to_db(self) -> dict:
        doc = self.model_dump()
        del doc['id']
        doc['sounds'] = json.dumps(doc['sounds'])
        return doc
