from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from pdf_utils import extract_text_from_pdf
from rag import create_chunks,create_embeddings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "Chatify is running"}


@app.post("/upload")
async def upload_pdf(file : UploadFile = File(...)):

    if file.content_type != "application/pdf":
        return {"error" : "Please upload a PDF file"}

    text = extract_text_from_pdf(file.file)

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    return {
        "message" : "PDF file uploaded successfully",
        "filename"  : file.filename,
        "characters" : len(text),
        "total_chunks" : len(chunks),
        "total_embeddings": len(embeddings),
        "first_embedding" : embeddings[0].tolist()
    }

   
    