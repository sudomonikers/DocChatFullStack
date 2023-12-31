import os
from fastapi import UploadFile

def save_file_to_disk(file: UploadFile) -> str:
    # Create a temporary directory to store the uploaded file
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)

    file_path = os.path.join(temp_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return os.path.abspath(file_path)

if __name__ == "__main__":
    #example usage
    save_file_to_disk(UploadFile("test.pdf"))