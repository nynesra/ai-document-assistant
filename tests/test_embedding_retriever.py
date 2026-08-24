import pytest

from src.embedding_retriever import (
    load_embedding_model,
    create_embedding,
    build_embedding_index,
    search_with_embedding_index,
)


@pytest.fixture(scope="module")
def embedding_model():
    """
    Embedding modelini bütün testler için
    yalnızca bir kez yükler.
    """

    return load_embedding_model()


@pytest.fixture(scope="module")
def embedding_index():
    """
    Embedding indeksini bütün testler için
    yalnızca bir kez oluşturur.
    """

    return build_embedding_index(
        chunk_size=500,
        overlap=100,
    )


def test_embedding_vector_dimension(
    embedding_model,
):
    """
    Oluşturulan embedding vektörünün
    beklenen boyutta olduğunu kontrol eder.
    """

    embedding = create_embedding(
        text="Python nasıl kurulur?",
        model=embedding_model,
    )

    assert embedding.shape == (384,)


def test_empty_embedding_text_raises_error(
    embedding_model,
):
    """
    Boş metin için embedding oluşturulmasına
    izin verilmediğini kontrol eder.
    """

    with pytest.raises(ValueError):
        create_embedding(
            text="   ",
            model=embedding_model,
        )


def test_embedding_retrieval_returns_expected_source(
    embedding_index,
):
    """
    Bilinen bir sorguda doğru kaynağın
    Top-1 olarak geldiğini kontrol eder.
    """

    chunks, model, embeddings = embedding_index

    results = search_with_embedding_index(
        query="Python nasıl kurulur?",
        chunks=chunks,
        model=model,
        embeddings=embeddings,
        top_k=3,
    )

    assert len(results) == 3

    assert (
        results[0]["source"]
        == "python_kurulumu.md"
    )


def test_invalid_top_k_raises_error(
    embedding_index,
):
    """
    Geçersiz Top-K değerinde ValueError
    oluşturulduğunu kontrol eder.
    """

    chunks, model, embeddings = embedding_index

    with pytest.raises(ValueError):
        search_with_embedding_index(
            query="Python nasıl kurulur?",
            chunks=chunks,
            model=model,
            embeddings=embeddings,
            top_k=0,
        )