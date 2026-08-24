from src.embedding_retriever import (
    build_embedding_index,
    search_with_embedding_index,
)


def main():
    print(
        "\n--- 11. GÜN GIT EMBEDDING HATA ANALİZİ ---"
    )

    # Embedding indeksini oluşturuyoruz.
    chunks, model, embeddings = build_embedding_index(
        chunk_size=500,
        overlap=100,
    )

    expected_source = "git_komutlari.md"

    # Aynı Git bilgisini farklı ifadelerle soruyoruz.
    queries = [
        "Git deposu nasıl oluşturulur?",
        "Git repository nasıl oluşturulur?",
        "Yeni bir Git repository nasıl başlatılır?",
        "Git projesi başlatmak için hangi komut kullanılır?",
        "git init komutu ne işe yarar?",
    ]

    print(
        "Toplam chunk sayısı:",
        len(chunks),
    )

    print(
        "Embedding matris boyutu:",
        embeddings.shape,
    )

    for query in queries:

        # Bütün chunkları sıralıyoruz.
        # Böylece git_komutlari.md dosyasının
        # gerçek sırasını görebiliyoruz.
        results = search_with_embedding_index(
            query=query,
            chunks=chunks,
            model=model,
            embeddings=embeddings,
            top_k=len(chunks),
        )

        top1_result = results[0]

        best_git_rank = None
        best_git_score = None
        best_git_result = None

        # git_komutlari.md kaynağının
        # sıralamadaki en iyi konumunu buluyoruz.
        for rank, result in enumerate(
            results,
            start=1,
        ):
            if result["source"] == expected_source:

                best_git_rank = rank
                best_git_score = result["score"]
                best_git_result = result

                break

        print(
            "\n" + "=" * 70
        )

        print(
            "Sorgu:",
            query,
        )

        print(
            "\nEmbedding Top-1 kaynak:",
            top1_result["source"],
        )

        print(
            "Top-1 skor:",
            f"{top1_result['score']:.4f}",
        )

        if best_git_rank is None:

            print(
                "\ngit_komutlari.md sonucu bulunamadı."
            )

            continue

        print(
            "\nEn iyi git_komutlari.md sırası:",
            best_git_rank,
        )

        print(
            "git_komutlari.md skoru:",
            f"{best_git_score:.4f}",
        )

        # Top-3 içerisinde mi?
        if best_git_rank <= 3:
            print(
                "Hit@3: EVET"
            )
        else:
            print(
                "Hit@3: HAYIR"
            )

        # Beklenen kaynak Top-1 mi?
        if best_git_rank == 1:
            print(
                "Top-1 Durum: DOĞRU"
            )
        else:
            print(
                "Top-1 Durum: YANLIŞ"
            )

        # Hata incelemesi için ilgili Git chunkını gösteriyoruz.
        print(
            "\nGit chunk bölümü:",
            best_git_result["section"],
        )

        print(
            "Git chunk metni:"
        )

        print(
            best_git_result["text"][:400]
        )


if __name__ == "__main__":
    main()