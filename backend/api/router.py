from fastapi import APIRouter, File, UploadFile
import textract
import os
from nltk.tokenize import sent_tokenize

from helper_functions.save_file_to_disk import save_file_to_disk
from helper_functions.create_embeddings import get_vector_embeddings
from helper_functions.upsert_vector_to_db import upsert_vectors

router = APIRouter()


#create a fastapi route that accepts a file of any type and then uses the textrace python package to parese it for text
@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        file_path = save_file_to_disk(file)
        text = textract.process(file_path)
        decoded_text = text.decode("utf-8")
        
        split_text = sent_tokenize(decoded_text)
        split_text = list(map(lambda x: x.replace("\n", " "), split_text))
        
        embeddings = get_vector_embeddings(split_text) 
        try:       
            upsert_vectors(embeddings, file.filename)
        except Exception as e:
            return {"error upserting vectors": str(e)}
        
        os.remove(file_path)  # Clean up the temporary file
        return {"message": f"Successfully Processed the file {file.filename}"}
    except Exception as e:
        return {"error": str(e)}