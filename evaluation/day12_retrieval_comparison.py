from src.retriever import (
    build_tfidf_index,
    search_with_index,
)

from src.embedding_retriever import (
    build_embedding_index,
    search_with_embedding_index,
)


def reciprocal_rank_at_3(
    results,
    expected_sources,
):
    """
    Kabul edilebilir kaynaklardan ilk bulunanın
    Top-3 içerisindeki reciprocal rank değerini hesaplar.
    """

    for rank, result in enumerate(
        results[:3],
        start=1,
    ):
        if result["source"] in expected_sources:
            return 1 / rank

    return 0.0


def evaluate_results(
    results,
    expected_sources,
):
    """
    Retrieval sonucu için Top-1, Hit@3
    ve RR@3 metriklerini hesaplar.
    """

    top1_source = results[0]["source"]

    top1_correct = (
        top1_source in expected_sources
    )

    top3_sources = [
        result["source"]
        for result in results[:3]
    ]

    hit3 = any(
        source in top3_sources
        for source in expected_sources
    )

    rr3 = reciprocal_rank_at_3(
        results=results,
        expected_sources=expected_sources,
    )

    return {
        "top1_source": top1_source,
        "top1_correct": top1_correct,
        "hit3": hit3,
        "rr3": rr3,
    }


def create_empty_metrics():
    """
    Metrik toplamlarını tutmak için
    boş sayaç yapısı oluşturur.
    """

    return {
        "total": 0,
        "top1_correct": 0,
        "hit3_correct": 0,
        "rr3_sum": 0.0,
    }


def update_metrics(
    metrics,
    evaluation,
):
    """
    Tek bir sorgunun sonucunu
    genel metriklere ekler.
    """

    metrics["total"] += 1

    if evaluation["top1_correct"]:
        metrics["top1_correct"] += 1

    if evaluation["hit3"]:
        metrics["hit3_correct"] += 1

    metrics["rr3_sum"] += evaluation["rr3"]


def print_metrics(
    title,
    metrics,
):
    """
    Bir sorgu grubunun performans
    sonuçlarını terminale yazdırır.
    """

    total = metrics["total"]

    if total == 0:
        return

    top1_rate = (
        metrics["top1_correct"]
        / total
    )

    hit3_rate = (
        metrics["hit3_correct"]
        / total
    )

    mrr3 = (
        metrics["rr3_sum"]
        / total
    )

    print("\n" + "-" * 65)

    print(title)

    print(
        "Toplam sorgu:",
        total,
    )

    print(
        "Top-1:",
        f"{metrics['top1_correct']}/{total}",
        f"(%{top1_rate * 100:.2f})",
    )

    print(
        "Hit@3:",
        f"{metrics['hit3_correct']}/{total}",
        f"(%{hit3_rate * 100:.2f})",
    )

    print(
        "MRR@3:",
        f"{mrr3:.4f}",
    )


