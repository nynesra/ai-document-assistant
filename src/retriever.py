from sklearn.feature_extraction.text import TfidfVectorizer#scikit-learn içinden TF-IDF işlemlerini yapan sınıfı alıyoruz.
from sklearn.metrics.pairwise import cosine_similarity

from src.document_loader import load_documents
from src.chunker import chunk_documents


def build_tfidf_index():
    """Bilgi tabanındaki chunklar için TF-IDF indeksi oluşturur."""

    documents = load_documents("data")

    chunks = chunk_documents(
        documents=documents,
        chunk_size=500,
        overlap=100,
    )

    chunk_texts = [#TfidVectorizer metadata istemediği için her chunkın sadece text kısmını alıyıoruz.
        chunk["text"]
        for chunk in chunks
    ]

    vectorizer = TfidfVectorizer(
        lowercase=True,
    )

    tfidf_matrix = vectorizer.fit_transform(#matrisi oluşturuyoruz.satır sayısı chunk sayısına eşit.
        chunk_texts
    )

    return chunks, vectorizer, tfidf_matrix

def search_with_index(
    query: str,
    chunks,
    vectorizer,
    tfidf_matrix,
    top_k: int = 3,
    threshold: float = 0.0,
):
    """Hazır TF-IDF indeksini kullanarak arama yapar."""

    if not query.strip():
        raise ValueError(
            "Arama sorgusu boş bırakılamaz."
        )

    if top_k <= 0:
        raise ValueError(
            "top_k sıfırdan büyük olmalıdır."
        )

    if threshold < 0 or threshold > 1:
        raise ValueError(
            "threshold 0 ile 1 arasında olmalıdır."
        )

    effective_top_k = min(
        top_k,
        len(chunks),
    )

    query_vector = vectorizer.transform(
        [query]
    )

    similarity_scores = cosine_similarity(
        query_vector,
        tfidf_matrix,
    )[0]

    ranked_indices = similarity_scores.argsort()[::-1]

    top_indices = ranked_indices[:effective_top_k]

    results = []

    for index in top_indices:

        score = float(
            similarity_scores[index]
        )

        # Similarity skoru eşik değerinin altındaysa
        # bu chunk retrieval sonucuna eklenmez.
        if score < threshold:
            continue

        chunk = chunks[index]

        result = {
            "source": chunk["source"],
            "section": chunk["section"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "score": score,
        }

        results.append(result)

    return results

def search(
    query: str,
    top_k: int = 3,
):
    """Kullanıcı sorgusuna en benzer chunkları bulur."""

    if not query.strip():
        raise ValueError(
            "Arama sorgusu boş bırakılamaz."
        )
    
    if top_k <= 0:
        raise ValueError(
            "top_k sıfırdan büyük olmalıdır."
    )

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    query_vector = vectorizer.transform(#Soru vektöre çevriliyor.
        [query]
    )

    similarity_scores = cosine_similarity(
        query_vector,
        tfidf_matrix,
    )[0]

    ranked_indices = similarity_scores.argsort()[::-1]

    top_indices = ranked_indices[:top_k]

    results = []

    for index in top_indices:
        chunk = chunks[index]

        result = {
            "source": chunk["source"],
            "section": chunk["section"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "score": float(
                similarity_scores[index]
            ),
        }

        results.append(result)

    return results

def main() -> None:
    """TF-IDF indeksini bir kez oluşturur ve birden fazla sorgu çalıştırır."""

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    queries = [
        "Sanal ortam nasıl oluşturulur?",
        "Python nasıl kurulur?",
        "FastAPI nedir?",
        "Git deposu nasıl oluşturulur?",
        "Loglama neden kullanılır?",

        "Türkiye'nin başkenti neresidir?",
        "5 + 5 kaçtır?",
        "En hızlı hayvan hangisidir?",
        "Bugün hava nasıl?",
        "Dünya'nın uydusu nedir?",
    ]

    print("\n--- HAZIR TF-IDF İNDEKSİ ---")

    print(
        "Toplam chunk sayısı:",
        len(chunks),
    )

    print(
        "TF-IDF matris boyutu:",
        tfidf_matrix.shape,
    )

    print(
        "Vocabulary boyutu:",
        len(vectorizer.get_feature_names_out()),
    )

    print(
        "\n--- ÇOKLU SORGU SONUÇLARI ---"
    )

    for query in queries:#listedeki soruları tek tek alıyor
        results = search_with_index(
            query=query,
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=3,
        )

        first_result = results[0]

        print(
            "\nSorgu:",
            query,
        )

        print(
            "Top-1 kaynak:",
            first_result["source"],
        )

        print(
            "Bölüm:",
            first_result["section"],
        )

        print(
            "Benzerlik skoru:",
            f"{first_result['score']:.4f}",
        )

if __name__ == "__main__":
    main()