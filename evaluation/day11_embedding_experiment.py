from src.embedding_retriever import (
    build_embedding_index,
    search_with_embedding_index,
)


def main():
    print(
        "\n--- 11. GÜN EMBEDDING RETRIEVAL DENEYİ ---"
    )

    # 10. günden korunan chunk parametreleri
    chunk_size = 500
    overlap = 100
    top_k = 3

    chunks, model, embeddings = build_embedding_index(
        chunk_size=chunk_size,
        overlap=overlap,
    )

    test_queries = [
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

    top1_correct = 0
    hit3_correct = 0

    print(
        "\nChunk Size:",
        chunk_size,
    )

    print(
        "Overlap:",
        overlap,
    )

    print(
        "Top-K:",
        top_k,
    )

    print(
        "Toplam chunk:",
        len(chunks),
    )

    print(
        "Embedding matris boyutu:",
        embeddings.shape,
    )

    for test in test_queries:

        query = test["query"]
        expected_source = test["expected_source"]

        results = search_with_embedding_index(
            query=query,
            chunks=chunks,
            model=model,
            embeddings=embeddings,
            top_k=top_k,
        )

        top1_source = results[0]["source"]

        top1_is_correct = (
            top1_source == expected_source
        )

        if top1_is_correct:
            top1_correct += 1

        top3_sources = [
            result["source"]
            for result in results
        ]

        hit3 = (
            expected_source in top3_sources
        )

        if hit3:
            hit3_correct += 1

        print(
            "\n" + "=" * 65
        )

        print(
            "Sorgu:",
            query,
        )

        print(
            "Beklenen kaynak:",
            expected_source,
        )

        print(
            "Top-1 kaynak:",
            top1_source,
        )

        print(
            "Top-1 durum:",
            "DOĞRU"
            if top1_is_correct
            else "YANLIŞ",
        )

        print(
            "Hit@3:",
            "EVET"
            if hit3
            else "HAYIR",
        )

        print(
            "\nTop-3 sonuç:"
        )

        for rank, result in enumerate(
            results,
            start=1,
        ):
            print(
                f"{rank}. {result['source']} "
                f"| Skor: {result['score']:.4f}"
            )

    total_queries = len(
        test_queries
    )

    top1_accuracy = (
        top1_correct
        / total_queries
    )

    hit3_rate = (
        hit3_correct
        / total_queries
    )

    print(
        "\n" + "=" * 65
    )

    print(
        "--- GENEL SONUÇ ---"
    )

    print(
        "Toplam sorgu:",
        total_queries,
    )

    print(
        "Doğru Top-1:",
        f"{top1_correct}/{total_queries}",
    )

    print(
        "Top-1 başarı oranı:",
        f"%{top1_accuracy * 100:.2f}",
    )

    print(
        "Hit@3:",
        f"{hit3_correct}/{total_queries}",
    )

    print(
        "Hit@3 başarı oranı:",
        f"%{hit3_rate * 100:.2f}",
    )


if __name__ == "__main__":
    main()