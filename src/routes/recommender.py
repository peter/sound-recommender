from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import APIRouter, Response, status
import src.models.sound as sound_model
from src.models.sound import Sound
import src.models.playlist as playlist_model
from src.embedding.similarity import cosine_similarity, euclidian_distance, combine_embeddings
import src.db.pg as pg

router = APIRouter()

def get_sound_ids_and_embedding(playlistId, soundId):
    if playlistId:
        playlist = pg.find_one(playlist_model.TABLE_NAME, playlistId)
        if not playlist or not playlist['sounds']:
            return (None, None)
        sound_ids = playlist['sounds']
        all_openai_embeddings = pg.query_values(f'''
          SELECT openai_embedding
          FROM {sound_model.TABLE_NAME}
          WHERE id in %s
          AND openai_embedding IS NOT NULL 
        ''', (tuple(sound_ids),))
        openai_embedding = combine_embeddings(all_openai_embeddings)
    elif soundId:
        sound_ids = [soundId]
        openai_embedding = pg.query_one_value(f'''
          SELECT openai_embedding
          FROM {sound_model.TABLE_NAME}
          where id = %s
        ''', (soundId,))
    return (sound_ids, openai_embedding)

def get_pgvector_similar(openai_embedding, sound_ids, limit, similarityMetric):
    similarity_operator = '<=>' if similarityMetric == 'cosine_similarity' else '<->'
    sql = f'''
        SELECT *
        FROM {sound_model.TABLE_NAME}
        WHERE id not in %s
        AND openai_embedding is NOT NULL
        ORDER BY openai_embedding {similarity_operator} %s
        LIMIT {limit}
    '''
    print(sql)
    data = pg.query(sql, (tuple(sound_ids), openai_embedding,))
    for doc in data:
        doc['euclidian_distance'] = euclidian_distance(openai_embedding, doc['openai_embedding'])
        doc['cosine_similarity'] = cosine_similarity(openai_embedding, doc['openai_embedding'])
    return data

def get_all_similar(openai_embedding, sound_ids, limit, similarityMetric):
    data_unsorted = pg.query(f'''
        SELECT *
        FROM {sound_model.TABLE_NAME}
        WHERE id not in %s
        AND openai_embedding is NOT NULL
    ''', (tuple(sound_ids),))
    for doc in data_unsorted:
        doc['euclidian_distance'] = euclidian_distance(openai_embedding, doc['openai_embedding'])
        doc['cosine_similarity'] = cosine_similarity(openai_embedding, doc['openai_embedding'])
    reverse = True if similarityMetric == 'cosine_similarity' else False
    data_sorted = list(sorted(data_unsorted, key=lambda doc: doc[similarityMetric], reverse=reverse))
    return data_sorted[0:limit]

# Get recommended sounds from playlist or sound
class SoundRecommendation(Sound):
    euclidian_distance: float | None = None
    cosine_similarity: float | None = None
class RecommenderResponseBody(BaseModel):
    data: list[SoundRecommendation]
@router.get("/sounds/recommended")
def sounds_recommended(
    playlistId: int | None = None,
    soundId: int | None = None,
    limit: int | None = 5,
    strategy: str | None = 'pgvector',
    similarityMetric: str | None = 'cosine_similarity'
) -> RecommenderResponseBody:
    if not playlistId and not soundId:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if not strategy in ('pgvector', 'memory'):
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if not similarityMetric in ('cosine_similarity', 'euclidian_distance'):
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    (sound_ids, openai_embedding) = get_sound_ids_and_embedding(playlistId, soundId)
    if not sound_ids or openai_embedding is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    if strategy == 'pgvector':
        data = get_pgvector_similar(openai_embedding, sound_ids, limit, similarityMetric)
    elif strategy == 'memory':
        data = get_all_similar(openai_embedding, sound_ids, limit, similarityMetric)
        print(data)
    else:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return { 'data': data }
