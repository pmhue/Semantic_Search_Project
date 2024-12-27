from prefect import task, flow

from src.evaluation import evaluate_search
from src.query_expansion import expand_query


@flow
def search_flow():
    query = "example query"
    expanded_query = expand_query(query)
    search_results = hybrid_search(expanded_query)
    evaluation = evaluate_search(search_results, "ground_truth")


@task
def hybrid_search(query):
    # Logic for keyword search using ElasticSearch
    # Logic for semantic search using embeddings
    # Re-ranking logic
    pass
