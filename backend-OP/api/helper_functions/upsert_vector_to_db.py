import pinecone
import os 
from typing import List

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_API_ENV")
index_name = os.getenv("PINECONE_INDEX_NAME")
vector_dimensionality = int(os.getenv("PINECONE_VECTOR_DIMENSIONALITY"))

pinecone.init(api_key=api_key, environment=environment)

hasIndex = pinecone.list_indexes()
if not hasIndex:
    pinecone.create_index(index_name, dimension=vector_dimensionality, metric="cosine", pod_type="p1")
elif hasIndex[0] != index_name:
    pinecone.delete_index(hasIndex[0])
    pinecone.create_index(index_name, dimension=vector_dimensionality, metric="cosine", pod_type="p1")

index = pinecone.Index(index_name)


def format_vectors(vectors: List[List[float]], split_text: List[str], doc_title: str, batch_size: int)-> List[List]:
    formatted_vectors = []
    current_batch = []
    
    for i, vector in enumerate(vectors):
        formatted_vector = (f'{i}-{doc_title}', vector, {"doc_title": doc_title, "text": split_text[i]})
        current_batch.append(formatted_vector)

        if len(current_batch) == batch_size:
            formatted_vectors.append(current_batch)
            current_batch = []

    # Add any remaining vectors to the last batch
    if current_batch:
        formatted_vectors.append(current_batch)

    return formatted_vectors

def upsert_vectors(vectors: List[List[float]], split_text: List[str], doc_title: str) -> bool:
    formatted_vectors_batches = format_vectors(vectors, split_text, doc_title, 100)
    success = True

    for batch_vectors in formatted_vectors_batches:
        upsert_response = index.upsert(
            vectors=batch_vectors,
            namespace=os.getenv("PINECONE_DOCS_NAMESPACE")
        )
        if not upsert_response.upserted_count > 0:
            print(f"Error in batch: {upsert_response}")
            success = False
    return success


if __name__ == "__main__":
    #example usage
    print(upsert_vectors([[1,2,3]], ["test"], "test"))