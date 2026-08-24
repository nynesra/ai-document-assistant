from src.query_router import (
    QueryRoute,
    route_query,
)


def main():
    print(
        "\n--- 13. GÜN ROUTING SINIR DURUMLARI ---"
    )

    test_queries = [

        # -----------------------------------------
        # Calculator - mevcut sembolik kullanım
        # -----------------------------------------

        {
            "query": "12 + 8",
            "expected": QueryRoute.CALCULATOR,
        },

        {
            "query": "-5 + 10 kaç?",
            "expected": QueryRoute.CALCULATOR,
        },

        {
            "query": "(4 + 6) / 2 nedir?",
            "expected": QueryRoute.CALCULATOR,
        },

        {
            "query": "2,5 * 4 kaçtır?",
            "expected": QueryRoute.CALCULATOR,
        },

        # -----------------------------------------
        # Calculator - doğal dil / farklı gösterim
        # -----------------------------------------

        {
            "query": "3 x 7 kaç?",
            "expected": QueryRoute.CALCULATOR,
        },

        {
            "query": "20 bölü 4 kaç?",
            "expected": QueryRoute.CALCULATOR,
        },

        # -----------------------------------------
        # Retrieval
        # -----------------------------------------

        {
            "query": "Python 3 nasıl kurulur?",
            "expected": QueryRoute.RETRIEVAL,
        },

        {
            "query": "FastAPI ile servis nasıl oluşturulur?",
            "expected": QueryRoute.RETRIEVAL,
        },

        {
            "query": "Git init komutu ne işe yarar?",
            "expected": QueryRoute.RETRIEVAL,
        },

        # -----------------------------------------
        # Invalid
        # -----------------------------------------

        {
            "query": "---",
            "expected": QueryRoute.INVALID,
        },

        {
            "query": "()",
            "expected": QueryRoute.INVALID,
        },

        {
            "query": "   ???   ",
            "expected": QueryRoute.INVALID,
        },
    ]

    correct = 0
    errors = []

    for test in test_queries:
        query = test["query"]
        expected = test["expected"]

        predicted = route_query(query)

        is_correct = (
            predicted == expected
        )

        if is_correct:
            correct += 1
        else:
            errors.append(
                {
                    "query": query,
                    "expected": expected.value,
                    "predicted": predicted.value,
                }
            )

        print("\n" + "=" * 60)

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

    total = len(test_queries)

    accuracy = (
        correct / total
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "--- SINIR DURUMU SONUCU ---"
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
        "Accuracy:",
        f"%{accuracy * 100:.2f}",
    )

    if errors:
        print(
            "\n--- HATALI ROUTINGLER ---"
        )

        for error in errors:
            print(
                "\nSorgu:",
                error["query"],
            )

            print(
                "Beklenen:",
                error["expected"],
            )

            print(
                "Tahmin:",
                error["predicted"],
            )


if __name__ == "__main__":
    main()