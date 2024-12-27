from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Define a Pydantic model for the document to be ingested
class Document(BaseModel):
    id: str
    content: str


# Define a Pydantic model for the search query
class SearchQuery(BaseModel):
    query: str
    top_k: int = 10  # Number of top results to return


# In-memory storage for documents (for demonstration purposes)
documents_db = {}


@app.get("/")
def index():
    return {
        "introduction": "Welcome to Semantic Search",
        "path": {
            "swagger_ui": "/docs"
        }
    }


# Route to ingest documents
@app.post("/ingest", tags=["Semantic Search"])
async def ingest_document(doc: Document):
    # Simulate indexing the document
    documents_db[doc.id] = doc.content
    # Here you would add logic to index the document in your search system
    return {"message": "Document ingested successfully", "document_id": doc.id}


# Route to perform semantic search
@app.post("/search", tags=["Semantic Search"])
async def search_documents(search_query: SearchQuery):
    # Simulate a search operation
    # Here you would add logic to perform a semantic search using your search system
    # For demonstration, we return a mock response
    results = [{"id": doc_id, "content": content} for doc_id, content in documents_db.items() if search_query.query in content]

    # Limit results to top_k
    results = results[:search_query.top_k]

    if not results:
        raise HTTPException(status_code=404, detail="No documents found matching the query")

    return {"query": search_query.query, "results": results}

# To run the FastAPI app, use the command: uvicorn api:app --reload
