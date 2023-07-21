from fastapi import APIRouter, File, UploadFile, HTTPException, Response
import textract
import os
from nltk.tokenize import sent_tokenize
from pydantic import BaseModel
from typing import Optional

from helper_functions.save_file_to_disk import save_file_to_disk
from helper_functions.create_embeddings import get_vector_embeddings
from helper_functions.upsert_vector_to_db import upsert_vectors, index
from helper_functions.upload_to_s3 import upload_file_to_aws
from helper_functions.get_file_from_s3 import download_file_from_s3

router = APIRouter()


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        file_path = save_file_to_disk(file)
        text = textract.process(file_path)
        decoded_text = text.decode("utf-8")
        split_text = sent_tokenize(decoded_text)
        split_text = list(map(lambda x: x.replace("\n", " "), split_text))
        
        embeddings = get_vector_embeddings(split_text) 
        upsert_vectors(embeddings, split_text, file.filename)        
        upload_file_to_aws(file_path, os.getenv("S3_BUCKET"), file.filename)
        
        os.remove(file_path)  # Clean up the temporary file
        return {"message": f"Successfully Processed the file {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    
class ChatMessage(BaseModel):
    message: str
    history: str
@router.post("/chat")
async def chat(message: ChatMessage):
    try:
        message_embedding = get_vector_embeddings([message.message])
        query_response = index.query(
            vector=message_embedding[0], 
            top_k=5, 
            include_metadata=True,
            namespace=os.getenv("PINECONE_DOCS_NAMESPACE")
        )
        print(query_response)
        return {"message": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.get("/document/{doc_title}")
async def get_document(doc_title: str) -> Optional[bytes]:
    try: 
        download_file_from_s3(os.getenv("S3_BUCKET"), doc_title, f'temp_files/{doc_title}')
        file_contents = open(f'temp_files/{doc_title}', 'rb').read()
        
        file_extension = os.path.splitext(doc_title)[-1].lower()
        media_type = f"application/{file_extension[1:]}"
        
        response = Response(content=file_contents, media_type=media_type)
        response.headers["Content-Disposition"] = f"attachment; filename={doc_title.split('/')[-1]}"
        
        os.remove(f'temp_files/{doc_title}')  # Clean up the temporary file
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")