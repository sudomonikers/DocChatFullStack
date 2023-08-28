from qdrant_client import models, QdrantClient
from typing import List
import boto3
import os
import numpy

vector_db_endpoint = os.getenv("QDRANT_ENDPOINT")
qdrant_port = os.getenv("QDRANT_PORT")
index_name = os.getenv("QDRANT_TITLES_NAMESPACE")
model_endpoint = os.getenv("MODEL_ENDPOINT")

runtime= boto3.client('runtime.sagemaker')
client = QdrantClient(url=vector_db_endpoint, port=qdrant_port)

def get_unique_document_titles() -> List[str]:
    titles = client.search(collection_name=index_name, query_vector=[0]*384, limit=1000)
    title_array = [item.payload['doc_title'] for item in titles]
    return title_array


if __name__ == "__main__":
    #example usage
    print(get_unique_document_titles())