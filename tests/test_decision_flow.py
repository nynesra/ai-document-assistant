import pytest

from src.decision_flow import execute_query
from src.retriever import build_tfidf_index


@pytest.fixture(scope="module")
def tfidf_index():
    """
    Test modülü boyunca TF-IDF indeksini
    yalnızca bir kez oluşturur.
    """

    return build_tfidf_index()


def test_invalid_query_is_rejected(tfidf_index):
    """
    Yalnızca noktalama işaretlerinden oluşan
    sorgu INVALID olarak reddedilmelidir.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    response = execute_query(
        query="!!!",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )

    assert response["route"] == "invalid"
    assert response["status"] == "rejected"
    assert response["result"] is None
    assert response["results"] == []


def test_calculator_query_uses_calculator(tfidf_index):
    """
    Matematiksel sorgu calculator route'una
    yönlendirilmeli ve doğru sonuç üretilmelidir.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    response = execute_query(
        query="5 + 5 kaç?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )

    assert response["route"] == "calculator"
    assert response["status"] == "success"
    assert response["result"] == 10
    assert response["results"] == []


def test_retrieval_query_finds_expected_source(
    tfidf_index,
):
    """
    Doküman sorusu retrieval route'una
    gitmeli ve beklenen kaynağı bulmalıdır.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    response = execute_query(
        query="Python nasıl kurulur?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )

    assert response["route"] == "retrieval"
    assert response["status"] == "success"

    assert len(response["results"]) > 0

    assert (
        response["results"][0]["source"]
        == "python_kurulumu.md"
    )

    assert response["results"][0]["score"] >= 0.20


def test_out_of_scope_query_is_rejected(
    tfidf_index,
):
    """
    Bilgi tabanı kapsamı dışındaki genel bilgi
    sorusu retriever çalıştırılmadan reddedilmelidir.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    response = execute_query(
        query="Türkiye'nin başkenti nedir?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )

    assert response["route"] == "out_of_scope"
    assert response["status"] == "rejected"
    assert response["result"] is None
    assert response["results"] == []

def test_calculator_error_is_controlled(
    tfidf_index,
):
    """
    Calculator içinde oluşan hata sistemden
    kontrolsüz şekilde dışarı çıkmamalıdır.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    response = execute_query(
        query="10 / 0 kaç?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )

    assert response["route"] == "calculator"
    assert response["status"] == "error"
    assert response["result"] is None
    assert response["results"] == []

    assert (
        response["message"]
        == "Sıfıra bölme işlemi yapılamaz."
    )

def test_multiplication_with_x_uses_calculator(
    tfidf_index,
):
    """
    Kullanıcının çarpma işlemini 'x' ile
    yazması calculator tarafından desteklenmelidir.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    response = execute_query(
        query="3 x 7 kaç?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )

    assert response["route"] == "calculator"
    assert response["status"] == "success"
    assert response["result"] == 21
    assert response["results"] == []


def test_turkish_division_word_uses_calculator(
    tfidf_index,
):
    """
    Kullanıcının bölme işlemini 'bölü' kelimesiyle
    yazması calculator tarafından desteklenmelidir.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    response = execute_query(
        query="20 bölü 4 kaç?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )

    assert response["route"] == "calculator"
    assert response["status"] == "success"
    assert response["result"] == 5
    assert response["results"] == []


def test_5g_false_positive_is_blocked_by_scope_control(
    tfidf_index,
):
    """
    TF-IDF'nin daha önce 0.2928 skorla yanlış
    kaynak kabul ettiği 5G sorgusu scope
    kontrolünde durdurulmalıdır.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    response = execute_query(
        query="5G hangi ülkede geliştirildi?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )

    assert response["route"] == "out_of_scope"
    assert response["status"] == "rejected"
    assert response["result"] is None
    assert response["results"] == []


def test_retrieval_can_return_insufficient_source(
    tfidf_index,
):
    """
    Sorgu bilgi tabanı kapsamında olsa bile
    yeterli similarity skoru bulunmadığında
    kesin cevap verilmemelidir.
    """

    chunks, vectorizer, tfidf_matrix = tfidf_index

    response = execute_query(
        query="Python nasıl kurulur?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        threshold=0.99,
    )

    assert response["route"] == "retrieval"

    assert (
        response["status"]
        == "insufficient_source"
    )

    assert response["result"] is None
    assert response["results"] == []