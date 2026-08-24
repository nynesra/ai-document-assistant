from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.document_loader import load_documents
from src.chunker import chunk_documents


MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


def load_embedding_model():
    """Embedding modelini yükler."""

    model = SentenceTransformer(
        MODEL_NAME
    )

    return model


def create_embedding(
    text: str,
    model,
):
    """Tek bir metni embedding vektörüne dönüştürür."""

    if not text.strip():
        raise ValueError(
            "Embedding oluşturulacak metin boş olamaz."
        )

    embedding = model.encode(
        text
    )

    return embedding


def build_embedding_index(
    chunk_size: int = 500,
    overlap: int = 100,
):
    """Doküman chunkları için embedding indeksi oluşturur."""

    documents = load_documents(
        "data"
    )

    chunks = chunk_documents(
        documents=documents,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    chunk_texts = [
        chunk["text"]
        for chunk in chunks
    ]

    model = load_embedding_model()

    embeddings = model.encode(
        chunk_texts
    )

    return (
        chunks,
        model,
        embeddings,
    )


def search_with_embedding_index(
    query: str,
    chunks,
    model,
    embeddings,
    top_k: int = 3,
):
    """Hazır embedding indeksinde semantik arama yapar."""

    if not query.strip():
        raise ValueError(
            "Arama sorgusu boş bırakılamaz."
        )

    if top_k <= 0:
        raise ValueError(
            "top_k sıfırdan büyük olmalıdır."
        )

    effective_top_k = min(
        top_k,
        len(chunks),
    )

    # Kullanıcı sorgusunu embedding vektörüne çeviriyoruz.
    query_embedding = model.encode(
        query
    )

    # Sorgu ile bütün chunklar arasındaki
    # cosine similarity değerleri hesaplanıyor.
    similarity_scores = cosine_similarity(
        [query_embedding],
        embeddings,
    )[0]

    # Skorları büyükten küçüğe sıralıyoruz.
    ranked_indices = similarity_scores.argsort()[::-1]

    # İlk Top-K sonucu seçiyoruz.
    top_indices = ranked_indices[
        :effective_top_k
    ]

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


def main():
    print(
        "\n--- EMBEDDING RETRIEVAL TESTİ ---"
    )

    chunks, model, embeddings = (
        build_embedding_index()
    )

    print(
        "Toplam chunk sayısı:",
        len(chunks),
    )

    print(
        "Embedding matris boyutu:",
        embeddings.shape,
    )

    queries = [
        "Sanal ortam nasıl oluşturulur?",
        "Python nasıl kurulur?",
        "FastAPI nedir?",
        "Git deposu nasıl oluşturulur?",
        "Loglama neden kullanılır?",
        "Python için sanal ortamı nasıl hazırlayabilirim?",
    ]

    for query in queries:

        results = search_with_embedding_index(
            query=query,
            chunks=chunks,
            model=model,
            embeddings=embeddings,
            top_k=3,
        )

        print(
            "\n" + "=" * 60
        )

        print(
            "Sorgu:",
            query,
        )

        print(
            "Top-3 Embedding Sonuçları:"
        )

        for rank, result in enumerate(
            results,
            start=1,
        ):

            print(
                f"{rank}. {result['source']} "
                f"| Skor: {result['score']:.4f}"
            )


if __name__ == "__main__":
    main()