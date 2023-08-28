import os
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition, Range, PointStruct
import uuid

vector_db_endpoint = os.getenv("QDRANT_ENDPOINT")
qdrant_port = os.getenv("QDRANT_PORT")
index_name = os.getenv("QDRANT_INDEX_NAME")

client = QdrantClient(url=vector_db_endpoint, port=qdrant_port)


def upsert_vectors(vectors: List[List[float]], split_text: List[str], doc_title: str) -> bool:
    success = True
    formatted_vectors = get_formatted_vectors(vectors, split_text, doc_title)

    response = client.upsert(
        collection_name=index_name,
        points=formatted_vectors
    )

    if not response.status == 'completed':
        print(f"Error in upsert: {response}")
        success = False
    return success


def get_formatted_vectors(vectors: List[List[float]], split_text: List[str], doc_title: str) -> List[PointStruct]:
    formatted_vectors = []
    for i, vector in enumerate(vectors):
        formatted_vector = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"doc_title": doc_title, "text": split_text[i]}
        )
        formatted_vectors.append(formatted_vector)
    return formatted_vectors

if __name__ == "__main__":
    import numpy as np
    vectors = np.random.rand(1, 384).tolist()
    print(upsert_vectors(vectors, ["test"], "test"))

