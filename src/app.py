from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.__infra__.exception_handler import exception_handler, request_validation_error_handler
from src.__infra__.logger import logger
from src.api import api
from src.evaluation import load_evaluation_dataset
from src.ingestion.embedding import load_embedding_model
from src.search.query_classification.train import train_query_classification, is_trained


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Initializing resources during application startup")
    load_evaluation_dataset()
    load_embedding_model()
    if not is_trained():
        train_query_classification()
    yield
    logger.info("Performing cleanup operations during application shutdown")


app = FastAPI(
    lifespan=lifespan,
    title="Semantic Search",
    description="Semantic Search API v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Exceptions
app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)

# Routers
app.include_router(api)


# Index page
@app.get("/", tags=["Index"])
def index() -> dict[str, Any]:
    return {
        "introduction": "Welcome to Semantic Search",
        "swagger": "/docs",
        "redoc": "/redoc",
    }
