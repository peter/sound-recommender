import json
from pydantic import BaseModel
import numpy as np
from random import randint

TABLE_NAME = 'sounds'

SCHEMA_CREATE = f'''
  CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
      id serial PRIMARY KEY,
      title text NOT NULL,
      genres TEXT[],
      bpm integer,
      duration_in_seconds integer,
      credits jsonb,
      embedding vector(3),
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
    embedding: list[int] | None = None

    def to_db(self) -> dict:
        doc = self.model_dump()
        del doc['id']
        doc['credits'] = json.dumps(doc['credits'])
        doc['embedding'] = np.array([randint(0, 10), randint(0, 10), randint(0, 10)])
        return doc

def to_response(doc: dict) -> dict:
  # FastAPI JSON serialize does not work with numpy arrays, see:
  # https://stackoverflow.com/questions/71102658/how-can-i-return-a-numpy-array-using-fastapi  
  return { **doc, 'embedding': doc['embedding'].tolist() }  

def format_response(data: dict) -> dict:
  if type(data) == list:
     return [to_response(doc) for doc in data]
  else:
     return to_response(data)
