from abc import ABC, abstractmethod
from typing import List

from elastic_transport import ObjectApiResponse
from prefect import task

from src.__infra__.elasticsearch import get_elasticsearch_client
from src.__infra__.logger import logger
from src.ingestion.ingest import PASSAGE_INDEX
from src.model import Passage


class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query: str, max_results: int) -> List[Passage]:
        """Perform a search and return a list of Passage objects."""
        pass


@task
def keyword_search(query: str, max_results: int):
    logger.info(f"Keyword Search: {query}")
    es = get_elasticsearch_client()
    response = es.search(
        index=PASSAGE_INDEX,
        size=max_results,
        query={
            "match": {
                "content": {
                    "query": query
                }
            }
        },
    )
    return to_passages(response)


@task
def semantic_search(query_embedding: List[float], max_results: int):
    logger.info(f"Semantic Search: {query_embedding[:10]}...")
    es = get_elasticsearch_client()
    response = es.search(
        index=PASSAGE_INDEX,
        size=max_results,
        query={
            "knn": {
                "field": "embedding",
                "query_vector": query_embedding,
                "k": max_results
            }
        },
    )
    return to_passages(response)


def to_passages(response: ObjectApiResponse) -> List[Passage]:
    passages = []
    for hit in response['hits']['hits']:
        score = hit['_score']
        source = hit['_source']
        passage = Passage(
            doc_id=source.get('doc_id'),
            passage_id=source.get('passage_id'),
            content=source.get('content'),
            embedding=source.get('embedding'),
            created_at=source.get('created_at'),
            updated_at=source.get('updated_at'),
            effective_at=source.get('effective_at'),
            expired_at=source.get('expired_at')
        )
        passage.score = score
        passages.append(passage)
    return passages
