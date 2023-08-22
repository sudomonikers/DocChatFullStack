import pinecone
import os 
from typing import List
import numpy

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


def get_unique_document_titles() -> List[str]:
    dummy_vector = numpy.zeros((1, 1536)).tolist()
    response = index.query(vector=dummy_vector, namespace=os.getenv("PINECONE_TITLES_NAMESPACE"), top_k=1000, include_metadata=True)
    filtered_response = get_unique_doc_titles(response)
    return filtered_response


if __name__ == "__main__":
    from get_unique_documents_from_query import get_unique_doc_titles
    #example usage
    print(get_unique_document_titles())
else:
    from .get_unique_documents_from_query import get_unique_doc_titles