from typing import List, Dict
import openai 
import os 
import pinecone 

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_API_ENV")
index_name = os.getenv("PINECONE_INDEX_NAME")
vector_dimensionality = int(os.getenv("PINECONE_VECTOR_DIMENSIONALITY"))
namespace = os.getenv("PINECONE_DOCS_NAMESPACE")

openai.api_key = os.getenv('OPENAI_API_KEY')
embed_model = "text-embedding-ada-002"

pinecone.init(api_key=api_key, environment=environment)
hasIndex = pinecone.list_indexes()
if not hasIndex:
    pinecone.create_index(index_name, dimension=vector_dimensionality, metric="cosine", pod_type="p1")
elif hasIndex[0] != index_name:
    pinecone.delete_index(hasIndex[0])
    pinecone.create_index(index_name, dimension=vector_dimensionality, metric="cosine", pod_type="p1")

index = pinecone.Index(index_name)


# system message to 'prime' the model
primer = f"""You are Q&A bot. A highly intelligent system that answers
user questions based on the information provided by the user above
each question. If the information can not be found in the information
provided by the user you truthfully say "I don't know".
"""

def chat_over_docs(query: str, document: str, history: List[Dict[str, str]] = []) -> List[Dict[str, str]]:
    if len(history) == 0:
        history.append({"role": "system", "content": primer})
    #embed the query
    res = get_openai_embeddings(query)

    # get relevant contexts (including the questions)
    res = index.query(
        vector=res[0], 
        filter={"doc_title": document},
        top_k=5, 
        namespace=namespace, 
        include_metadata=True)
    contexts = [item['metadata']['text'] for item in res['matches']]
    augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\nUser Query: "+query
    history.append({"role": "user", "content": augmented_query})
    
    #now we ask openai the question and pass it in chat history and the relevant contexts
    answer = openai.ChatCompletion.create(
        model="gpt-4",
        messages=history
    )
    history.append({"role": "assistant", "content": answer.choices[0].message.content})
    return history

if __name__ == "__main__":
    from create_embeddings import get_openai_embeddings
    #example usage
    print(chat_over_docs("What is the best way to get a job at OpenAI?"))
else:
    from .create_embeddings import get_openai_embeddings
