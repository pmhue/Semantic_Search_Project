from datetime import datetime
from enum import Enum
from typing import List, Optional

from src.__infra__.base_model import BaseModel


class ConnectorType(Enum):
    HUGGINGFACE_DATASET = "HUGGINGFACE_DATASET"
    FILE = "FILE"
    SQL = "SQL"
    URL = "URL"


class SearchStrategyType(Enum):
    HYBRID_SEARCH = "HYBRID_SEARCH"
    FALLBACK_MECHANISM = "FALLBACK_MECHANISM"
    TIERED_SEARCH = "TIERED_SEARCH"


class Document(BaseModel):
    doc_id: str
    content: str
    created_at: datetime
    updated_at: datetime
    effective_at: datetime
    expired_at: datetime


class Passage(BaseModel):
    doc_id: str
    passage_id: str
    content: str
    embedding: List[float]
    created_at: datetime
    updated_at: datetime
    effective_at: datetime
    expired_at: datetime


class PassageResponse(BaseModel):
    doc_id: str
    passage_id: str
    content: str
    score: Optional[float]
    created_at: datetime
    updated_at: datetime
    effective_at: datetime
    expired_at: datetime


class SearchResultFeedback(BaseModel):
    passage_id: str
    is_relevant: bool


class SearchFeedbackInput(BaseModel):
    query: str
    strategy_type: SearchStrategyType
    feedbacks: List[SearchResultFeedback]
