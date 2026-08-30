import os

from dotenv import load_dotenv
from google import genai

from vector_store import search_documents


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=API_KEY
)


def ask_rag(question):

    relevant_chunks = search_documents(
        question,
        top_k=5
    )

    if not relevant_chunks:
        return "No document content is available."

    context = "\n\n--- DOCUMENT SECTION ---\n\n".join(
        relevant_chunks
    )

    prompt = f"""
You are a helpful document question-answering assistant.

The user has uploaded a PDF document.

Answer the user's question using the document content below.

DOCUMENT CONTENT:
{context}

USER QUESTION:
{question}

Instructions:
- Use the document content to answer.
- Give a clear and useful answer.
- If the question asks what the document is about, summarize its main topic.
- If the question asks for key aspects, list the important points.
- Do not make up information that is not supported by the document.

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text