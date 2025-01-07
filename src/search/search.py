from typing import Optional

from prefect import flow

from src.evaluation import evaluate_search
from src.model import SearchStrategyType
from src.search.search_strategy.search_strategy_factory import get_search_strategy_map


@flow
def search_pipeline(strategy_type: SearchStrategyType, query: str, max_results: int, evaluate: Optional[bool]):
    search_strategy = get_search_strategy_map().get(strategy_type)

    if not search_strategy:
        raise ValueError(f"Unknown search strategy type: {strategy_type}")

    search_results = search_strategy.search(query, max_results)
    evaluation_task = evaluate_search.submit(search_results, query)

    return {
        "results": search_results,
        "total_results": len(search_results),
        "evaluation": evaluation_task.result() if evaluate else None,
    }
