from time import perf_counter#yüksek hassasiyetli süre ölçümü yapar

from src.retriever import (
    build_tfidf_index,
    search,
    search_with_index,
)


QUERIES = [
    "Sanal ortam nasıl oluşturulur?",
    "Python nasıl kurulur?",
    "FastAPI nedir?",
    "Git deposu nasıl oluşturulur?",
    "Loglama neden kullanılır?",
]


def measure_old_method() -> float:
    """Her sorguda TF-IDF indeksinin yeniden oluşturulduğu yöntemi ölçer."""

    start_time = perf_counter()

    for query in QUERIES:
        search(
            query=query,
            top_k=3,
        )

    end_time = perf_counter()

    elapsed_time = end_time - start_time

    return elapsed_time


def measure_reusable_index_method() -> float:
    """TF-IDF indeksinin bir kez oluşturulup tekrar kullanıldığı yöntemi ölçer."""

    start_time = perf_counter()

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    for query in QUERIES:
        search_with_index(
            query=query,
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=3,
        )

    end_time = perf_counter()

    elapsed_time = end_time - start_time

    return elapsed_time


def main() -> None:
    old_time = measure_old_method()

    reusable_time = measure_reusable_index_method()

    print(
        "\n--- 8. GÜN RETRIEVAL SÜRE KARŞILAŞTIRMASI ---\n"
    )

    print(
        "Sorgu sayısı:",
        len(QUERIES),
    )

    print(
        "Eski yöntem süresi:",
        f"{old_time:.6f} saniye",
    )

    print(
        "Hazır indeks yöntemi süresi:",
        f"{reusable_time:.6f} saniye",
    )

    if reusable_time > 0:
        speedup = old_time / reusable_time

        print(
            "Hızlanma katsayısı:",
            f"{speedup:.2f}x",
        )


if __name__ == "__main__":
    main()