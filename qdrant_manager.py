import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def setup_collection(name, vector_size=384):
    client.recreate_collection(
        collection_name=name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

def upload_to_qdrant(name, chunks, embeddings):
    client.upsert(
        collection_name=name,
        points=[
            {"id": i, "vector": embeddings[i], "payload": {"text": chunks[i]}}
            for i in range(len(chunks))
        ]
    )

def search_chunks(name, query_vector, k=3):
    results = client.search(
        collection_name=name,
        query_vector=query_vector,
        limit=k
    )
    return [res.payload['text'] for res in results]
