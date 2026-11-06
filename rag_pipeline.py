import os
import re

from dotenv import load_dotenv
from google import genai

from vector_store import search_documents


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=API_KEY
)


def ask_rag(question, chat_history=None):
    relevant_chunks = search_documents(question, top_k=4)

    if not relevant_chunks:
        return "No policy records or document contents are currently available.", []

    context = "\n\n--- POLICY SECTION ---\n\n".join(relevant_chunks)

    # Format the recent conversation turns (up to the last 4 messages)
    history_text = "None"
    if chat_history:
        formatted = []
        for msg in chat_history[-4:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted.append(f"{role}: {msg['content']}")
        if formatted:
            history_text = "\n".join(formatted)

    prompt = f"""
You are the official Internal HR & Policy Assistant.

Your task is to answer employee inquiries accurately, professionally, and conversationally based strictly on the provided company policy excerpts.

RECENT CONVERSATION HISTORY:
{history_text}

CONTEXT FROM HR HANDBOOK:
{context}

EMPLOYEE QUESTION:
{question}

Response Guidelines:
- Answer the user's question directly in a friendly, professional, and natural tone.
- Do NOT simply copy-paste verbatim sections, markdown headers, or raw chunks. Synthesize the relevant rules into a concise, easily understood explanation.
- Address the employee naturally (e.g., "Under company policy, you can...", "You are allowed to...").
- Include relevant limits, days, deadlines, or conditions that directly apply to their question.
- Use the RECENT CONVERSATION HISTORY to resolve pronouns (e.g., "it", "that", "the policy mentioned") and understand the context of follow-up questions.
- If the handbook does not contain the answer, politely let the employee know and refer them to HR support.
- Do not fabricate rules or policies not found in the provided context.

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    # Extract the primary section title from each retrieved chunk (limit to top 3)
    sources = []
    for chunk in relevant_chunks:
        # Match only full, clean heading lines like "## 2. LEAVE & ATTENDANCE" or "2.3 Carry Forward Rule"
        matches = re.findall(r"(?:^|\n)(?:#+\s*)?(\d+(?:\.\d+)*\s+[A-Za-z\s&/\-\(\)]+)", chunk)
        for m in matches:
            clean_title = m.strip().split("\n")[0].strip()
            # Ignore cut-off fragments and ensure complete words
            if len(clean_title) > 6 and not clean_title.endswith((" Fo", " and", " or")):
                if clean_title not in sources:
                    sources.append(clean_title)
                    break  # Take only the main section per chunk

    # Keep only the top 2-3 most relevant sources
    sources = sources[:3]

    if not sources:
        sources = ["HR Employee Handbook - General Guidelines"]

    return response.text, sources