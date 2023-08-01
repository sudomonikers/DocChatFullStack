from fastapi import APIRouter, File, UploadFile, HTTPException, Response
import textract
import os
from pydantic import BaseModel
from typing import Optional, List, Dict
from fastapi.responses import JSONResponse

from helper_functions.save_file_to_disk import save_file_to_disk
from helper_functions.create_embeddings import get_openai_embeddings
from helper_functions.upsert_vector_to_db import upsert_vectors, index
from helper_functions.upload_to_s3 import upload_file_to_aws
from helper_functions.get_file_from_s3 import download_file_from_s3
from helper_functions.text_splitter import split_into_overlapping_chunks
from helper_functions.chat import chat_over_docs
from helper_functions.get_all_unique_document_titles import get_unique_document_titles

router = APIRouter()


@router.post("/uploadfile/")
async def create_upload_file(files: List[UploadFile] = File(...)):
    responses = []

    for file in files:
        file_path = save_file_to_disk(file)
        text = textract.process(file_path)
        decoded_text = text.decode("utf-8")
        split_text = split_into_overlapping_chunks(decoded_text)
        embeddings = get_openai_embeddings(split_text)
        upsert_vectors(embeddings, split_text, file.filename)
        upload_file_to_aws(file_path, os.getenv("S3_BUCKET"), file.filename)
        os.remove(file_path)  # Clean up the temporary file
        responses.append({"message": f"Successfully processed the file {file.filename}"})

    return responses


class ChatMessage(BaseModel):
    query: str
    document: str
    history: List[Dict[str, str]] = []
@router.post("/chat")
async def chat(message: ChatMessage) -> List[Dict[str, str]]:
    try:
        updated_conversation = chat_over_docs(query=message.query, document=message.document, history=message.history)
        return JSONResponse(content=updated_conversation)
    except Exception as e:
        print(e)
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
    

@router.get("/all-document-titles")
async def get_all_document_titles() -> List[str]:
    try:
        response = get_unique_document_titles()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    