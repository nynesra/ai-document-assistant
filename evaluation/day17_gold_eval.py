import json
from pathlib import Path

from src.controlled_flow import (
    run_controlled_flow,
)

from src.retriever import (
    build_tfidf_index,
)


EVAL_SET_PATH = Path(
    "evaluation/eval_set.json"
)


def load_eval_set():
    """
    16. gün hazırlanan Gold Evaluation Set'i
    JSON dosyasından yükler.
    """

    with EVAL_SET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def calculator_result_matches(
    actual,
    expected,
    tolerance=1e-9,
):
    """
    Calculator sonuçlarını küçük floating-point
    farklılıklarına karşı güvenli biçimde karşılaştırır.
    """

    if (
        isinstance(actual, (int, float))
        and isinstance(expected, (int, float))
    ):
        return (
            abs(actual - expected)
            <= tolerance
        )

    return actual == expected


def evaluate_category_specific(
    item,
    response,
):
    """
    Sorgunun kategorisine göre ek doğruluk
    kontrollerini gerçekleştirir.
    """

    category = item["category"]

    result = {
        "category_correct": True,
        "retrieval_top1_correct": None,
        "retrieval_hit3": None,
        "calculator_correct": None,
        "guardrail_reason_correct": None,
    }

    # ==========================================
    # RETRIEVAL
    # ==========================================

    if category == "retrieval":

        results = response.get(
            "results",
            [],
        )

        expected_sources = item[
            "expected_sources"
        ]

        if results:
            top1_source = results[0][
                "source"
            ]

            top1_correct = (
                top1_source
                in expected_sources
            )

        else:
            top1_correct = False

        top3_sources = [
            result_item["source"]
            for result_item
            in results[:3]
        ]

        hit3 = any(
            source in top3_sources
            for source in expected_sources
        )

        result[
            "retrieval_top1_correct"
        ] = top1_correct

        result[
            "retrieval_hit3"
        ] = hit3

        # End-to-End doğruluk için
        # Top-1 kaynağı esas alıyoruz.
        result[
            "category_correct"
        ] = top1_correct

    # ==========================================
    # CALCULATOR
    # ==========================================

    elif category == "calculator":

        actual_result = response.get(
            "result"
        )

        expected_result = item[
            "expected_result"
        ]

        calculator_correct = (
            calculator_result_matches(
                actual=actual_result,
                expected=expected_result,
            )
        )

        result[
            "calculator_correct"
        ] = calculator_correct

        result[
            "category_correct"
        ] = calculator_correct

    # ==========================================
    # GUARDRAIL
    # ==========================================

    elif category == "guardrail":

        trace = response["trace"]

        actual_reason = trace.get(
            "guardrail_reason"
        )

        expected_reason = item[
            "expected_guardrail_reason"
        ]

        reason_correct = (
            actual_reason
            == expected_reason
        )

        result[
            "guardrail_reason_correct"
        ] = reason_correct

        result[
            "category_correct"
        ] = reason_correct

    # ==========================================
    # OUT OF SCOPE / INVALID
    # ==========================================

    else:
        # Bu kategorilerde route/tool/status
        # kontrolü yeterli kabul edilmektedir.
        result[
            "category_correct"
        ] = True

    return result


