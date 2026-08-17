import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
     api_key = os.getenv("GROQ_API_KEY")
)

def generate_answer(query,context):
    prompt = f"""
    You are a helpful assistant that answers questions
    about an uploaded PDF.

    Use only the provided context to answer the question.

    If the answer cannot be found in the context, say:
    "I couldn't find that information in the uploaded document."

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    response = client.chat.completions.create(
         model  = "openai/gpt-oss-120b",
         messages = [{
              "role" : "user",
              "content" : prompt
         }]
    )

    return response.choices[0].message.content