from typing import List

from prefect import task

from src.__infra__.logger import logger
from src.ingestion.embedding import generate_embedding
from src.model import Passage
from src.query_expansion import expand_query
from src.search.search_strategy.abstract_search_strategy import SearchStrategy, semantic_search, keyword_search


class FallbackMechanism(SearchStrategy):
    @task
    def search(self, query: str, max_results: int) -> List[Passage]:
        logger.info(f"Fallback Mechanism: {query}")
        expanded_query = expand_query(query)
        query_embedding = generate_query_embedding(expanded_query)
        results = semantic_search(query_embedding, max_results)
        if not results:
            return keyword_search(query, max_results)
        return results


@task
def generate_query_embedding(query: str) -> List[float]:
    logger.info(f"Generate Query Embedding: {query}")
    return generate_embedding(query)
