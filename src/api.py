from typing import Optional, Any

from fastapi import Body, APIRouter
from fastapi import Query

from src.human_feedback import human_feedback
from src.ingestion.ingest import ingest_pipeline
from src.model import Passage, PassageResponse, SearchFeedbackInput, ConnectorType, SearchStrategyType
from src.search.search import search_pipeline

api = APIRouter(prefix="/api/v1")


@api.post("/ingest", tags=["Semantic Search"])
def ingest_endpoint(
        connector_type: ConnectorType,
        config: dict = Body(default={
            "dataset_path": "microsoft/ms_marco",
            "dataset_name": "v1.1",
            "split": "train",
            "max_size": 100,
            "chunk_size": 100,
        })
) -> dict[str, Any]:
    ingest_pipeline(connector_type=connector_type, config=config)
    return {
        "message": "Documents ingested successfully"
    }


@api.get("/search", tags=["Semantic Search"])
async def search_endpoint(
        strategy_type: SearchStrategyType = SearchStrategyType.HYBRID_SEARCH,
        query: str = Query(default="what is rba", description="MS MARCO Dataset: https://huggingface.co/datasets/microsoft/ms_marco/viewer/v1.1/train"),
        max_results: int = 5,
        evaluate: Optional[bool] = True,
) -> dict[str, Any]:
    search_results = search_pipeline(strategy_type, query, max_results, evaluate)
    return {
        "results": [to_passage_response(p) for p in search_results["results"]],
        "total_results": search_results["total_results"],
        "evaluation": search_results["evaluation"],
    }


@api.post("/human-feedback", tags=["Semantic Search"])
def human_feedback_endpoint(
        feedback: SearchFeedbackInput = Body(default={
            "query": "what is rba",
            "strategy_type": "HYBRID_SEARCH",
            "feedbacks": [
                {
                    "passage_id": "08f4ab9c5b751129183ac513a45583fb",
                    "is_relevant": True,
                },
                {
                    "passage_id": "3fd37024da2ced6be6c5bfb02ff723be",
                    "is_relevant": True,
                },
                {
                    "passage_id": "de935c050a5abd6853e4c64a17cdf502",
                    "is_relevant": False,
                }
            ],
        })
) -> dict[str, Any]:
    human_feedback(feedback)
    return {
        "message": "Thank you for taking the time to provide your feedback! "
                   "Your insights are invaluable to us and help us improve our services. "
                   "We appreciate your contribution!"
    }


def to_passage_response(passage: Passage) -> PassageResponse:
    data = passage.model_dump()
    data.pop("embedding")
    return PassageResponse(**data)
