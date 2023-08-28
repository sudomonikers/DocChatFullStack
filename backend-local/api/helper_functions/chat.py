from typing import List, Dict
import os 
from qdrant_client import models, QdrantClient
import boto3
import json 

vector_db_endpoint = os.getenv("QDRANT_ENDPOINT")
qdrant_port = os.getenv("QDRANT_PORT")
index_name = os.getenv("QDRANT_INDEX_NAME")
model_endpoint = os.getenv("MODEL_ENDPOINT")

runtime= boto3.client('runtime.sagemaker')
client = QdrantClient(url=vector_db_endpoint, port=qdrant_port)

# system message to 'prime' the model
primer = f"""You are Q&A bot. A highly intelligent system that answers
user questions based on the information provided by the user above
each question. If the information can not be found in the information
provided by the user you truthfully say "I don't know".
"""

def chat_over_docs(query: str, document: str, history: List[Dict[str, str]] = []) -> List[Dict[str, str]]:
    if len(history) == 0:
        history.append({"role": "system", "content": primer})
        
    query_vector = get_embeddings([query])[0]
    similar_vectors = client.search(
        collection_name=index_name, 
        query_vector=query_vector, 
        limit=3, 
        query_filter=models.Filter(**{"must": [{"key": "doc_title", "match": {"value": document}}]})
    )
    
    contexts = [item.payload['text'] for item in similar_vectors]
    augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\nUser Query: "+query
    history.append({"role": "user", "content": augmented_query})
    
    model_params = {"inputs": history, "parameters": {"max_new_tokens":256, "top_p":0.9, "temperature":0.6}}
    response = runtime.invoke_endpoint(EndpointName=model_endpoint,
                                       ContentType='application/json',
                                       Body=json.dumps(model_params),
                                       CustomAttributes="accept_eula=true")
    
    history.append({"role": "assistant", "content": response['Body'].read().decode()})
    return history


if __name__ == "__main__":
    from create_embeddings import get_embeddings
    #example usage
    print(chat_over_docs("What is the best way to get a job at OpenAI?"))
else:
    from .create_embeddings import get_embeddings
