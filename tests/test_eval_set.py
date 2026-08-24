from evaluation.day16_build_eval_set import (
    build_eval_set,
)

from evaluation.day16_validate_eval_set import (
    validate_eval_set,
)


def test_eval_set_has_20_items():
    """
    Gold Evaluation Set toplam 20
    kayıt içermelidir.
    """

    eval_set = build_eval_set()

    assert len(eval_set) == 20


def test_eval_set_has_unique_ids():
    """
    Evaluation Set içerisindeki bütün
    ID değerleri benzersiz olmalıdır.
    """

    eval_set = build_eval_set()

    ids = [
        item["id"]
        for item in eval_set
    ]

    assert len(ids) == len(set(ids))


def test_eval_set_has_no_duplicate_queries():
    """
    Aynı sorgu birden fazla kez
    kullanılmamalıdır.
    """

    eval_set = build_eval_set()

    queries = [
        item["query"]
        .strip()
        .casefold()
        for item in eval_set
    ]

    assert len(queries) == len(set(queries))


def test_eval_set_category_distribution():
    """
    Kategori dağılımı belirlenen Gold
    Evaluation Set tasarımına uymalıdır.
    """

    eval_set = build_eval_set()

    counts = {}

    for item in eval_set:

        category = item["category"]

        counts[category] = (
            counts.get(
                category,
                0,
            )
            + 1
        )

    assert counts["retrieval"] == 8
    assert counts["calculator"] == 4
    assert counts["out_of_scope"] == 3
    assert counts["invalid"] == 2
    assert counts["guardrail"] == 3


def test_retrieval_items_have_expected_sources():
    """
    Retrieval kayıtlarında en az bir
    kabul edilebilir kaynak bulunmalıdır.
    """

    eval_set = build_eval_set()

    retrieval_items = [
        item
        for item in eval_set
        if item["category"] == "retrieval"
    ]

    for item in retrieval_items:

        assert "expected_sources" in item

        assert isinstance(
            item["expected_sources"],
            list,
        )

        assert (
            len(item["expected_sources"])
            > 0
        )


def test_calculator_items_have_expected_result():
    """
    Calculator kayıtlarında beklenen
    hesaplama sonucu bulunmalıdır.
    """

    eval_set = build_eval_set()

    calculator_items = [
        item
        for item in eval_set
        if item["category"] == "calculator"
    ]

    for item in calculator_items:

        assert "expected_result" in item


def test_guardrail_items_have_expected_reason():
    """
    Guardrail kayıtlarında beklenen
    engelleme nedeni bulunmalıdır.
    """

    eval_set = build_eval_set()

    guardrail_items = [
        item
        for item in eval_set
        if item["category"] == "guardrail"
    ]

    for item in guardrail_items:

        assert (
            "expected_guardrail_reason"
            in item
        )


def test_eval_set_passes_validator():
    """
    Gold Evaluation Set bütün validation
    kontrollerinden hatasız geçmelidir.
    """

    eval_set = build_eval_set()

    errors = validate_eval_set(
        eval_set
    )

    assert errors == []