def main():

    print(
        "\n--- 17. GÜN GOLD EVALUATION ---"
    )

    eval_set = load_eval_set()

    (
        chunks,
        vectorizer,
        tfidf_matrix,
    ) = build_tfidf_index()

    total = len(eval_set)

    route_correct = 0
    tool_correct = 0
    status_correct = 0
    category_correct = 0
    end_to_end_correct = 0

    # ==========================================
    # KATEGORİ ÖZEL METRİKLER
    # ==========================================

    retrieval_total = 0
    retrieval_top1_correct = 0
    retrieval_hit3_correct = 0

    calculator_total = 0
    calculator_correct = 0

    guardrail_total = 0
    guardrail_reason_correct = 0

    # ==========================================
    # KATEGORİ BAZLI E2E
    # ==========================================

    category_totals = {}
    category_e2e_correct = {}

    errors = []

    # ==========================================
    # EVALUATION LOOP
    # ==========================================

    for item in eval_set:

        response = run_controlled_flow(
            query=item["query"],
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
        )

        actual_route = response[
            "route"
        ]

        actual_tool = response[
            "selected_tool"
        ]

        actual_status = response[
            "status"
        ]

        route_ok = (
            actual_route
            == item["expected_route"]
        )

        tool_ok = (
            actual_tool
            == item["expected_tool"]
        )

        status_ok = (
            actual_status
            == item["expected_status"]
        )

        specific = (
            evaluate_category_specific(
                item=item,
                response=response,
            )
        )

        specific_ok = specific[
            "category_correct"
        ]

        full_ok = (
            route_ok
            and tool_ok
            and status_ok
            and specific_ok
        )

        # ======================================
        # GENEL SAYACLAR
        # ======================================

        if route_ok:
            route_correct += 1

        if tool_ok:
            tool_correct += 1

        if status_ok:
            status_correct += 1

        if specific_ok:
            category_correct += 1

        if full_ok:
            end_to_end_correct += 1

        # ======================================
        # KATEGORİ SAYACLARI
        # ======================================

        category = item[
            "category"
        ]

        category_totals[
            category
        ] = (
            category_totals.get(
                category,
                0,
            )
            + 1
        )

        if full_ok:

            category_e2e_correct[
                category
            ] = (
                category_e2e_correct.get(
                    category,
                    0,
                )
                + 1
            )

        # ======================================
        # RETRIEVAL METRİKLERİ
        # ======================================

        if category == "retrieval":

            retrieval_total += 1

            if specific[
                "retrieval_top1_correct"
            ]:
                retrieval_top1_correct += 1

            if specific[
                "retrieval_hit3"
            ]:
                retrieval_hit3_correct += 1

        # ======================================
        # CALCULATOR METRİKLERİ
        # ======================================

        elif category == "calculator":

            calculator_total += 1

            if specific[
                "calculator_correct"
            ]:
                calculator_correct += 1

        # ======================================
        # GUARDRAIL METRİKLERİ
        # ======================================

        elif category == "guardrail":

            guardrail_total += 1

            if specific[
                "guardrail_reason_correct"
            ]:
                guardrail_reason_correct += 1

        # ======================================
        # HATALAR
        # ======================================

        if not full_ok:

            errors.append({
                "id": item["id"],
                "category": category,
                "query": item["query"],
                "expected_route":
                    item["expected_route"],
                "actual_route":
                    actual_route,
                "expected_tool":
                    item["expected_tool"],
                "actual_tool":
                    actual_tool,
                "expected_status":
                    item["expected_status"],
                "actual_status":
                    actual_status,
                "category_specific_correct":
                    specific_ok,
            })

        # ======================================
        # SORGU BAZLI ÇIKTI
        # ======================================

        print(
            "\n" + "=" * 72
        )

        print(
            "ID:",
            item["id"],
        )

        print(
            "Kategori:",
            category,
        )

        print(
            "Sorgu:",
            repr(item["query"]),
        )

        print(
            "Route:",
            actual_route,
            "|",
            "DOĞRU"
            if route_ok
            else "YANLIŞ",
        )

        print(
            "Tool:",
            actual_tool,
            "|",
            "DOĞRU"
            if tool_ok
            else "YANLIŞ",
        )

        print(
            "Status:",
            actual_status,
            "|",
            "DOĞRU"
            if status_ok
            else "YANLIŞ",
        )

        if category == "retrieval":

            print(
                "Retrieval Top-1:",
                "DOĞRU"
                if specific[
                    "retrieval_top1_correct"
                ]
                else "YANLIŞ",
            )

            print(
                "Hit@3:",
                "EVET"
                if specific[
                    "retrieval_hit3"
                ]
                else "HAYIR",
            )

            if response["results"]:

                print(
                    "Top-1 kaynak:",
                    response[
                        "results"
                    ][0]["source"],
                )

                print(
                    "Top-1 skor:",
                    f"{response['results'][0]['score']:.4f}",
                )

        elif category == "calculator":

            print(
                "Sonuç:",
                response["result"],
            )

            print(
                "Calculator sonucu:",
                "DOĞRU"
                if specific[
                    "calculator_correct"
                ]
                else "YANLIŞ",
            )

        elif category == "guardrail":

            print(
                "Guardrail reason:",
                response[
                    "trace"
                ][
                    "guardrail_reason"
                ],
            )

            print(
                "Reason:",
                "DOĞRU"
                if specific[
                    "guardrail_reason_correct"
                ]
                else "YANLIŞ",
            )

        print(
            "End-to-End:",
            "DOĞRU"
            if full_ok
            else "YANLIŞ",
        )

    # ==========================================
    # GENEL METRİKLER
    # ==========================================

    route_accuracy = (
        route_correct / total
    )

    tool_accuracy = (
        tool_correct / total
    )

    status_accuracy = (
        status_correct / total
    )

    category_accuracy = (
        category_correct / total
    )

    end_to_end_accuracy = (
        end_to_end_correct / total
    )

    print(
        "\n" + "=" * 72
    )

    print(
        "--- GENEL GOLD EVALUATION SONUCU ---"
    )

    print(
        "Toplam sorgu:",
        total,
    )

    print(
        "Doğru route:",
        route_correct,
    )

    print(
        "Doğru tool:",
        tool_correct,
    )

    print(
        "Doğru status:",
        status_correct,
    )

    print(
        "Doğru kategori özel sonuç:",
        category_correct,
    )

    print(
        "Tam doğru End-to-End:",
        end_to_end_correct,
    )

    print(
        "Route Accuracy:",
        f"%{route_accuracy * 100:.2f}",
    )

    print(
        "Tool Accuracy:",
        f"%{tool_accuracy * 100:.2f}",
    )

    print(
        "Status Accuracy:",
        f"%{status_accuracy * 100:.2f}",
    )

    print(
        "Category-Specific Accuracy:",
        f"%{category_accuracy * 100:.2f}",
    )

    print(
        "End-to-End Accuracy:",
        f"%{end_to_end_accuracy * 100:.2f}",
    )

    # ==========================================
    # RETRIEVAL
    # ==========================================

    retrieval_top1_accuracy = (
        retrieval_top1_correct
        / retrieval_total
    )

    retrieval_hit3 = (
        retrieval_hit3_correct
        / retrieval_total
    )

    print(
        "\n--- RETRIEVAL SONUÇLARI ---"
    )

    print(
        "Toplam retrieval:",
        retrieval_total,
    )

    print(
        "Doğru Top-1:",
        retrieval_top1_correct,
    )

    print(
        "Hit@3 başarılı:",
        retrieval_hit3_correct,
    )

    print(
        "Retrieval Top-1 Accuracy:",
        f"%{retrieval_top1_accuracy * 100:.2f}",
    )

    print(
        "Retrieval Hit@3:",
        f"%{retrieval_hit3 * 100:.2f}",
    )

    # ==========================================
    # CALCULATOR
    # ==========================================

    calculator_accuracy = (
        calculator_correct
        / calculator_total
    )

    print(
        "\n--- CALCULATOR SONUÇLARI ---"
    )

    print(
        "Toplam calculator:",
        calculator_total,
    )

    print(
        "Doğru sonuç:",
        calculator_correct,
    )

    print(
        "Calculator Accuracy:",
        f"%{calculator_accuracy * 100:.2f}",
    )

    # ==========================================
    # GUARDRAIL
    # ==========================================

    guardrail_accuracy = (
        guardrail_reason_correct
        / guardrail_total
    )

    print(
        "\n--- GUARDRAIL SONUÇLARI ---"
    )

    print(
        "Toplam guardrail:",
        guardrail_total,
    )

    print(
        "Doğru reason:",
        guardrail_reason_correct,
    )

    print(
        "Guardrail Reason Accuracy:",
        f"%{guardrail_accuracy * 100:.2f}",
    )

    # ==========================================
    # KATEGORİ BAZLI E2E
    # ==========================================

    print(
        "\n--- KATEGORİ BAZLI END-TO-END ---"
    )

    for category, count in (
        category_totals.items()
    ):

        correct = (
            category_e2e_correct.get(
                category,
                0,
            )
        )

        accuracy = (
            correct / count
        )

        print(
            f"\n{category.upper()}"
        )

        print(
            "Doğru:",
            f"{correct}/{count}",
        )

        print(
            "Accuracy:",
            f"%{accuracy * 100:.2f}",
        )

    # ==========================================
    # HATALAR
    # ==========================================

    if errors:

        print(
            "\n--- HATALI GOLD EVALUATION SONUÇLARI ---"
        )

        for error in errors:

            print(
                "\nID:",
                error["id"],
            )

            print(
                "Kategori:",
                error["category"],
            )

            print(
                "Sorgu:",
                repr(error["query"]),
            )

            print(
                "Beklenen route / gerçek:",
                error["expected_route"],
                "/",
                error["actual_route"],
            )

            print(
                "Beklenen tool / gerçek:",
                error["expected_tool"],
                "/",
                error["actual_tool"],
            )

            print(
                "Beklenen status / gerçek:",
                error["expected_status"],
                "/",
                error["actual_status"],
            )

            print(
                "Kategori özel doğru:",
                error[
                    "category_specific_correct"
                ],
            )


if __name__ == "__main__":
    main()