from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from router import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Startup
    print('starting up')
    
    yield
    # Shutdown
    
app = FastAPI(lifespan=lifespan, description="This is an api to upload documents, and then interact with them using a chatbot", version="0.0.1")
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "OK"}

app.include_router(api_router, prefix="", tags=["Auth"])

#lambda handler
handler = Mangum(app)