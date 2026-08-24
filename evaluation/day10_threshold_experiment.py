from src.retriever import (
    build_tfidf_index,
    search_with_index,
)


def main():
    print("\n--- 10. GÜN SIMILARITY THRESHOLD DENEYİ ---")

    # 9. gün sonunda seçilen yapı:
    # Chunk Size = 500
    # Overlap = 100
    # Top-K = 3

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    top_k = 3

    thresholds = [
        0.00,
        0.05,
        0.10,
        0.15,
        0.20,
        0.25,
        0.30,
    ]

    # True:
    # Bilgi tabanında bu sorguyla ilgili kaynak bulunması bekleniyor.
    #
    # False:
    # Bilgi tabanında ilgili kaynak bulunmaması bekleniyor.

    test_queries = [
        {
            "query": "Sanal ortam nasıl oluşturulur?",
            "should_find": True,
        },
        {
            "query": "Python nasıl kurulur?",
            "should_find": True,
        },
        {
            "query": "FastAPI nedir?",
            "should_find": True,
        },
        {
            "query": "Git deposu nasıl oluşturulur?",
            "should_find": True,
        },
        {
            "query": "Loglama neden kullanılır?",
            "should_find": True,
        },

        {
            "query": "Türkiye'nin başkenti neresidir?",
            "should_find": False,
        },
        {
            "query": "5 + 5 kaçtır?",
            "should_find": False,
        },
        {
            "query": "En hızlı hayvan hangisidir?",
            "should_find": False,
        },
        {
            "query": "Bugün hava nasıl?",
            "should_find": False,
        },
        {
            "query": "Dünya'nın uydusu nedir?",
            "should_find": False,
        },
    ]

    print("Toplam chunk:", len(chunks))
    print("Top-K:", top_k)

    print(
        "TF-IDF matris boyutu:",
        tfidf_matrix.shape,
    )

    print(
        "Vocabulary boyutu:",
        len(vectorizer.get_feature_names_out()),
    )

    # Her threshold değeri ayrı ayrı denenir.
    for threshold in thresholds:

        print("\n" + "=" * 65)
        print(
            f"THRESHOLD: {threshold:.2f}"
        )
        print("=" * 65)

        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0

        total_returned_chunks = 0

        for test in test_queries:

            query = test["query"]
            should_find = test["should_find"]

            # Önce threshold olmadan gerçek Top-1 skorunu
            # görmek için ham retrieval sonucu alınır.
            raw_results = search_with_index(
                query=query,
                chunks=chunks,
                vectorizer=vectorizer,
                tfidf_matrix=tfidf_matrix,
                top_k=top_k,
                threshold=0.0,
            )

            raw_top1_score = raw_results[0]["score"]

            # Şimdi incelenen threshold uygulanır.
            filtered_results = search_with_index(
                query=query,
                chunks=chunks,
                vectorizer=vectorizer,
                tfidf_matrix=tfidf_matrix,
                top_k=top_k,
                threshold=threshold,
            )

            found = len(filtered_results) > 0

            total_returned_chunks += len(
                filtered_results
            )

            # Confusion Matrix değerlerini hesaplıyoruz.

            if should_find and found:
                true_positive += 1
                status = "DOĞRU KABUL"

            elif should_find and not found:
                false_negative += 1
                status = "YANLIŞ RET"

            elif not should_find and not found:
                true_negative += 1
                status = "DOĞRU RET"

            else:
                false_positive += 1
                status = "YANLIŞ KABUL"

            print(
                f"\nSorgu: {query}"
            )

            print(
                "Beklenen:",
                "KAYNAK BUL" if should_find
                else "KAYNAK BULMA",
            )

            print(
                "Top-1 ham skor:",
                f"{raw_top1_score:.4f}",
            )

            print(
                "Threshold sonrası sonuç sayısı:",
                len(filtered_results),
            )

            print(
                "Karar:",
                status,
            )

        total_tests = len(test_queries)

        correct = (
            true_positive
            + true_negative
        )

        accuracy = (
            correct
            / total_tests
        )

        relevant_total = sum(
            1
            for test in test_queries
            if test["should_find"]
        )

        irrelevant_total = (
            total_tests
            - relevant_total
        )

        relevant_accept_rate = (
            true_positive
            / relevant_total
        )

        irrelevant_reject_rate = (
            true_negative
            / irrelevant_total
        )

        average_returned_chunks = (
            total_returned_chunks
            / total_tests
        )

        print("\n--- GENEL SONUÇ ---")

        print(
            "True Positive:",
            true_positive,
        )

        print(
            "True Negative:",
            true_negative,
        )

        print(
            "False Positive:",
            false_positive,
        )

        print(
            "False Negative:",
            false_negative,
        )

        print(
            "Karar doğruluğu:",
            f"%{accuracy * 100:.2f}",
        )

        print(
            "İlgili sorgu kabul oranı:",
            f"%{relevant_accept_rate * 100:.2f}",
        )

        print(
            "İlgisiz sorgu ret oranı:",
            f"%{irrelevant_reject_rate * 100:.2f}",
        )

        print(
            "Ortalama dönen chunk sayısı:",
            f"{average_returned_chunks:.2f}",
        )


if __name__ == "__main__":
    main()