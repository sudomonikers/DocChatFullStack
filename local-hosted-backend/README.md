To start the api in dev mode: uvicorn main:app --reload

Please keep in mind the first time the endpoint to upload a document is hit, it will take much longer because we need to download the embeddings model

to load env vars: cat .env