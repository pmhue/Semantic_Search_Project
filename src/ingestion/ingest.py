from prefect import flow
from prefect import task


@flow
def ingest_flow():
    documents = parse_documents("data/raw/documents.txt")
    indexed_docs = index_documents(documents)


@task
def parse_documents(file_path):
    # Logic to parse documents from raw data
    pass


@task
def index_documents(documents):
    # Logic to index documents into ElasticSearch
    pass
