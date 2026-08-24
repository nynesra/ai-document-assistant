from src.retriever import (
    build_tfidf_index,
    search_with_index,
)


def main():
    print("\n--- 10. GÜN PARAPHRASE THRESHOLD DENEYİ ---")

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    top_k = 3
    threshold = 0.20

    test_queries = [
        {
            "query": "Python kurulumu için hangi adımları izlemeliyim?",
            "expected_source": "python_kurulumu.md",
        },
        {
            "query": "FastAPI ne işe yarar?",
            "expected_source": "fastapi_kullanimi.md",
        },
        {
            "query": "Git projesi başlatmak için ne yapmalıyım?",
            "expected_source": "git_komutlari.md",
        },
        {
            "query": "Uygulamada neden log tutulur?",
            "expected_source": "loglama.md",
        },
        {
            "query": "Python için sanal ortamı nasıl hazırlayabilirim?",
            "expected_source": "sanal_ortam.md",
        },
    ]

    correct_source = 0
    rejected = 0

    for test in test_queries:

        query = test["query"]
        expected_source = test["expected_source"]

        # Threshold uygulanmadan önce ham sonuçları alıyoruz.
        raw_results = search_with_index(
            query=query,
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=top_k,
            threshold=0.0,
        )

        raw_top1 = raw_results[0]

        # Seçilen threshold ile sonuçları filtreliyoruz.
        filtered_results = search_with_index(
            query=query,
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=top_k,
            threshold=threshold,
        )

        print("\n" + "-" * 60)

        print("Sorgu:", query)
        print("Beklenen kaynak:", expected_source)

        print(
            "Ham Top-1 kaynak:",
            raw_top1["source"],
        )

        print(
            "Ham Top-1 skor:",
            f"{raw_top1['score']:.4f}",
        )

        # Hiçbir sonuç threshold değerini geçemediyse
        if not filtered_results:

            print(
                "Threshold sonucu:",
                "KAYNAK REDDEDİLDİ",
            )

            rejected += 1
            continue

        # Threshold sonrasında kalan bütün sonuçları gösteriyoruz.
        print("Threshold sonrası sıralama:")

        for rank, result in enumerate(
            filtered_results,
            start=1,
        ):
            print(
                f"{rank}. {result['source']} "
                f"| Skor: {result['score']:.4f}"
            )

        first_result = filtered_results[0]

        print(
            "Threshold sonrası kaynak:",
            first_result["source"],
        )

        print(
            "Threshold sonrası sonuç sayısı:",
            len(filtered_results),
        )

        # Top-1 kaynak beklenen kaynak mı?
        if first_result["source"] == expected_source:

            print("Durum: DOĞRU")
            correct_source += 1

        else:

            print("Durum: YANLIŞ KAYNAK")

    total = len(test_queries)

    accuracy = correct_source / total

    print("\n" + "=" * 60)
    print("--- GENEL SONUÇ ---")

    print(
        "Doğru kaynak:",
        f"{correct_source}/{total}",
    )

    print(
        "Threshold nedeniyle reddedilen:",
        rejected,
    )

    print(
        "Paraphrase Top-1 başarı oranı:",
        f"%{accuracy * 100:.2f}",
    )


if __name__ == "__main__":
    main()