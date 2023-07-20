from fastapi import APIRouter, File, UploadFile
import textract
import os

from helper_functions.save_file_to_disk import save_file_to_disk

router = APIRouter()


#create a fastapi route that accepts a file of any type and then uses the textrace python package to parese it for text
@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        file_path = save_file_to_disk(file)
        text = textract.process(file_path)
        decoded_text = text.decode("utf-8")
        os.remove(file_path)  # Clean up the temporary file
        print(decoded_text)  # Print the parsed text to the console
        
        return {"message": f"Successfully Processed the file {file.filename}"}
    except Exception as e:
        return {"error": str(e)}