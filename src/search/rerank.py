from typing import List

import numpy as np
from prefect import task
from sklearn.metrics.pairwise import cosine_similarity

from src.__infra__.logger import logger
from src.model import Passage


@task
def rerank_passages(query_embedding: List[float], passages: List[Passage], threshold: float = 0.7) -> List[Passage]:
    logger.info("Rerank Passages")
    query_embedding_np = np.array(query_embedding).reshape(1, -1)

    similarities = []
    logger.info("Rerank Passages - Compute cosine similarity score")
    for passage in passages:
        passage_embedding_np = np.array(passage.embedding).reshape(1, -1)
        similarity = cosine_similarity(query_embedding_np, passage_embedding_np)[0][0]
        if similarity > threshold:
            passage.score = similarity  # Set the score attribute
            logger.info(f"passage_id: {passage.passage_id} passage_score: {passage.score}")
            similarities.append((passage, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)

    return [passage for passage, _ in similarities]
