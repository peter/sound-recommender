import json
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from datetime import datetime

TABLE_NAME = 'playlists'

SCHEMA_CREATE = f'''
  CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
      id serial PRIMARY KEY,
      title text NOT NULL,
      sounds jsonb NOT NULL,
      created_at TIMESTAMP NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMP NOT NULL DEFAULT NOW()
  );
'''

SCHEMA_DROP = f'''
  DROP TABLE IF EXISTS {TABLE_NAME};
'''

class Playlist(BaseModel):
    id: int | None = None
    title: str
    sounds: Annotated[list[int], Field(max_length=1000)]

    def to_db(self) -> dict:
        doc = self.model_dump()
        if 'id' in doc:
          del doc['id']
        if 'created_at' in doc:
          del doc['created_at']
        doc['updated_at'] = datetime.now()
        doc['sounds'] = json.dumps(doc['sounds'])
        return doc
