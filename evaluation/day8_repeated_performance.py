from statistics import mean#pythonun ortalama hesaplamasını sağlayan fonksiyondur
from time import perf_counter

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

REPEAT_COUNT = 10#döngü 10 kez çalışır


def measure_old_method() -> float:
    """Eski yöntemin bir çalıştırmadaki süresini ölçer."""

    start_time = perf_counter()

    for query in QUERIES:
        search(
            query=query,
            top_k=3,
        )

    end_time = perf_counter()

    return end_time - start_time


def measure_reusable_method() -> float:
    """Hazır indeks yönteminin bir çalıştırmadaki süresini ölçer."""

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

    return end_time - start_time


def main() -> None:
    old_times = []
    reusable_times = []

    for _ in range(REPEAT_COUNT):
        old_times.append(
            measure_old_method()
        )

        reusable_times.append(
            measure_reusable_method()
        )

    average_old_time = mean(
        old_times
    )

    average_reusable_time = mean(
        reusable_times
    )

    speedup = (
        average_old_time
        / average_reusable_time
    )

    print(
        "\n--- 8. GÜN TEKRARLI PERFORMANS ANALİZİ ---\n"
    )

    print(
        "Tekrar sayısı:",
        REPEAT_COUNT,
    )

    print(
        "Sorgu sayısı:",
        len(QUERIES),
    )

    print(
        "Eski yöntem ortalama süresi:",
        f"{average_old_time:.6f} saniye",
    )

    print(
        "Hazır indeks ortalama süresi:",
        f"{average_reusable_time:.6f} saniye",
    )

    print(
        "Ortalama hızlanma katsayısı:",
        f"{speedup:.2f}x",
    )


if __name__ == "__main__":
    main()