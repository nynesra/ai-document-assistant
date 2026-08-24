from src.calculator_tool import calculate
from src.query_router import (
    QueryRoute,
    extract_math_expression,
)
from src.tool_registry import (
    ToolName,
    is_tool_allowed,
)


def execute_tool(
    route: QueryRoute,
    tool: ToolName,
    query: str,
    chunks=None,
    vectorizer=None,
    tfidf_matrix=None,
    top_k: int = 3,
    threshold: float = 0.20,
):
    """
    Yalnızca route tarafından izin verilen
    tool'un çalıştırılmasını sağlar.
    """

    # ==========================================
    # TOOL YETKİ KONTROLÜ
    # ==========================================

    if not is_tool_allowed(
        route=route,
        tool=tool,
    ):
        return {
            "status": "blocked",
            "tool": tool.value,
            "message": (
                "Seçilen tool bu route için "
                "çalıştırılamaz."
            ),
            "result": None,
            "results": [],
        }

    # ==========================================
    # NONE
    # ==========================================

    if tool == ToolName.NONE:
        return {
            "status": "not_executed",
            "tool": tool.value,
            "message": (
                "Bu sorgu için tool çağrısı "
                "gerekmiyor."
            ),
            "result": None,
            "results": [],
        }

    # ==========================================
    # CALCULATOR
    # ==========================================

    if tool == ToolName.CALCULATOR:
        expression = extract_math_expression(
            query
        )

        if expression is None:
            return {
                "status": "error",
                "tool": tool.value,
                "message": (
                    "Matematik ifadesi "
                    "çıkarılamadı."
                ),
                "result": None,
                "results": [],
            }

        try:
            result = calculate(
                expression
            )

        except ValueError as exc:
            return {
                "status": "error",
                "tool": tool.value,
                "message": str(exc),
                "result": None,
                "results": [],
            }

        return {
            "status": "success",
            "tool": tool.value,
            "message": (
                "Calculator Tool başarıyla "
                "çalıştırıldı."
            ),
            "result": result,
            "results": [],
        }

    # ==========================================
    # RETRIEVER
    # ==========================================

    if tool == ToolName.RETRIEVER:
        if (
            chunks is None
            or vectorizer is None
            or tfidf_matrix is None
        ):
            return {
                "status": "error",
                "tool": tool.value,
                "message": (
                    "Retriever için gerekli "
                    "indeks bileşenleri eksik."
                ),
                "result": None,
                "results": [],
            }

        from src.retriever import (
            search_with_index,
        )

        results = search_with_index(
            query=query,
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
            top_k=top_k,
            threshold=threshold,
        )

        if not results:
            return {
                "status": "insufficient_source",
                "tool": tool.value,
                "message": (
                    "Yeterli similarity skoruna "
                    "sahip kaynak bulunamadı."
                ),
                "result": None,
                "results": [],
            }

        return {
            "status": "success",
            "tool": tool.value,
            "message": (
                "Retriever Tool başarıyla "
                "çalıştırıldı."
            ),
            "result": None,
            "results": results,
        }

    raise ValueError(
        f"Desteklenmeyen tool: {tool}"
    )
