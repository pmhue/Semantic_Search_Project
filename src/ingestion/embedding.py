from prefect import task
from sentence_transformers import SentenceTransformer

@task
def generate_embeddings(passages):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(passages)
    return embeddings