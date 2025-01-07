from threading import Lock
from typing import List, Any, Optional

from datasets import load_dataset
from prefect import task

from src.__infra__.hash import generate_md5_hash
from src.__infra__.logger import logger
from src.model import Passage

dataset = None
dataset_lock = Lock()
top_k = 5


@task
def evaluate_search(results: List[Passage], query: str) -> Optional[dict[str, Any]]:
    ground_truth = get_ground_truth(query)
    if not ground_truth:
        return None
    result_doc_ids = [passage.doc_id for passage in results]
    precision = precision_at_k(ground_truth, result_doc_ids, top_k)
    mrr = mrr_at_k(ground_truth, result_doc_ids, top_k)
    # TODO: store to db
    return {
        f"precision@{top_k}": precision,
        f"mrr@{top_k}": mrr
    }


def get_ground_truth(query: str) -> Optional[List[str]]:
    global dataset
    dataset = load_evaluation_dataset()
    cleaned_query = clean_query(query)
    filtered_dataset = dataset.filter(lambda row: row["query"] == cleaned_query)
    if len(filtered_dataset) == 0:
        return None
    first_row = filtered_dataset[0]
    return [
        generate_md5_hash(content)
        for content in first_row["passages"]["passage_text"]
    ]


def clean_query(query: str) -> str:
    # TODO
    return query


def precision_at_k(ground_truth: List[str], result_doc_id: List[str], k: int) -> float:
    k = min(k, len(result_doc_id))
    if k == 0:
        return 0.0
    top_k_results = result_doc_id[:k]
    relevant_count = sum(1 for doc_id in top_k_results if doc_id in ground_truth)
    precision = relevant_count / k
    return precision


def mrr_at_k(ground_truth: List[str], result_doc_id: List[str], k: int = 10) -> float:
    top_k_results = result_doc_id[:k]
    for rank, doc_id in enumerate(top_k_results, start=1):
        if doc_id in ground_truth:
            return 1.0 / rank
    return 0.0


def load_evaluation_dataset():
    logger.info("Load evaluation dataset")
    global dataset
    if dataset is None:
        with dataset_lock:
            dataset = load_dataset("microsoft/ms_marco", name="v1.1", split="train")
    return dataset
