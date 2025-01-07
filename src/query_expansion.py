from prefect import task

from src.__infra__.logger import logger


@task
def expand_query(query: str) -> str:
    logger.info(f"Expand query: {query}")
    # TODO
    return query
