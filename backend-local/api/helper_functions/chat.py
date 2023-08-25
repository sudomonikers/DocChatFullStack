from typing import List, Dict
import os 


# system message to 'prime' the model
primer = f"""You are Q&A bot. A highly intelligent system that answers
user questions based on the information provided by the user above
each question. If the information can not be found in the information
provided by the user you truthfully say "I don't know".
"""

def chat_over_docs(query: str, document: str, history: List[Dict[str, str]] = []) -> List[Dict[str, str]]:
    
    return history

if __name__ == "__main__":
    from create_embeddings import get_embeddings
    #example usage
    print(chat_over_docs("What is the best way to get a job at OpenAI?"))
else:
    from .create_embeddings import get_embeddings
