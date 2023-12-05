import json
from pydantic import BaseModel
from src.embedding.openai import get_embedding as get_openai_embedding

TABLE_NAME = 'sounds'

SCHEMA_CREATE = f'''
  CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
      id serial PRIMARY KEY,
      title text NOT NULL,
      genres TEXT[],
      bpm integer,
      duration_in_seconds integer,
      credits jsonb,
      openai_embedding vector(1536),
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
    openai_embedding: list[float] | None = None

    def to_db(self) -> dict:
        doc = self.model_dump()
        del doc['id']
        text = sound_text(doc)
        doc['openai_embedding'] = get_openai_embedding(text)
        doc['credits'] = json.dumps(doc['credits'])
        return doc

def to_response(doc: dict) -> dict:
  # FastAPI JSON serialize does not work with numpy arrays, see:
  # https://stackoverflow.com/questions/71102658/how-can-i-return-a-numpy-array-using-fastapi
  response_doc = { **doc }
  del response_doc['openai_embedding'] # this vector is large and not super useful to the end user
  return response_doc

def format_response(data: dict) -> dict:
  if type(data) == list:
     return [to_response(doc) for doc in data]
  else:
     return to_response(data)

def credit_text(credit: dict) -> str:
   if credit['role']:
      return f"{credit['name']} ({credit['role'].lower()})"
   else:
      return credit['name']

# Create a textual representation of a sound, something like:
# "Sunrise by Norah Jones in genre adult standards with bpm 157"
def sound_text(doc: dict) -> str:
   parts = []
   if doc['title']:
      parts.append(doc['title'])
   if doc['credits']:
      parts.append('by')
      credit_strings = [credit_text(credit) for credit in doc['credits']]
      parts.append(', '.join(credit_strings))
   if doc['genres']:
      parts.append('in genres')
      parts.append(', '.join(doc['genres']))
   if doc['bpm']:
      parts.append('with bpm')
      parts.append(str(doc['bpm']))
   return ' '.join(parts).strip()
