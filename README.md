# 💬 Chatify — RAG-Based AI Assistant

A full-stack AI application that allows users to upload a PDF document and ask questions about its contents using semantic search and Large Language Models (LLMs).

Instead of sending the entire document to the LLM, the application extracts the PDF text, divides it into smaller chunks, generates vector embeddings, retrieves the most relevant sections using cosine similarity, and provides only the relevant context to the LLM for answer generation.

This project demonstrates the fundamental concepts behind Retrieval-Augmented Generation (RAG)

---

## ✨ Features

* 📄 Upload and process PDF documents
* ✂️ Split large documents into overlapping text chunks
* 🧠 Generate semantic embeddings for document chunks
* 🔍 Retrieve relevant information using cosine similarity
* 💬 Ask natural-language questions about the uploaded PDF
* 🤖 Generate contextual answers using an LLM
* 🎯 Ground responses using retrieved document content
* ⚡ FastAPI-based backend
* ⚛️ React + Vite frontend
* ⏳ PDF processing/loading indicator
* 🔐 Secure API-key management using environment variables

---

#ScreenShots


## 🧠 How It Works

The application follows a basic Retrieval-Augmented Generation workflow:

```text
                    PDF Upload
                        │
                        ▼
                 Extract PDF Text
                        │
                        ▼
                  Split into Chunks
                        │
                        ▼
               Generate Embeddings
                        │
                        ▼
                 Store in Memory
                        │
                        │
User Question ──────────┘
      │
      ▼
Generate Query Embedding
      │
      ▼
Cosine Similarity Search
      │
      ▼
Retrieve Top Relevant Chunks
      │
      ▼
Combine Chunks into Context
      │
      ▼
      LLM
      │
      ▼
Context-Aware Answer
```
---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* JavaScript
* HTML
* CSS

### Backend
* Python
* FastAPI
* Pydantic
* PyPDF
* NumPy
* Sentence Transformers
* Groq API

### AI / RAG

* Sentence Transformers for embeddings
* `all-MiniLM-L6-v2` embedding model
* Cosine similarity for semantic retrieval
* Groq-hosted LLM for answer generation

---

## 📂 Project Structure

```text
Day3-Chat_With_PDF/
│
├── backend/
│   ├── main.py
│   ├── pdf_utils.py
│   ├── rag.py
│   ├── llm.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── eslint.config.js
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

---

## 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Configure the Groq API Key

Create a `.env` file inside the `backend` directory:

```text
backend/.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Never commit your actual `.env` file or API key to GitHub.

---

## 4. Start the Backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 5. Frontend Setup

Open another terminal and navigate to:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The application will normally be available at:

```text
http://localhost:5173
```

---

# 🚀 Usage

1. Start the FastAPI backend.
2. Start the React frontend.
3. Open the frontend in your browser.
4. Select a text-based PDF document.
5. Click Upload PDF.
6. Wait for the document to be processed.
7. Enter a question related to the uploaded document.
8. Click Ask.
9. The application retrieves relevant PDF sections and generates an answer based on that context.

---

# 🔍 RAG Pipeline

## 1. PDF Text Extraction

The uploaded PDF is processed using PyPDF.

```text
PDF
 ↓
Pages
 ↓
Extracted Text
```

---

## 2. Chunking

Large PDF text is divided into smaller overlapping chunks.

For example:

```text
Chunk 1 → characters 0–1000
Chunk 2 → characters 800–1800
Chunk 3 → characters 1600–2600
```

The overlap helps preserve context when important information occurs near chunk boundaries.

---

## 3. Embeddings

Each chunk is converted into a numerical embedding using:

```text
all-MiniLM-L6-v2
```

Conceptually:

```text
"Machine learning allows computers to learn from data."

                    ↓

              Embedding Model

                    ↓

[0.12, -0.37, 0.68, 0.21, ...]
```

These vectors allow the application to compare text based on semantic meaning rather than relying only on exact keyword matches.

---

## 4. Semantic Search

When a user asks a question, the question is converted into an embedding using the same model.

The query embedding is compared against the stored document embeddings using **cosine similarity**.

```text
Question Embedding
       │
       ├── Chunk 1 → 0.31
       ├── Chunk 2 → 0.82  ← Relevant
       ├── Chunk 3 → 0.67  ← Relevant
       └── Chunk 4 → 0.19
```

The highest-scoring chunks are selected.

---

## 5. Context Augmentation

The retrieved chunks are combined:

```text
Relevant Chunk 1

Relevant Chunk 2

Relevant Chunk 3
```

This becomes the context provided to the LLM.

---

## 6. LLM Answer Generation

The application sends:

```text
Retrieved PDF Context
        +
User Question
        ↓
       LLM
        ↓
Generated Answer
```

The prompt instructs the model to answer using the retrieved document context and indicate when the requested information cannot be found in the document.

---

# 🔌 API Endpoints

## `POST /upload`

Uploads and processes a PDF document.

The backend:

* extracts the PDF text,
* creates overlapping chunks,
* generates embeddings,
* and temporarily stores the processed document data.

Example response:

```json
{
  "message": "PDF processed successfully",
  "filename": "document.pdf",
  "total_chunks": 25
}
```

---

## `POST /chat`

Accepts a question about the uploaded PDF.

Example request:

```json
{
  "question": "What is supervised learning?"
}
```

The backend:

1. Generates an embedding for the question.
2. Compares it with document embeddings.
3. Retrieves the most relevant chunks.
4. Creates the LLM context.
5. Generates an answer.

Example response:

```json
{
  "question": "What is supervised learning?",
  "answer": "According to the document, supervised learning is..."
}
```

---

# 📚 Key Concepts Demonstrated

This project provides hands-on implementation of:

* Retrieval-Augmented Generation (RAG)
* PDF text extraction
* Text chunking
* Chunk overlap
* Text embeddings
* Vector representations
* Semantic search
* Cosine similarity
* Top-K retrieval
* Context augmentation
* Prompt grounding
* LLM API integration
* REST API development
* React–FastAPI communication
* Environment variable management

---

# ⚠️ Current Limitations

This project intentionally keeps the RAG implementation simple for learning purposes.

Current limitations include:

* Only one PDF is handled at a time.
* Embeddings are stored temporarily in application memory.
* Data is lost when the backend restarts.
* No persistent vector database is used.
* No user authentication or sessions are implemented.
* Retrieval uses a simple cosine-similarity implementation.
* Scanned/image-only PDFs may not work because OCR is not implemented.

These limitations can be addressed in a production-oriented version using persistent vector databases, metadata filtering, document management, authentication, and more advanced retrieval techniques.

---

# 🔮 Future Improvements

Potential improvements include:

* Vector database integration
* Multiple PDF support
* Persistent document storage
* Conversation history
* Source/page citations
* Streaming LLM responses
* Drag-and-drop PDF upload
* OCR support for scanned documents
* Advanced chunking strategies
* Hybrid search
* Reranking
* User authentication
* Docker containerization
* Cloud deployment

---

# 🎯 Learning Outcome

The main objective of this project was to understand what happens inside a basic RAG application rather than relying entirely on high-level frameworks.

The project manually implements the core pipeline:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
Semantic Retrieval
 ↓
Context Augmentation
 ↓
LLM Generation
```

Building these components individually provides a stronger understanding of how production RAG frameworks and vector databases fit together.

---

## ⭐ Acknowledgements

Built as part of a hands-on learning journey focused on developing modern AI applications using LLMs, embeddings, retrieval systems, backend APIs, and frontend technologies.
