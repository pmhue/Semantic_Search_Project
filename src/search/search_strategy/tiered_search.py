from typing import List

from prefect import task

from src.__infra__.logger import logger
from src.ingestion.embedding import generate_embedding
from src.model import Passage
from src.query_expansion import expand_query
from src.search.search_strategy.hybrid_search import generate_query_embedding
from src.search.query_classification.query_classification import classify_query
from src.search.search_strategy.abstract_search_strategy  import SearchStrategy, keyword_search, semantic_search


class TieredSearch(SearchStrategy):
    @task
    def search(self, query: str, max_results: int) -> List[Passage]:
        logger.info(f"Tiered Search: {query}")
        expanded_query = expand_query(query)
        is_simple = classify_query(expanded_query)
        if is_simple:
            return keyword_search(expanded_query, max_results)
        else:
            query_embedding = generate_query_embedding(expanded_query)
            return semantic_search(query_embedding, max_results)


@task
def generate_query_embedding(query: str) -> List[float]:
    logger.info(f"Generate Query Embedding: {query}")
    return generate_embedding(query)
