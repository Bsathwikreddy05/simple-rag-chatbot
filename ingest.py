from text_splitter import split_text
from vector_store import add_documents

# 1. Read the handbook file
with open("company_policy.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2. Split into semantic chunks
chunks = split_text(text)
print(f"Created {len(chunks)} chunks from handbook.")

# 3. Store into ChromaDB
add_documents(chunks)
print("Successfully loaded handbook into ChromaDB!")