from typing import List

from dotenv import load_dotenv
from prefect import task

from src.__infra__.env import get_env
from src.__infra__.logger import logger
from src.ingestion.embedding import generate_embedding
from src.model import Passage
from src.query_expansion import expand_query
from src.search.rerank import rerank_passages
from src.search.search_strategy.abstract_search_strategy  import SearchStrategy, keyword_search

load_dotenv()
threshold = float(get_env("SIMILARITY_THRESHOLD"))


class HybridSearch(SearchStrategy):
    @task
    def search(self, query: str, max_results: int) -> List[Passage]:
        logger.info(f"Hybrid Search: {query}")
        expanded_query = expand_query(query)
        passages = keyword_search(expanded_query, max_results)
        query_embedding = generate_query_embedding(expanded_query)
        return rerank_passages(query_embedding, passages, threshold)


@task
def generate_query_embedding(query: str) -> List[float]:
    logger.info(f"Generate Query Embedding: {query}")
    return generate_embedding(query)
