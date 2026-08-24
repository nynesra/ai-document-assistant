from src.retriever import (
    build_tfidf_index,
    search_with_index,
)


QUERIES = [
    "Sanal ortam nasıl oluşturulur?",
    "Python nasıl kurulur?",
    "FastAPI nedir?",
    "Git deposu nasıl oluşturulur?",
    "Loglama neden kullanılır?",
]


def main() -> None:
    """Beş sorgunun Top-3 retrieval sonuçlarını inceler."""

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    print(
        "\n--- 8. GÜN TOP-3 RETRIEVAL ANALİZİ ---\n"
    )

    print(
        "Toplam chunk:",
        len(chunks),
    )

    print(
        "TF-IDF matris boyutu:",
        tfidf_matrix.shape,
    )

    for query in QUERIES:
        results = search_with_index(
            query=query,
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=3,
        )

        print(
            "\nSorgu:",
            query,
        )

        for rank, result in enumerate(#her sonuca sıra numarası veriyor.
            results,
            start=1,
        ):
            print(
                f"{rank}. "
                f"{result['source']} | "
                f"{result['section']} | "
                f"Skor: {result['score']:.4f}"
            )

        print(
            "-" * 70
        )


if __name__ == "__main__":
    main()