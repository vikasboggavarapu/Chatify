from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from llm import generate_answer
from pdf_utils import extract_text_from_pdf
from rag import (create_chunks,create_embeddings,search_similar_chunks)
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

stored_chunks = []
stored_embeddings = None

class ChatRequest(BaseModel):
    question : str

@app.get("/")
def home():
    return {"message": "Chatify is running"}


@app.post("/upload")
async def upload_pdf(file : UploadFile = File(...)):

    global stored_chunks, stored_embeddings

    if file.content_type != "application/pdf":
        return {"error" : "Please upload a PDF file"}

    text = extract_text_from_pdf(file.file)

    stored_chunks = create_chunks(text)

    stored_embeddings = create_embeddings(stored_chunks)

    return {
        "message" : "PDF file uploaded successfully",
        "filename"  : file.filename,
        "total_chunks" : len(stored_chunks)
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    if not stored_chunks or stored_embeddings is None:
        return {"error" : "please upload a PDF file first"}

    results = search_similar_chunks(request.question,stored_chunks,stored_embeddings)

    context = "\n\n".join(result["chunk"] for result in results)

    answer = generate_answer(request.question,context)

    return{
        "question" : request.question,
         "answer" : answer
    }

   
