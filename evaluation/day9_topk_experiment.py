from src.retriever import (
    build_tfidf_index,
    search_with_index,
)


TEST_CASES = [
    (
        "Sanal ortam nasıl oluşturulur?",
        "sanal_ortam.md",
    ),
    (
        "Python nasıl kurulur?",
        "python_kurulumu.md",
    ),
    (
        "FastAPI nedir?",
        "fastapi_kullanimi.md",
    ),
    (
        "Git deposu nasıl oluşturulur?",
        "git_komutlari.md",
    ),
    (
        "Loglama neden kullanılır?",
        "loglama.md",
    ),
]


TOP_K_VALUES = [
    1,
    3,
    5,
]


def main() -> None:
    chunks, vectorizer, tfidf_matrix = (
        build_tfidf_index(
            chunk_size=500,
            overlap=100,
        )
    )

    print(
        "\n--- 9. GÜN TOP-K DENEYİ ---"
    )

    print(
        "Chunk size: 500"
    )

    print(
        "Overlap: 100"
    )

    print(
        "Toplam chunk:",
        len(chunks),
    )

    for top_k in TOP_K_VALUES:

        total_relevant = 0
        total_returned = 0

        print(
            "\n"
            + "=" * 70
        )

        print(
            "TOP-K:",
            top_k,
        )

        print(
            "=" * 70
        )

        for query, expected_source in TEST_CASES:

            results = search_with_index(
                query=query,
                chunks=chunks,
                vectorizer=vectorizer,
                tfidf_matrix=tfidf_matrix,
                top_k=top_k,
            )

            relevant_count = sum(
                1
                for result in results
                if result["source"]
                == expected_source
            )

            precision_at_k = (
                relevant_count
                / len(results)
            )

            total_relevant += (
                relevant_count
            )

            total_returned += (
                len(results)
            )

            print(
                "\nSorgu:",
                query,
            )

            print(
                "Beklenen kaynak:",
                expected_source,
            )

            print(
                "İlgili sonuç:",
                f"{relevant_count}/{len(results)}",
            )

            print(
                f"Precision@{top_k}:",
                f"{precision_at_k:.4f}",
            )

            for rank, result in enumerate(
                results,
                start=1,
            ):
                print(
                    f"  {rank}. "
                    f"{result['source']} | "
                    f"Skor: "
                    f"{result['score']:.4f}"
                )

        overall_precision = (
            total_relevant
            / total_returned
        )

        print(
            "\nGENEL SONUÇ"
        )

        print(
            "Toplam ilgili sonuç:",
            f"{total_relevant}/{total_returned}",
        )

        print(
            f"Genel Precision@{top_k}:",
            f"{overall_precision:.4f}",
        )


if __name__ == "__main__":
    main()