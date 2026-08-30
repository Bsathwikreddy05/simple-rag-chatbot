import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


documents = []
vectorizer = None
document_vectors = None


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

    print(f"Stored {len(documents)} chunks using local TF-IDF.")


def search_documents(query, top_k=3):
    global documents, vectorizer, document_vectors

    if not documents or document_vectors is None:
        return []

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append(documents[index])

    print("Search similarities:", similarities[top_indices])

    return results