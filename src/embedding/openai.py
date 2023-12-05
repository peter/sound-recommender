import traceback
import os
from openai import OpenAI
import timeit

API_KEY = os.environ.get("OPENAI_API_KEY")

def is_enabled() -> bool:
   return bool(API_KEY)

client = None
if is_enabled():
    client = OpenAI(
        api_key=API_KEY,
    )

def get_embedding(text, model="text-embedding-ada-002"):
   if not is_enabled():
      return None
   text = text.replace("\n", " ")
   log_prefix = 'embedding.openapi get_embedding'
   try:
      start = timeit.timeit()
      embedding = client.embeddings.create(input = [text], model=model).data[0].embedding
      elapsed = timeit.timeit() - start
      print(f'{log_prefix} - success elapsed={elapsed} length={len(embedding)}')
      return embedding
   except Exception as error:
      print(f'{log_prefix} - error thrown', error, traceback.format_exc())
