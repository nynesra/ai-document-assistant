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


CHUNK_SIZES = [
    300,
    500,
    700,
]


def main() -> None:
    for chunk_size in CHUNK_SIZES:

        chunks, vectorizer, tfidf_matrix = (
            build_tfidf_index(
                chunk_size=chunk_size,
                overlap=100,
            )
        )

        correct_count = 0

        print(
            "\n"
            + "=" * 70
        )

        print(
            "CHUNK SIZE:",
            chunk_size,
        )

        print(
            "Chunk sayısı:",
            len(chunks),
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
                top_k=1,
            )

            first_result = results[0]

            predicted_source = (
                first_result["source"]
            )

            score = (
                first_result["score"]
            )

            is_correct = (
                predicted_source
                == expected_source
            )

            if is_correct:
                correct_count += 1

            print(
                "\nSorgu:",
                query,
            )

            print(
                "Beklenen:",
                expected_source,
            )

            print(
                "Bulunan:",
                predicted_source,
            )

            print(
                "Skor:",
                f"{score:.4f}",
            )

            print(
                "Durum:",
                "DOĞRU"
                if is_correct
                else "YANLIŞ",
            )

        accuracy = (
            correct_count
            / len(TEST_CASES)
            * 100
        )

        print(
            "\nDoğru sonuç:",
            f"{correct_count}/{len(TEST_CASES)}",
        )

        print(
            "Top-1 başarı oranı:",
            f"%{accuracy:.2f}",
        )


if __name__ == "__main__":
    main()