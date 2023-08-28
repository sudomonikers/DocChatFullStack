from typing import List, Dict
import os 
from qdrant_client import models, QdrantClient
import uuid 

vector_db_endpoint = os.getenv("QDRANT_ENDPOINT")
qdrant_port = os.getenv("QDRANT_PORT")
index_name = os.getenv("QDRANT_TITLES_NAMESPACE")

client = QdrantClient(url=vector_db_endpoint, port=qdrant_port)

def upsert_title(doc_title: str):
    client.upsert(collection_name=index_name, points=[models.PointStruct(id=str(uuid.uuid4()), vector=[0]*384, payload={"doc_title": doc_title})])
    
if __name__ == "__main__":
    #example usage
    upsert_title("test_title")