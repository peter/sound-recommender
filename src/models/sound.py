import json
from pydantic import BaseModel

TABLE_NAME = 'sounds'

SCHEMA_CREATE = f'''
  CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
      id serial PRIMARY KEY,
      title text NOT NULL,
      genres TEXT[],
      bpm integer,
      duration_in_seconds integer,
      credits jsonb,
      created_at TIMESTAMP NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMP NOT NULL DEFAULT NOW()
  );
'''

SCHEMA_DROP = f'''
  DROP TABLE IF EXISTS {TABLE_NAME};
'''

class Credit(BaseModel):
    name: str
    role: str

class Sound(BaseModel):
    id: int | None = None
    title: str
    genres: list[str]
    bpm: int | None = None
    duration_in_seconds: int | None = None
    credits: list[Credit]

    def to_db(self) -> dict:
        doc = self.model_dump()
        del doc['id']
        doc['credits'] = json.dumps(doc['credits'])
        return doc
