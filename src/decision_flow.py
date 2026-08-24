from src.query_router import (
    QueryRoute,
    route_query,
    extract_math_expression,
)

from src.calculator_tool import calculate

from src.retriever import (
    build_tfidf_index,
    search_with_index,
)


DEFAULT_TOP_K = 3
DEFAULT_THRESHOLD = 0.20


def execute_query(
    query: str,
    chunks,
    vectorizer,
    tfidf_matrix,
    top_k: int = DEFAULT_TOP_K,
    threshold: float = DEFAULT_THRESHOLD,
):
    """
    Kullanıcı sorgusunu sınıflandırır
    ve yalnızca uygun aracı çalıştırır.
    """

    route = route_query(query)

    # ==========================================
    # INVALID
    # ==========================================

    if route == QueryRoute.INVALID:
        return {
            "route": route.value,
            "status": "rejected",
            "message": (
                "Geçerli bir soru giriniz."
            ),
            "result": None,
            "results": [],
        }

    # ==========================================
    # CALCULATOR
    # ==========================================

    if route == QueryRoute.CALCULATOR:
        expression = extract_math_expression(
            query
        )

        if expression is None:
            return {
                "route": route.value,
                "status": "error",
                "message": (
                    "Matematik ifadesi çözümlenemedi."
                ),
                "result": None,
                "results": [],
            }

        try:
            calculation_result = calculate(
                expression
            )

        except ValueError as exc:
            return {
                "route": route.value,
                "status": "error",
                "message": str(exc),
                "result": None,
                "results": [],
            }

        return {
            "route": route.value,
            "status": "success",
            "message": (
                "Hesaplama başarıyla tamamlandı."
            ),
            "result": calculation_result,
            "results": [],
        }

        # ==========================================
    # OUT OF SCOPE
    # ==========================================

    if route == QueryRoute.OUT_OF_SCOPE:
        return {
            "route": route.value,
            "status": "rejected",
            "message": (
                "Bu soru mevcut teknik doküman "
                "bilgi tabanının kapsamı dışındadır."
            ),
            "result": None,
            "results": [],
        }
    
    # ==========================================
    # RETRIEVAL
    # ==========================================

    if route == QueryRoute.RETRIEVAL:
        results = search_with_index(
            query=query,
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=top_k,
            threshold=threshold,
        )

        # Threshold sonrasında yeterli
        # kaynak kalmadıysa kesin cevap verme.
        if not results:
            return {
                "route": route.value,
                "status": "insufficient_source",
                "message": (
                    "Dokümanlarda bu soruyu "
                    "yanıtlamak için yeterli "
                    "kaynak bulunamadı."
                ),
                "result": None,
                "results": [],
            }

        return {
            "route": route.value,
            "status": "success",
            "message": (
                "İlgili doküman parçaları bulundu."
            ),
            "result": None,
            "results": results,
        }

    raise ValueError(
        "Desteklenmeyen query route."
    )


def main():
    (
        chunks,
        vectorizer,
        tfidf_matrix,
    ) = build_tfidf_index()

    sample_queries = [
    "5 + 5 kaç?",
    "Python nasıl kurulur?",
    "Türkiye'nin başkenti nedir?",
    "5G hangi ülkede geliştirildi?",
    "!!!",
]

    for query in sample_queries:
        response = execute_query(
            query=query,
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
        )

        print("\n" + "=" * 60)

        print(
            "Sorgu:",
            query,
        )

        print(
            "Route:",
            response["route"],
        )

        print(
            "Status:",
            response["status"],
        )

        print(
            "Mesaj:",
            response["message"],
        )

        if response["result"] is not None:
            print(
                "Sonuç:",
                response["result"],
            )

        if response["results"]:
            print(
                "Kaynak:",
                response["results"][0]["source"],
            )

            print(
                "Skor:",
                f"{response['results'][0]['score']:.4f}",
            )


if __name__ == "__main__":
    main()