def main():
    print(
        "\n--- 12. GÜN KAPSAMLI RETRIEVAL KARŞILAŞTIRMASI ---"
    )

    # ------------------------------------------------
    # TF-IDF İNDEKSİ
    # ------------------------------------------------

    (
        tfidf_chunks,
        vectorizer,
        tfidf_matrix,
    ) = build_tfidf_index()

    # ------------------------------------------------
    # EMBEDDING İNDEKSİ
    # ------------------------------------------------

    (
        embedding_chunks,
        model,
        embeddings,
    ) = build_embedding_index(
        chunk_size=500,
        overlap=100,
    )

    top_k = 3

    # ------------------------------------------------
    # TEST SETİ
    # ------------------------------------------------

    test_queries = [

        # ================================================
        # BASIC
        # ================================================

        {
            "type": "basic",
            "query": "Sanal ortam nasıl oluşturulur?",
            "expected_sources": [
                "sanal_ortam.md",
                "servis_kurulumu.md",
            ],
        },

        {
            "type": "basic",
            "query": "Python nasıl kurulur?",
            "expected_sources": [
                "python_kurulumu.md",
            ],
        },

        {
            "type": "basic",
            "query": "FastAPI nedir?",
            "expected_sources": [
                "fastapi_kullanimi.md",
            ],
        },

        {
            "type": "basic",
            "query": "Git deposu nasıl oluşturulur?",
            "expected_sources": [
                "git_komutlari.md",
            ],
        },

        {
            "type": "basic",
            "query": "Loglama neden kullanılır?",
            "expected_sources": [
                "loglama.md",
            ],
        },

        # ================================================
        # PARAPHRASE
        # ================================================

        {
            "type": "paraphrase",
            "query":
                "Python kurulumu için hangi adımları izlemeliyim?",
            "expected_sources": [
                "python_kurulumu.md",
            ],
        },

        {
            "type": "paraphrase",
            "query":
                "FastAPI ne işe yarar?",
            "expected_sources": [
                "fastapi_kullanimi.md",
            ],
        },

        {
            "type": "paraphrase",
            "query":
                "Git projesi başlatmak için ne yapmalıyım?",
            "expected_sources": [
                "git_komutlari.md",
            ],
        },

        {
            "type": "paraphrase",
            "query":
                "Uygulamada neden log tutulur?",
            "expected_sources": [
                "loglama.md",
            ],
        },

        {
            "type": "paraphrase",
            "query":
                "Python için sanal ortamı nasıl hazırlayabilirim?",
            "expected_sources": [
                "sanal_ortam.md",
                "servis_kurulumu.md",
            ],
        },

        # ================================================
        # TERMINOLOGY
        # ================================================

        {
            "type": "terminology",
            "query":
                "Git repository nasıl oluşturulur?",
            "expected_sources": [
                "git_komutlari.md",
            ],
        },

        {
            "type": "terminology",
            "query":
                "Yeni bir Git repository nasıl başlatılır?",
            "expected_sources": [
                "git_komutlari.md",
            ],
        },

        {
            "type": "terminology",
            "query":
                "Git projesi başlatmak için hangi komut kullanılır?",
            "expected_sources": [
                "git_komutlari.md",
            ],
        },

        {
            "type": "terminology",
            "query":
                "git init komutu ne işe yarar?",
            "expected_sources": [
                "git_komutlari.md",
            ],
        },
    ]

    # ------------------------------------------------
    # GENEL METRİKLER
    # ------------------------------------------------

    tfidf_general = create_empty_metrics()
    embedding_general = create_empty_metrics()

    # ------------------------------------------------
    # SORGU TÜRÜ BAZLI METRİKLER
    # ------------------------------------------------

    query_types = [
        "basic",
        "paraphrase",
        "terminology",
    ]

    tfidf_by_type = {
        query_type: create_empty_metrics()
        for query_type in query_types
    }

    embedding_by_type = {
        query_type: create_empty_metrics()
        for query_type in query_types
    }

    # ------------------------------------------------
    # DENEY
    # ------------------------------------------------

    for test in test_queries:

        query = test["query"]
        query_type = test["type"]
        expected_sources = (
            test["expected_sources"]
        )

        # -------------------------
        # TF-IDF
        # -------------------------

        tfidf_results = search_with_index(
            query=query,
            chunks=tfidf_chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=top_k,
            threshold=0.0,
        )

        tfidf_eval = evaluate_results(
            results=tfidf_results,
            expected_sources=expected_sources,
        )

        # -------------------------
        # EMBEDDING
        # -------------------------

        embedding_results = (
            search_with_embedding_index(
                query=query,
                chunks=embedding_chunks,
                model=model,
                embeddings=embeddings,
                top_k=top_k,
            )
        )

        embedding_eval = evaluate_results(
            results=embedding_results,
            expected_sources=expected_sources,
        )

        # -------------------------
        # GENEL METRİKLER
        # -------------------------

        update_metrics(
            tfidf_general,
            tfidf_eval,
        )

        update_metrics(
            embedding_general,
            embedding_eval,
        )

        # -------------------------
        # TÜR BAZLI METRİKLER
        # -------------------------

        update_metrics(
            tfidf_by_type[query_type],
            tfidf_eval,
        )

        update_metrics(
            embedding_by_type[query_type],
            embedding_eval,
        )

        # -------------------------
        # SORGU BAZINDA ÇIKTI
        # -------------------------

        print(
            "\n" + "=" * 70
        )

        print(
            "Sorgu türü:",
            query_type.upper(),
        )

        print(
            "Sorgu:",
            query,
        )

        print(
            "Kabul edilebilir kaynaklar:",
            ", ".join(expected_sources),
        )

        print("\nTF-IDF")

        print(
            "Top-1:",
            tfidf_eval["top1_source"],
        )

        print(
            "Top-1 durum:",
            "DOĞRU"
            if tfidf_eval["top1_correct"]
            else "YANLIŞ",
        )

        print(
            "Hit@3:",
            "EVET"
            if tfidf_eval["hit3"]
            else "HAYIR",
        )

        print(
            "RR@3:",
            f"{tfidf_eval['rr3']:.4f}",
        )

        print("\nEMBEDDING")

        print(
            "Top-1:",
            embedding_eval["top1_source"],
        )

        print(
            "Top-1 durum:",
            "DOĞRU"
            if embedding_eval["top1_correct"]
            else "YANLIŞ",
        )

        print(
            "Hit@3:",
            "EVET"
            if embedding_eval["hit3"]
            else "HAYIR",
        )

        print(
            "RR@3:",
            f"{embedding_eval['rr3']:.4f}",
        )

    # ------------------------------------------------
    # SORGU TÜRÜ BAZLI SONUÇLAR
    # ------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "--- SORGU TÜRÜ BAZLI SONUÇLAR ---"
    )

    for query_type in query_types:

        print(
            "\n" + "=" * 65
        )

        print(
            f"SORGU TÜRÜ: {query_type.upper()}"
        )

        print_metrics(
            "TF-IDF",
            tfidf_by_type[query_type],
        )

        print_metrics(
            "EMBEDDING",
            embedding_by_type[query_type],
        )

    # ------------------------------------------------
    # GENEL SONUÇLAR
    # ------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "--- GENEL KARŞILAŞTIRMA ---"
    )

    print_metrics(
        "TF-IDF GENEL",
        tfidf_general,
    )

    print_metrics(
        "EMBEDDING GENEL",
        embedding_general,
    )


if __name__ == "__main__":
    main()