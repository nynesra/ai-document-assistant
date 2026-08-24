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
        "\n--- 11. GÜN PARAPHRASE TF-IDF vs EMBEDDING ---"
    )

    # TF-IDF indeksi
    chunks_tfidf, vectorizer, tfidf_matrix = (
        build_tfidf_index()
    )

    # Embedding indeksi
    chunks_embedding, model, embeddings = (
        build_embedding_index(
            chunk_size=500,
            overlap=100,
        )
    )

    test_queries = [
    {
        "query":
            "Python kurulumu için hangi adımları izlemeliyim?",
        "expected_sources": [
            "python_kurulumu.md",
        ],
    },
    {
        "query":
            "FastAPI ne işe yarar?",
        "expected_sources": [
            "fastapi_kullanimi.md",
        ],
    },
    {
        "query":
            "Git projesi başlatmak için ne yapmalıyım?",
        "expected_sources": [
            "git_komutlari.md",
        ],
    },
    {
        "query":
            "Uygulamada neden log tutulur?",
        "expected_sources": [
            "loglama.md",
        ],
    },
    {
        "query":
            "Python için sanal ortamı nasıl hazırlayabilirim?",
        "expected_sources": [
            "sanal_ortam.md",
            "servis_kurulumu.md",
        ],
    },
]

    tfidf_top1_correct = 0
    embedding_top1_correct = 0

    tfidf_hit3_correct = 0
    embedding_hit3_correct = 0

    for test in test_queries:

        query = test["query"]
        expected_sources = test["expected_sources"]

        # -------------------------
        # TF-IDF
        # -------------------------

        tfidf_results = search_with_index(
            query=query,
            chunks=chunks_tfidf,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=3,
            threshold=0.0,
        )

        # -------------------------
        # EMBEDDING
        # -------------------------

        embedding_results = (
            search_with_embedding_index(
                query=query,
                chunks=chunks_embedding,
                model=model,
                embeddings=embeddings,
                top_k=3,
            )
        )

        tfidf_top1 = (
            tfidf_results[0]["source"]
        )

        embedding_top1 = (
            embedding_results[0]["source"]
        )

        tfidf_top1_ok = (
            tfidf_top1 in expected_sources
        )

        embedding_top1_ok = (
            embedding_top1 in expected_sources
        )

        if not embedding_top1_ok:

            print(
                "\n--- EMBEDDING HATA ANALİZİ ---"
            )

            for rank, result in enumerate(
                embedding_results,
                start=1,
            ):
                print(
                    f"\n{rank}. Kaynak:",
                    result["source"],
                )

                print(
                    "Bölüm:",
                    result["section"],
                )

                print(
                    "Skor:",
                    f"{result['score']:.4f}",
                )

                print(
                    "Chunk metni:"
                )

                print(
                    result["text"][:300]
                )

        if tfidf_top1_ok:
            tfidf_top1_correct += 1

        if embedding_top1_ok:
            embedding_top1_correct += 1

        tfidf_sources = [
            result["source"]
            for result in tfidf_results
        ]

        embedding_sources = [
            result["source"]
            for result in embedding_results
        ]

        tfidf_hit3 = any(
            source in tfidf_sources
            for source in expected_sources
        )

        embedding_hit3 = any(
            source in embedding_sources
            for source in expected_sources
        )

        if tfidf_hit3:
            tfidf_hit3_correct += 1

        if embedding_hit3:
            embedding_hit3_correct += 1

        print(
            "\n" + "=" * 70
        )

        print(
            "Sorgu:",
            query,
        )

        print(
            "Kabul edilebilir kaynaklar:",
            ", ".join(expected_sources),
        )

        print(
            "\nTF-IDF Top-1:",
            tfidf_top1,
        )

        print(
            "TF-IDF Top-1 Durum:",
            "DOĞRU"
            if tfidf_top1_ok
            else "YANLIŞ",
        )

        print(
            "TF-IDF Hit@3:",
            "EVET"
            if tfidf_hit3
            else "HAYIR",
        )

        print(
            "\nEmbedding Top-1:",
            embedding_top1,
        )

        print(
            "Embedding Top-1 Durum:",
            "DOĞRU"
            if embedding_top1_ok
            else "YANLIŞ",
        )

        print(
            "Embedding Hit@3:",
            "EVET"
            if embedding_hit3
            else "HAYIR",
        )

    total = len(
        test_queries
    )

    tfidf_top1_rate = (
        tfidf_top1_correct
        / total
    )

    embedding_top1_rate = (
        embedding_top1_correct
        / total
    )

    tfidf_hit3_rate = (
        tfidf_hit3_correct
        / total
    )

    embedding_hit3_rate = (
        embedding_hit3_correct
        / total
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "--- PARAPHRASE GENEL KARŞILAŞTIRMA ---"
    )

    print("\nTF-IDF")

    print(
        "Top-1:",
        f"{tfidf_top1_correct}/{total}",
        f"(%{tfidf_top1_rate * 100:.2f})",
    )

    print(
        "Hit@3:",
        f"{tfidf_hit3_correct}/{total}",
        f"(%{tfidf_hit3_rate * 100:.2f})",
    )

    print("\nEMBEDDING")

    print(
        "Top-1:",
        f"{embedding_top1_correct}/{total}",
        f"(%{embedding_top1_rate * 100:.2f})",
    )

    print(
        "Hit@3:",
        f"{embedding_hit3_correct}/{total}",
        f"(%{embedding_hit3_rate * 100:.2f})",
    )


if __name__ == "__main__":
    main()