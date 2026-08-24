import pytest

from src.retriever import (
    build_tfidf_index,
    search_with_index,
)


@pytest.fixture
def tfidf_index():
    """Testlerde aynı TF-IDF indeksini tekrar kullanır."""

    return build_tfidf_index()


def test_threshold_filters_low_score_results(tfidf_index):
    """
    Threshold uygulanınca düşük skorlu sonuçların
    filtrelenip filtrelenmediğini kontrol eder.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    results = search_with_index(
        query="Loglama neden kullanılır?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        top_k=3,
        threshold=0.20,
    )

    assert len(results) >= 1

    for result in results:
        assert result["score"] >= 0.20


def test_irrelevant_query_is_rejected(tfidf_index):
    """
    Bilgi tabanıyla ilgisiz bir sorgunun
    threshold nedeniyle reddedilmesini kontrol eder.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    results = search_with_index(
        query="Türkiye'nin başkenti neresidir?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        top_k=3,
        threshold=0.20,
    )

    assert results == []


def test_too_high_threshold_can_reject_relevant_query(tfidf_index):
    """
    Çok yüksek threshold değerinin ilgili bir sorguyu
    reddedebildiğini doğrular.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    results = search_with_index(
        query="Loglama neden kullanılır?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        top_k=3,
        threshold=0.30,
    )

    assert results == []


def test_invalid_threshold_raises_error(tfidf_index):
    """
    Threshold değeri 0-1 aralığının dışındaysa
    ValueError verilmesini kontrol eder.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    with pytest.raises(ValueError):
        search_with_index(
            query="Python nasıl kurulur?",
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=3,
            threshold=1.50,
        )