from src.query_router import (
    QueryRoute,
    route_query,
)


def main():
    print(
        "\n--- 13. GÜN QUERY ROUTING DENEYİ ---"
    )

    test_queries = [

        # =========================================
        # INVALID
        # =========================================

        {
            "query": "",
            "expected": QueryRoute.INVALID,
        },

        {
            "query": "     ",
            "expected": QueryRoute.INVALID,
        },

        {
            "query": "!!!",
            "expected": QueryRoute.INVALID,
        },

        {
            "query": "???",
            "expected": QueryRoute.INVALID,
        },

        {
            "query": "...!!!",
            "expected": QueryRoute.INVALID,
        },

        # =========================================
        # CALCULATOR
        # =========================================

        {
            "query": "5 + 5 kaç?",
            "expected": QueryRoute.CALCULATOR,
        },

        {
            "query": "10 / 2 nedir?",
            "expected": QueryRoute.CALCULATOR,
        },

        {
            "query": "(8 + 2) * 3 hesapla",
            "expected": QueryRoute.CALCULATOR,
        },

        {
            "query": "7 - 4 sonucu",
            "expected": QueryRoute.CALCULATOR,
        },

        {
            "query": "2.5 * 4 kaçtır?",
            "expected": QueryRoute.CALCULATOR,
        },

        # =========================================
        # RETRIEVAL
        # =========================================

        {
            "query": "Python nasıl kurulur?",
            "expected": QueryRoute.RETRIEVAL,
        },

        {
            "query": "FastAPI nedir?",
            "expected": QueryRoute.RETRIEVAL,
        },

        {
            "query": "Git repository nasıl oluşturulur?",
            "expected": QueryRoute.RETRIEVAL,
        },

        {
            "query": "Loglama neden kullanılır?",
            "expected": QueryRoute.RETRIEVAL,
        },

        {
            "query": "Sanal ortam nasıl oluşturulur?",
            "expected": QueryRoute.RETRIEVAL,
        },

        # =========================================
        # OUT OF SCOPE
        # =========================================

        {
            "query": "Türkiye'nin başkenti nedir?",
            "expected": QueryRoute.OUT_OF_SCOPE,
        },

        {
            "query": "Bugün hava nasıl?",
            "expected": QueryRoute.OUT_OF_SCOPE,
        },

        {
            "query": "En hızlı hayvan hangisidir?",
            "expected": QueryRoute.OUT_OF_SCOPE,
        },

        {
            "query": "5G hangi ülkede geliştirildi?",
            "expected": QueryRoute.OUT_OF_SCOPE,
        },

        {
            "query": "Dünya'nın uydusu nedir?",
            "expected": QueryRoute.OUT_OF_SCOPE,
        },
    ]

    correct = 0
    total = len(test_queries)

    class_total = {
        QueryRoute.INVALID: 0,
        QueryRoute.CALCULATOR: 0,
        QueryRoute.RETRIEVAL: 0,
        QueryRoute.OUT_OF_SCOPE: 0,
    }

    class_correct = {
        QueryRoute.INVALID: 0,
        QueryRoute.CALCULATOR: 0,
        QueryRoute.RETRIEVAL: 0,
        QueryRoute.OUT_OF_SCOPE: 0,
    }

    for test in test_queries:
        query = test["query"]
        expected = test["expected"]

        predicted = route_query(query)

        is_correct = (
            predicted == expected
        )

        class_total[expected] += 1

        if is_correct:
            correct += 1
            class_correct[expected] += 1

        print(
            "\n" + "=" * 60
        )

        print(
            "Sorgu:",
            repr(query),
        )

        print(
            "Beklenen:",
            expected.value,
        )

        print(
            "Tahmin:",
            predicted.value,
        )

        print(
            "Durum:",
            "DOĞRU"
            if is_correct
            else "YANLIŞ",
        )


    # =============================================
    # GENEL SONUÇ
    # =============================================

    accuracy = (
        correct / total
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "--- GENEL ROUTING SONUCU ---"
    )

    print(
        "Toplam sorgu:",
        total,
    )

    print(
        "Doğru karar:",
        correct,
    )

    print(
        "Yanlış karar:",
        total - correct,
    )

    print(
        "Routing Accuracy:",
        f"%{accuracy * 100:.2f}",
    )

    # =============================================
    # SINIF BAZLI SONUÇ
    # =============================================

    print(
        "\n--- SINIF BAZLI SONUÇLAR ---"
    )

    for route in [
        QueryRoute.INVALID,
        QueryRoute.CALCULATOR,
        QueryRoute.RETRIEVAL,
        QueryRoute.OUT_OF_SCOPE,
    ]:

        route_total = (
            class_total[route]
        )

        route_correct = (
            class_correct[route]
        )

        if route_total > 0:
            route_accuracy = (
                route_correct
                / route_total
        )
        else:
            route_accuracy = 0.0

        print(
            f"\n{route.value.upper()}"
        )

        print(
            "Doğru:",
            f"{route_correct}/{route_total}",
        )

        print(
            "Accuracy:",
            f"%{route_accuracy * 100:.2f}",
        )


if __name__ == "__main__":
    main()