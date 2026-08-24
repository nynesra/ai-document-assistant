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
        "\n--- 11. GÜN TF-IDF vs EMBEDDING KARŞILAŞTIRMASI ---"
    )

    # -------------------------
    # TF-IDF indeksi
    # -------------------------

    chunks_tfidf, vectorizer, tfidf_matrix = (
        build_tfidf_index()
    )

    # -------------------------
    # Embedding indeksi
    # -------------------------

    chunks_embedding, model, embeddings = (
        build_embedding_index(
            chunk_size=500,
            overlap=100,
        )
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

    tfidf_top1_correct = 0
    embedding_top1_correct = 0

    tfidf_hit3_correct = 0
    embedding_hit3_correct = 0

    for test in test_queries:

        query = test["query"]
        expected_source = test["expected_source"]

        # -------------------------
        # TF-IDF retrieval
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
        # Embedding retrieval
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

        tfidf_top1 = tfidf_results[0]["source"]

        embedding_top1 = (
            embedding_results[0]["source"]
        )

        # Top-1 kontrolleri

        tfidf_top1_ok = (
            tfidf_top1 == expected_source
        )

        embedding_top1_ok = (
            embedding_top1 == expected_source
        )

        if tfidf_top1_ok:
            tfidf_top1_correct += 1

        if embedding_top1_ok:
            embedding_top1_correct += 1

        # Hit@3 kontrolleri

        tfidf_sources = [
            result["source"]
            for result in tfidf_results
        ]

        embedding_sources = [
            result["source"]
            for result in embedding_results
        ]

        tfidf_hit3 = (
            expected_source in tfidf_sources
        )

        embedding_hit3 = (
            expected_source in embedding_sources
        )

        if tfidf_hit3:
            tfidf_hit3_correct += 1

        if embedding_hit3:
            embedding_hit3_correct += 1

        # -------------------------
        # Sorgu bazında çıktı
        # -------------------------

        print(
            "\n" + "=" * 70
        )

        print(
            "Sorgu:",
            query,
        )

        print(
            "Beklenen:",
            expected_source,
        )

        print(
            "\nTF-IDF Top-1:",
            tfidf_top1,
            "|",
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
            "|",
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

    # -------------------------
    # Genel karşılaştırma
    # -------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "--- GENEL KARŞILAŞTIRMA ---"
    )

    print(
        "\nTF-IDF"
    )

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

    print(
        "\nEMBEDDING"
    )

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