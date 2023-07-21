import pinecone
import os 
from typing import List
import numpy as np


api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_API_ENV")
index_name = os.getenv("PINECONE_INDEX_NAME")

pinecone.init(api_key=api_key, environment=environment)

hasIndex = pinecone.list_indexes()
if not hasIndex:
    pinecone.create_index(index_name, dimension=768, metric="cosine", pod_type="p1")
elif hasIndex[0] != index_name:
    pinecone.delete_index(hasIndex[0])
    pinecone.create_index(index_name, dimension=768, metric="cosine", pod_type="p1")

index = pinecone.Index(index_name)


def format_vectors(vectors: List[np.ndarray], split_text: List[str], doc_title: str):
    formatted_vectors = []    
    for [i,vector] in enumerate(vectors):
        formatted_vectors.append((f'{i}-{doc_title}', vector, {"doc_title": doc_title, "text": split_text[i]}))
    return formatted_vectors

def upsert_vectors(vectors: List[np.ndarray], split_text: List[str], doc_title: str) -> bool:
    formatted_vectors = format_vectors(vectors, split_text, doc_title)
    upsert_response = index.upsert(
        vectors=formatted_vectors,
        namespace=os.getenv("PINECONE_DOCS_NAMESPACE")
    )
    return upsert_response.status_code == 200
