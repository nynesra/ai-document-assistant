import pytest

from evaluation.day12_retrieval_comparison import (
    reciprocal_rank_at_3,
    evaluate_results,
)


def test_reciprocal_rank_first_position():
    """
    Doğru kaynak ilk sıradaysa
    RR@3 değerinin 1 olması gerekir.
    """

    results = [
        {"source": "python_kurulumu.md"},
        {"source": "sanal_ortam.md"},
        {"source": "loglama.md"},
    ]

    expected_sources = [
        "python_kurulumu.md",
    ]

    rr = reciprocal_rank_at_3(
        results=results,
        expected_sources=expected_sources,
    )

    assert rr == 1.0


def test_reciprocal_rank_second_position():
    """
    Doğru kaynak ikinci sıradaysa
    RR@3 değerinin 1/2 olması gerekir.
    """

    results = [
        {"source": "servis_kurulumu.md"},
        {"source": "sanal_ortam.md"},
        {"source": "python_kurulumu.md"},
    ]

    expected_sources = [
        "sanal_ortam.md",
    ]

    rr = reciprocal_rank_at_3(
        results=results,
        expected_sources=expected_sources,
    )

    assert rr == 0.5


def test_no_expected_source_in_top3():
    """
    Kabul edilebilir kaynak Top-3 içerisinde
    bulunmuyorsa RR@3 sıfır olmalıdır.
    """

    results = [
        {"source": "veri_temizleme.md"},
        {"source": "python_kurulumu.md"},
        {"source": "loglama.md"},
    ]

    expected_sources = [
        "git_komutlari.md",
    ]

    evaluation = evaluate_results(
        results=results,
        expected_sources=expected_sources,
    )

    assert evaluation["top1_correct"] is False
    assert evaluation["hit3"] is False
    assert evaluation["rr3"] == 0.0


def test_multiple_expected_sources_are_supported():
    """
    Bir sorgu için birden fazla kabul edilebilir
    kaynak bulunduğunda bunlardan herhangi biri
    Top-1 ise sonuç doğru kabul edilmelidir.
    """

    results = [
        {"source": "servis_kurulumu.md"},
        {"source": "sanal_ortam.md"},
        {"source": "python_kurulumu.md"},
    ]

    expected_sources = [
        "sanal_ortam.md",
        "servis_kurulumu.md",
    ]

    evaluation = evaluate_results(
        results=results,
        expected_sources=expected_sources,
    )

    assert evaluation["top1_correct"] is True
    assert evaluation["hit3"] is True
    assert evaluation["rr3"] == 1.0