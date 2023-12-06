from numpy import dot
from numpy.linalg import norm
from functools import reduce

# Measure how aligned two vectors are (i.e. the angle between them).
# The value ranges between 1 (perfectly aligned) and -1
def cosine_similarity(embedding1, embedding2) -> float:
    return float(dot(embedding1, embedding2)/(norm(embedding1)*norm(embedding2)))

def euclidian_distance(embedding1, embedding2) -> float:
    return float(norm(embedding1 - embedding2))

def combine_embeddings(embeddings):
    if not embeddings:
        return None
    # We could preserve the average norm of the embeddings, but the norm does not matter much,
    # at least not for cosine_similarity
    return reduce(lambda a, b: a + b, embeddings)
