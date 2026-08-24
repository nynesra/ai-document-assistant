import time

from src.retriever import (
    build_tfidf_index,
    search_with_index,
)

from src.embedding_retriever import (
    build_embedding_index,
    search_with_embedding_index,
)


def main():
    print(
        "\n--- 12. GÜN RETRIEVAL PERFORMANS DENEYİ ---"
    )

    queries = [
        "Sanal ortam nasıl oluşturulur?",
        "Python nasıl kurulur?",
        "FastAPI nedir?",
        "Git deposu nasıl oluşturulur?",
        "Loglama neden kullanılır?",
    ]

    # =================================================
    # TF-IDF INDEX SÜRESİ
    # =================================================

    tfidf_start = time.perf_counter()

    (
        tfidf_chunks,
        vectorizer,
        tfidf_matrix,
    ) = build_tfidf_index()

    tfidf_index_time = (
        time.perf_counter()
        - tfidf_start
    )

    # =================================================
    # EMBEDDING INDEX SÜRESİ
    # =================================================

    embedding_start = time.perf_counter()

    (
        embedding_chunks,
        model,
        embeddings,
    ) = build_embedding_index(
        chunk_size=500,
        overlap=100,
    )

    embedding_index_time = (
        time.perf_counter()
        - embedding_start
    )

    # =================================================
    # TF-IDF QUERY SÜRELERİ
    # =================================================

    tfidf_query_times = []

    for query in queries:

        start = time.perf_counter()

        search_with_index(
            query=query,
            chunks=tfidf_chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=3,
            threshold=0.0,
        )

        elapsed = (
            time.perf_counter()
            - start
        )

        tfidf_query_times.append(
            elapsed
        )

    # =================================================
    # EMBEDDING QUERY SÜRELERİ
    # =================================================

    embedding_query_times = []

    for query in queries:

        start = time.perf_counter()

        search_with_embedding_index(
            query=query,
            chunks=embedding_chunks,
            model=model,
            embeddings=embeddings,
            top_k=3,
        )

        elapsed = (
            time.perf_counter()
            - start
        )

        embedding_query_times.append(
            elapsed
        )

    # =================================================
    # ORTALAMALAR
    # =================================================

    tfidf_average = (
        sum(tfidf_query_times)
        / len(tfidf_query_times)
    )

    embedding_average = (
        sum(embedding_query_times)
        / len(embedding_query_times)
    )

    # =================================================
    # SONUÇLAR
    # =================================================

    print(
        "\n--- INDEX OLUŞTURMA SÜRELERİ ---"
    )

    print(
        "TF-IDF:",
        f"{tfidf_index_time:.4f} saniye",
    )

    print(
        "Embedding:",
        f"{embedding_index_time:.4f} saniye",
    )

    print(
        "\n--- ORTALAMA QUERY SÜRELERİ ---"
    )

    print(
        "TF-IDF:",
        f"{tfidf_average:.6f} saniye",
    )

    print(
        "Embedding:",
        f"{embedding_average:.6f} saniye",
    )

    print(
        "\n--- SORGU BAZINDA SÜRELER ---"
    )

    for index, query in enumerate(
        queries
    ):
        print(
            f"\nSorgu: {query}"
        )

        print(
            "TF-IDF:",
            f"{tfidf_query_times[index]:.6f}",
        )

        print(
            "Embedding:",
            f"{embedding_query_times[index]:.6f}",
        )


if __name__ == "__main__":
    main()