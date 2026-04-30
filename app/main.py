from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os

from app.ingestion import load_and_split_documents
from app.retriever import create_vector_store, clear_vector_store_cache
from app.rag_pipeline import get_rag_response
from app.config import DATA_PATH, VECTOR_DB_PATH

app = FastAPI()

os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(VECTOR_DB_PATH, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(file.filename)
    if not safe_filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    file_path = os.path.join(DATA_PATH, safe_filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    docs = load_and_split_documents(DATA_PATH)
    create_vector_store(docs)
    clear_vector_store_cache()

    return {"message": "File processed successfully"}

class Message(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    question: str
    chat_history: Optional[List[Message]] = []


@app.post("/query")
def query(request: QueryRequest):
    try:
        response = get_rag_response(request.question, request.chat_history)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"answer": response}
