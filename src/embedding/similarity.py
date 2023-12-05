from numpy import dot
from numpy.linalg import norm

def cosine_similarity(embedding1, embedding2) -> float:
    return float(dot(embedding1, embedding2)/(norm(embedding1)*norm(embedding2)))

def euclidian_distance(embedding1, embedding2) -> float:
    return float(norm(embedding1 - embedding2))