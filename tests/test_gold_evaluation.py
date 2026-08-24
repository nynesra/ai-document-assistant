import pytest

from evaluation.day16_build_eval_set import (
    build_eval_set,
)

from evaluation.day17_gold_eval import (
    evaluate_category_specific,
)

from src.controlled_flow import (
    run_controlled_flow,
)

from src.retriever import (
    build_tfidf_index,
)


@pytest.fixture(scope="module")
def tfidf_index():
    """
    Gold Evaluation testleri boyunca
    TF-IDF indeksini yalnızca bir kez oluşturur.
    """

    return build_tfidf_index()


@pytest.fixture(autouse=True)
def disable_trace_logging(
    monkeypatch,
):
    """
    Otomatik testler sırasında gerçek
    decision_trace.jsonl dosyasına
    kayıt eklenmesini engeller.
    """

    monkeypatch.setattr(
        "src.controlled_flow.save_trace",
        lambda trace: None,
    )


def run_gold_item(
    item,
    tfidf_index,
):
    """
    Tek bir Gold Evaluation kaydını
    Controlled Flow üzerinden çalıştırır.
    """

    (
        chunks,
        vectorizer,
        tfidf_matrix,
    ) = tfidf_index

    return run_controlled_flow(
        query=item["query"],
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )


def test_all_gold_routes_tools_and_statuses(
    tfidf_index,
):
    """
    20 Gold Evaluation kaydının tamamında
    route, tool ve status beklenen değerlerle
    aynı olmalıdır.
    """

    eval_set = build_eval_set()

    for item in eval_set:

        response = run_gold_item(
            item,
            tfidf_index,
        )

        assert (
            response["route"]
            == item["expected_route"]
        )

        assert (
            response["selected_tool"]
            == item["expected_tool"]
        )

        assert (
            response["status"]
            == item["expected_status"]
        )


def test_all_retrieval_gold_items(
    tfidf_index,
):
    """
    Retrieval Gold kayıtlarının tamamında
    kabul edilebilir kaynak Top-1 sırada
    bulunmalıdır.
    """

    eval_set = build_eval_set()

    retrieval_items = [
        item
        for item in eval_set
        if item["category"] == "retrieval"
    ]

    assert len(retrieval_items) == 8

    for item in retrieval_items:

        response = run_gold_item(
            item,
            tfidf_index,
        )

        assert len(
            response["results"]
        ) > 0

        top1_source = (
            response["results"][0]["source"]
        )

        assert (
            top1_source
            in item["expected_sources"]
        )


def test_all_calculator_gold_items(
    tfidf_index,
):
    """
    Calculator Gold kayıtlarının tamamında
    beklenen matematik sonucu üretilmelidir.
    """

    eval_set = build_eval_set()

    calculator_items = [
        item
        for item in eval_set
        if item["category"] == "calculator"
    ]

    assert len(calculator_items) == 4

    for item in calculator_items:

        response = run_gold_item(
            item,
            tfidf_index,
        )

        assert (
            response["result"]
            == item["expected_result"]
        )


def test_all_guardrail_gold_items(
    tfidf_index,
):
    """
    Guardrail Gold kayıtlarının tamamında
    doğru engelleme nedeni üretilmelidir.
    """

    eval_set = build_eval_set()

    guardrail_items = [
        item
        for item in eval_set
        if item["category"] == "guardrail"
    ]

    assert len(guardrail_items) == 3

    for item in guardrail_items:

        response = run_gold_item(
            item,
            tfidf_index,
        )

        assert (
            response["route"]
            == "blocked"
        )

        assert (
            response["selected_tool"]
            == "none"
        )

        assert (
            response["trace"][
                "guardrail_reason"
            ]
            == item[
                "expected_guardrail_reason"
            ]
        )


def test_gold_evaluation_end_to_end(
    tfidf_index,
):
    """
    20 soruluk Gold Evaluation Set üzerinde
    kategoriye özel sonuçlar dahil bütün
    akışların tam doğru olması gerekir.
    """

    eval_set = build_eval_set()

    total = len(eval_set)
    fully_correct = 0

    for item in eval_set:

        response = run_gold_item(
            item,
            tfidf_index,
        )

        route_ok = (
            response["route"]
            == item["expected_route"]
        )

        tool_ok = (
            response["selected_tool"]
            == item["expected_tool"]
        )

        status_ok = (
            response["status"]
            == item["expected_status"]
        )

        specific = (
            evaluate_category_specific(
                item=item,
                response=response,
            )
        )

        category_ok = specific[
            "category_correct"
        ]

        if (
            route_ok
            and tool_ok
            and status_ok
            and category_ok
        ):
            fully_correct += 1

    assert total == 20

    assert fully_correct == 20