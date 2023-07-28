from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import os 

model_name = os.getenv("EMBEDDING_MODEL")
model = SentenceTransformer(model_name)

def get_vector_embeddings(sentences: List[str]) -> List[np.ndarray]:
    sentence_embeddings = model.encode(sentences).tolist()
    return sentence_embeddings
