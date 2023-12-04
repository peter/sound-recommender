import json
from pydantic import BaseModel
import src.db.pg as pg

SCHEMA_SQL_CREATE = '''
  CREATE TABLE IF NOT EXISTS sounds (
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

SCHEMA_SQL_DROP = '''
  DROP TABLE IF EXISTS sounds;
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

    def to_db_dict(self) -> dict:
        doc = self.model_dump()
        del doc['id']
        doc['credits'] = json.dumps(doc['credits'])
        return doc

def create_schema():
  pg.execute(SCHEMA_SQL_CREATE)

def drop_schema():
  pg.execute(SCHEMA_SQL_DROP)
