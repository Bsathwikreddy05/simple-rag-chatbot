import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_splitter import split_text

documents = []
vectorizer = None
document_vectors = None

def init_knowledge_base(file_path="company_policy.txt"):
    """Automatically loads and indexes the document if not already loaded."""
    global documents, vectorizer, document_vectors
    if documents and document_vectors is not None:
        return

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        chunks = split_text(content)
        add_documents(chunks)
        print(f"Loaded and indexed {len(chunks)} chunks from {file_path}")
    else:
        print(f"Warning: {file_path} not found.")

def add_documents(chunks):
    global documents, vectorizer, document_vectors
    documents = chunks

    if not documents:
        document_vectors = None
        return

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        max_features=10000
    )
    document_vectors = vectorizer.fit_transform(documents)

def search_documents(query, top_k=3):
    global documents, vectorizer, document_vectors

    # Ensure document is loaded
    if not documents or document_vectors is None:
        init_knowledge_base()

    if not documents or document_vectors is None:
        return []

    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, document_vectors)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = [documents[i] for i in top_indices]
    return results

# Auto-initialize on import
init_knowledge_base()