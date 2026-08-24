from src.decision_flow import execute_query
from src.retriever import build_tfidf_index


def main():
    print(
        "\n--- 13. GÜN FİNAL DECISION FLOW DENEYİ ---"
    )

    (
        chunks,
        vectorizer,
        tfidf_matrix,
    ) = build_tfidf_index()

    test_cases = [

        # =============================================
        # CALCULATOR -> SUCCESS
        # =============================================

        {
            "query": "5 + 5 kaç?",
            "expected_route": "calculator",
            "expected_status": "success",
        },

        {
            "query": "10 / 2 nedir?",
            "expected_route": "calculator",
            "expected_status": "success",
        },

        {
            "query": "3 x 7 kaç?",
            "expected_route": "calculator",
            "expected_status": "success",
        },

        {
            "query": "20 bölü 4 kaç?",
            "expected_route": "calculator",
            "expected_status": "success",
        },

        # =============================================
        # RETRIEVAL -> SUCCESS
        # =============================================

        {
            "query": "Python nasıl kurulur?",
            "expected_route": "retrieval",
            "expected_status": "success",
        },

        {
            "query": "FastAPI nedir?",
            "expected_route": "retrieval",
            "expected_status": "success",
        },

        {
            "query": "Loglama neden kullanılır?",
            "expected_route": "retrieval",
            "expected_status": "success",
        },

        {
            "query": "Sanal ortam nasıl oluşturulur?",
            "expected_route": "retrieval",
            "expected_status": "success",
        },

        # =============================================
        # RETRIEVAL -> INSUFFICIENT SOURCE
        #
        # Bu bölümde threshold bilerek 0.99
        # kullanılarak güvenli ret dalı test edilir.
        # =============================================

        {
            "query": "Python nasıl kurulur?",
            "expected_route": "retrieval",
            "expected_status": "insufficient_source",
            "threshold": 0.99,
        },

        {
            "query": "FastAPI nedir?",
            "expected_route": "retrieval",
            "expected_status": "insufficient_source",
            "threshold": 0.99,
        },

        {
            "query": "Loglama neden kullanılır?",
            "expected_route": "retrieval",
            "expected_status": "insufficient_source",
            "threshold": 0.99,
        },

        {
            "query": "Sanal ortam nasıl oluşturulur?",
            "expected_route": "retrieval",
            "expected_status": "insufficient_source",
            "threshold": 0.99,
        },

        # =============================================
        # OUT OF SCOPE -> REJECTED
        # =============================================

        {
            "query": "Türkiye'nin başkenti nedir?",
            "expected_route": "out_of_scope",
            "expected_status": "rejected",
        },

        {
            "query": "Bugün hava nasıl?",
            "expected_route": "out_of_scope",
            "expected_status": "rejected",
        },

        {
            "query": "En hızlı hayvan hangisidir?",
            "expected_route": "out_of_scope",
            "expected_status": "rejected",
        },

        {
            "query": "5G hangi ülkede geliştirildi?",
            "expected_route": "out_of_scope",
            "expected_status": "rejected",
        },

        # =============================================
        # INVALID -> REJECTED
        # =============================================

        {
            "query": "",
            "expected_route": "invalid",
            "expected_status": "rejected",
        },

        {
            "query": "     ",
            "expected_route": "invalid",
            "expected_status": "rejected",
        },

        {
            "query": "!!!",
            "expected_route": "invalid",
            "expected_status": "rejected",
        },

        {
            "query": "...???",
            "expected_route": "invalid",
            "expected_status": "rejected",
        },
    ]

    total = len(test_cases)

    correct_route = 0
    correct_status = 0
    fully_correct = 0

    outcome_counts = {
        "calculator_success": 0,
        "retrieval_success": 0,
        "insufficient_source": 0,
        "out_of_scope_rejected": 0,
        "invalid_rejected": 0,
    }

    errors = []

    for test in test_cases:

        threshold = test.get(
            "threshold",
            0.20,
        )

        response = execute_query(
            query=test["query"],
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            threshold=threshold,
        )

        actual_route = response["route"]
        actual_status = response["status"]

        route_ok = (
            actual_route
            == test["expected_route"]
        )

        status_ok = (
            actual_status
            == test["expected_status"]
        )

        full_ok = (
            route_ok
            and status_ok
        )

        if route_ok:
            correct_route += 1

        if status_ok:
            correct_status += 1

        if full_ok:
            fully_correct += 1

        else:
            errors.append({
                "query": test["query"],
                "expected_route":
                    test["expected_route"],
                "actual_route":
                    actual_route,
                "expected_status":
                    test["expected_status"],
                "actual_status":
                    actual_status,
            })

        # =============================================
        # ÇIKTI DAĞILIMI
        # =============================================

        if (
            actual_route == "calculator"
            and actual_status == "success"
        ):
            outcome_counts[
                "calculator_success"
            ] += 1

        elif (
            actual_route == "retrieval"
            and actual_status == "success"
        ):
            outcome_counts[
                "retrieval_success"
            ] += 1

        elif (
            actual_route == "retrieval"
            and actual_status
            == "insufficient_source"
        ):
            outcome_counts[
                "insufficient_source"
            ] += 1

        elif (
            actual_route == "out_of_scope"
            and actual_status == "rejected"
        ):
            outcome_counts[
                "out_of_scope_rejected"
            ] += 1

        elif (
            actual_route == "invalid"
            and actual_status == "rejected"
        ):
            outcome_counts[
                "invalid_rejected"
            ] += 1

        print(
            "\n" + "=" * 65
        )

        print(
            "Sorgu:",
            repr(test["query"]),
        )

        print(
            "Threshold:",
            threshold,
        )

        print(
            "Beklenen:",
            test["expected_route"],
            "/",
            test["expected_status"],
        )

        print(
            "Gerçek:",
            actual_route,
            "/",
            actual_status,
        )

        print(
            "Durum:",
            "DOĞRU"
            if full_ok
            else "YANLIŞ",
        )

    # =============================================
    # METRİKLER
    # =============================================

    route_accuracy = (
        correct_route / total
    )

    status_accuracy = (
        correct_status / total
    )

    end_to_end_accuracy = (
        fully_correct / total
    )

    print(
        "\n" + "=" * 65
    )

    print(
        "--- GENEL DECISION FLOW SONUCU ---"
    )

    print(
        "Toplam sorgu:",
        total,
    )

    print(
        "Doğru route:",
        correct_route,
    )

    print(
        "Doğru status:",
        correct_status,
    )

    print(
        "Tam doğru karar:",
        fully_correct,
    )

    print(
        "Route Accuracy:",
        f"%{route_accuracy * 100:.2f}",
    )

    print(
        "Status Accuracy:",
        f"%{status_accuracy * 100:.2f}",
    )

    print(
        "End-to-End Accuracy:",
        f"%{end_to_end_accuracy * 100:.2f}",
    )

    # =============================================
    # DAĞILIM
    # =============================================

    print(
        "\n--- DECISION FLOW DAĞILIMI ---"
    )

    print(
        "Calculator Success:",
        outcome_counts[
            "calculator_success"
        ],
    )

    print(
        "Retrieval Success:",
        outcome_counts[
            "retrieval_success"
        ],
    )

    print(
        "Insufficient Source:",
        outcome_counts[
            "insufficient_source"
        ],
    )

    print(
        "Out of Scope Rejected:",
        outcome_counts[
            "out_of_scope_rejected"
        ],
    )

    print(
        "Invalid Rejected:",
        outcome_counts[
            "invalid_rejected"
        ],
    )

    # =============================================
    # HATALAR
    # =============================================

    if errors:

        print(
            "\n--- HATALI SONUÇLAR ---"
        )

        for error in errors:

            print(
                "\nSorgu:",
                repr(error["query"]),
            )

            print(
                "Beklenen:",
                error["expected_route"],
                "/",
                error["expected_status"],
            )

            print(
                "Gerçek:",
                error["actual_route"],
                "/",
                error["actual_status"],
            )


if __name__ == "__main__":
    main()