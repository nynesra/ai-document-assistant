from src.retriever import search


EVALUATION_QUERIES = [
    {
        "query": "Sanal ortam nasıl oluşturulur?",
        "expected_source": "sanal_ortam.md",
    },
    {
        "query": "Python nasıl kurulur?",
        "expected_source": "python_kurulumu.md",
    },
    {
        "query": "FastAPI nedir?",
        "expected_source": "fastapi_kullanimi.md",
    },
    {
        "query": "Git deposu nasıl oluşturulur?",
        "expected_source": "git_komutlari.md",
    },
    {
        "query": "Loglama neden kullanılır?",
        "expected_source": "loglama.md",
    },
]


def main() -> None:
    successful_queries = 0

    print(
        "\n--- 7. GÜN RETRIEVAL ÖN DEĞERLENDİRME ---\n"
    )

    for item in EVALUATION_QUERIES:
        query = item["query"]
        expected_source = item["expected_source"]

        results = search(
            query=query,
            top_k=3,
        )

        first_result = results[0]

        actual_source = first_result["source"]
        score = first_result["score"]

        is_correct = (
            actual_source == expected_source
        )

        if is_correct:
            successful_queries += 1
            status = "BAŞARILI"

        else:
            status = "BAŞARISIZ"

        print(
            f"Sorgu: {query}"
        )

        print(
            f"Beklenen kaynak: {expected_source}"
        )

        print(
            f"Bulunan kaynak: {actual_source}"
        )

        print(
            f"Benzerlik skoru: {score:.4f}"
        )

        print(
            f"Sonuç: {status}"
        )

        print(
            "-" * 50
        )

    total_queries = len(
        EVALUATION_QUERIES
    )

    accuracy = (
        successful_queries
        / total_queries
    ) * 100

    print(
        f"\nToplam sorgu: {total_queries}"
    )

    print(
        f"Doğru Top-1 kaynak: "
        f"{successful_queries}"
    )

    print(
        f"Top-1 kaynak başarı oranı: "
        f"%{accuracy:.2f}"
    )


if __name__ == "__main__":
    main()