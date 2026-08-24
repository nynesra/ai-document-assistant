from math import isclose#ondalıklı sayıları karşılaştırmak için kullanılır

from src.retriever import (
    build_tfidf_index,
    search,
    search_with_index,
)

def test_tfidf_index_chunk_count() -> None:
    """TF-IDF indeksindeki chunk sayısını kontrol eder."""

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    assert len(chunks) == 37
    assert tfidf_matrix.shape[0] == 37


def test_tfidf_vocabulary() -> None:
    """TF-IDF vocabulary yapısının oluşturulduğunu kontrol eder."""

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    vocabulary = vectorizer.get_feature_names_out()

    assert len(vocabulary) > 0

    assert len(vocabulary) == tfidf_matrix.shape[1]


def test_search_result_count() -> None:
    """top_k=3 kullanıldığında üç sonuç dönmesini kontrol eder."""

    results = search(
        query="Sanal ortam nasıl oluşturulur?",
        top_k=3,
    )

    assert len(results) == 3


def test_correct_source_for_virtual_environment() -> None:
    """Sanal ortam sorgusunda doğru kaynağın ilk sıraya gelmesini kontrol eder."""

    results = search(
        query="Sanal ortam nasıl oluşturulur?",
        top_k=3,
    )

    first_result = results[0]

    assert first_result["source"] == "sanal_ortam.md"


def test_scores_are_sorted() -> None:
    """Arama sonuçlarının benzerlik skoruna göre sıralandığını kontrol eder."""

    results = search(
        query="Sanal ortam nasıl oluşturulur?",
        top_k=3,
    )

    first_score = results[0]["score"]
    second_score = results[1]["score"]
    third_score = results[2]["score"]

    assert first_score >= second_score
    assert second_score >= third_score


def test_result_metadata() -> None:
    """Retrieval sonucunda gerekli metadata alanlarının bulunduğunu kontrol eder."""

    results = search(
        query="Sanal ortam nasıl oluşturulur?",
        top_k=1,
    )

    first_result = results[0]

    assert "source" in first_result
    assert "section" in first_result
    assert "chunk_id" in first_result
    assert "text" in first_result
    assert "score" in first_result


def test_empty_query() -> None:
    """Boş sorgunun ValueError üretmesini kontrol eder."""

    try:
        search(
            query="",
            top_k=3,
        )

    except ValueError:
        return

    raise AssertionError(
        "Boş sorgu için ValueError bekleniyordu."
    )


def test_invalid_top_k() -> None:
    """Geçersiz top_k değerinin ValueError üretmesini kontrol eder."""

    try:
        search(
            query="Python kurulumu",
            top_k=0,
        )

    except ValueError:
        return

    raise AssertionError(
        "top_k=0 için ValueError bekleniyordu."
    )

def test_reusable_tfidf_index() -> None:
    """Aynı TF-IDF indeksinin birden fazla sorguda kullanılmasını test eder."""

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    queries = [
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

    for query, expected_source in queries:
        results = search_with_index(
            query=query,
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=1,
        )

        first_result = results[0]

        assert first_result["source"] == expected_source

def test_top_k_larger_than_chunk_count() -> None:
    """top_k chunk sayısından büyük olduğunda mevcut tüm chunkların dönmesini test eder."""

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    results = search_with_index(
        query="Python kurulumu",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        top_k=100,
    )

    assert len(chunks) == 37
    assert len(results) == 37       

def test_old_and_reusable_methods_match() -> None:
    """Eski ve hazır indeks yöntemlerinin aynı retrieval sonuçlarını verdiğini test eder."""

    query = "Sanal ortam nasıl oluşturulur?"

    old_results = search(
        query=query,
        top_k=3,
    )

    chunks, vectorizer, tfidf_matrix = build_tfidf_index()

    reusable_results = search_with_index(
        query=query,
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        top_k=3,
    )

    assert len(old_results) == len(reusable_results)

    for old_result, reusable_result in zip(#eski ve yeni sonuçları eşşleştirir
        old_results,
        reusable_results,
    ):
        assert (
            old_result["source"]
            == reusable_result["source"]
        )

        assert (
            old_result["section"]
            == reusable_result["section"]
        )

        assert (
            old_result["chunk_id"]
            == reusable_result["chunk_id"]
        )

        assert isclose(
            old_result["score"],
            reusable_result["score"],
            rel_tol=1e-9,
        )

def main() -> None:
    """TF-IDF retrieval modülüne ait testleri çalıştırır."""

    tests = [
        (
            "TF-IDF chunk sayısı testi",
            test_tfidf_index_chunk_count,
        ),
        (
            "TF-IDF vocabulary testi",
            test_tfidf_vocabulary,
        ),
        (
            "Top-K sonuç sayısı testi",
            test_search_result_count,
        ),
        (
            "Doğru kaynak retrieval testi",
            test_correct_source_for_virtual_environment,
        ),
        (
            "Skor sıralama testi",
            test_scores_are_sorted,
        ),
        (
            "Retrieval metadata testi",
            test_result_metadata,
        ),
        (
            "Boş sorgu testi",
            test_empty_query,
        ),
        (
            "Geçersiz top_k testi",
            test_invalid_top_k,
        ),
        (
            "Hazır TF-IDF indeksi tekrar kullanım testi",
            test_reusable_tfidf_index,
        ),
        (
            "Büyük top_k sınır testi",
            test_top_k_larger_than_chunk_count,
        ),
        (
            "Eski ve hazır indeks sonuç eşitliği testi",
            test_old_and_reusable_methods_match,
        ),
    ]

    successful_tests = 0

    print(
        "\n--- 7. GÜN TF-IDF RETRIEVAL TEST SONUÇLARI ---\n"
    )

    for test_name, test_function in tests:
        try:
            test_function()

            successful_tests += 1

            print(
                f"[BAŞARILI] {test_name}"
            )

        except AssertionError as error:
            print(
                f"[BAŞARISIZ] {test_name}: {error}"  
            )

        except Exception as error:
            print(
                f"[HATA] {test_name}: "
                f"{type(error).__name__}: {error}"
            )

    total_tests = len(tests)

    success_rate = (
        successful_tests
        / total_tests
    ) * 100

    print(
        "\n--------------------------------------------"
    )

    print(
        f"Toplam test: {total_tests}"
    )

    print(
        f"Başarılı test: {successful_tests}"
    )

    print(
        f"Test başarı oranı: "
        f"%{success_rate:.2f}"
    )


if __name__ == "__main__":
    main()