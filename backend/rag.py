import os
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("HF_TOKEN")

model = SentenceTransformer('all-MiniLM-L6-v2')

#creates chunks
def create_chunks(text,chunk_size = 1000,overlap = 200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks  

#creates embeddings
def create_embeddings(chunks):

    embeddings =  model.encode(chunks)
    return embeddings

def create_query_embedding(query):
    query_embedding  = model.encode(query)
    return query_embedding

#cosine similarity
def cosine_similarity(vector1,vector2):
    dot_product = np.dot(vector1,vector2)

    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)

    similarity = dot_product / (magnitude1 * magnitude2)
    return similarity

