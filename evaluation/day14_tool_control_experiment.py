from src.controlled_flow import run_controlled_flow
from src.query_router import QueryRoute
from src.retriever import build_tfidf_index
from src.tool_executor import execute_tool
from src.tool_registry import ToolName


def trace_is_complete(trace):
    """
    Trace içerisinde beklenen temel alanların
    tamamının bulunup bulunmadığını kontrol eder.
    """

    required_fields = [
        "timestamp",
        "query",
        "route",
        "selected_tool",
        "tool_status",
        "message",
        "result",
        "result_count",
        "top_source",
        "top_score",
    ]

    return all(
        field in trace
        for field in required_fields
    )


def main():
    print(
        "\n--- 14. GÜN KONTROLLÜ TOOL-CALL DENEYİ ---"
    )

    (
        chunks,
        vectorizer,
        tfidf_matrix,
    ) = build_tfidf_index()

    # =================================================
    # NORMAL CONTROLLED FLOW TEST SETİ
    # =================================================

    test_cases = [

        # ---------------------------------------------
        # CALCULATOR
        # ---------------------------------------------

        {
            "query": "5 + 5 kaç?",
            "expected_route": "calculator",
            "expected_tool": "calculator",
            "expected_tool_status": "success",
        },

        {
            "query": "10 / 2 nedir?",
            "expected_route": "calculator",
            "expected_tool": "calculator",
            "expected_tool_status": "success",
        },

        {
            "query": "3 x 7 kaç?",
            "expected_route": "calculator",
            "expected_tool": "calculator",
            "expected_tool_status": "success",
        },

        {
            "query": "20 bölü 4 kaç?",
            "expected_route": "calculator",
            "expected_tool": "calculator",
            "expected_tool_status": "success",
        },

        # ---------------------------------------------
        # RETRIEVAL
        # ---------------------------------------------

        {
            "query": "Python nasıl kurulur?",
            "expected_route": "retrieval",
            "expected_tool": "retriever",
            "expected_tool_status": "success",
        },

        {
            "query": "FastAPI nedir?",
            "expected_route": "retrieval",
            "expected_tool": "retriever",
            "expected_tool_status": "success",
        },

        {
            "query": "Loglama neden kullanılır?",
            "expected_route": "retrieval",
            "expected_tool": "retriever",
            "expected_tool_status": "success",
        },

        {
            "query": "Sanal ortam nasıl oluşturulur?",
            "expected_route": "retrieval",
            "expected_tool": "retriever",
            "expected_tool_status": "success",
        },

        # ---------------------------------------------
        # OUT OF SCOPE
        # ---------------------------------------------

        {
            "query": "Türkiye'nin başkenti nedir?",
            "expected_route": "out_of_scope",
            "expected_tool": "none",
            "expected_tool_status": "not_executed",
        },

        {
            "query": "Bugün hava nasıl?",
            "expected_route": "out_of_scope",
            "expected_tool": "none",
            "expected_tool_status": "not_executed",
        },

        {
            "query": "En hızlı hayvan hangisidir?",
            "expected_route": "out_of_scope",
            "expected_tool": "none",
            "expected_tool_status": "not_executed",
        },

        {
            "query": "Dünya'nın uydusu nedir?",
            "expected_route": "out_of_scope",
            "expected_tool": "none",
            "expected_tool_status": "not_executed",
        },

        # ---------------------------------------------
        # INVALID
        # ---------------------------------------------

        {
            "query": "",
            "expected_route": "invalid",
            "expected_tool": "none",
            "expected_tool_status": "not_executed",
        },

        {
            "query": "     ",
            "expected_route": "invalid",
            "expected_tool": "none",
            "expected_tool_status": "not_executed",
        },

        {
            "query": "!!!",
            "expected_route": "invalid",
            "expected_tool": "none",
            "expected_tool_status": "not_executed",
        },

        {
            "query": "...???",
            "expected_route": "invalid",
            "expected_tool": "none",
            "expected_tool_status": "not_executed",
        },
    ]

    total = len(test_cases)

    route_correct = 0
    tool_correct = 0
    status_correct = 0
    trace_complete = 0
    fully_correct = 0

    # =================================================
    # CONTROLLED FLOW DENEYİ
    # =================================================

    for test in test_cases:

        response = run_controlled_flow(
            query=test["query"],
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
        )

        actual_route = response["route"]

        actual_tool = response[
            "selected_tool"
        ]

        actual_status = response[
            "status"
        ]

        trace = response["trace"]

        route_ok = (
            actual_route
            == test["expected_route"]
        )

        tool_ok = (
            actual_tool
            == test["expected_tool"]
        )

        status_ok = (
            actual_status
            == test["expected_tool_status"]
        )

        trace_ok = trace_is_complete(
            trace
        )

        full_ok = (
            route_ok
            and tool_ok
            and status_ok
            and trace_ok
        )

        if route_ok:
            route_correct += 1

        if tool_ok:
            tool_correct += 1

        if status_ok:
            status_correct += 1

        if trace_ok:
            trace_complete += 1

        if full_ok:
            fully_correct += 1

        print(
            "\n" + "=" * 70
        )

        print(
            "Sorgu:",
            repr(test["query"]),
        )

        print(
            "Beklenen route:",
            test["expected_route"],
        )

        print(
            "Gerçek route:",
            actual_route,
        )

        print(
            "Beklenen tool:",
            test["expected_tool"],
        )

        print(
            "Gerçek tool:",
            actual_tool,
        )

        print(
            "Beklenen tool status:",
            test["expected_tool_status"],
        )

        print(
            "Gerçek tool status:",
            actual_status,
        )

        print(
            "Trace eksiksiz:",
            "EVET"
            if trace_ok
            else "HAYIR",
        )

        print(
            "Genel durum:",
            "DOĞRU"
            if full_ok
            else "YANLIŞ",
        )

    # =================================================
    # CONTROLLED FLOW METRİKLERİ
    # =================================================

    route_accuracy = (
        route_correct / total
    )

    tool_accuracy = (
        tool_correct / total
    )

    status_accuracy = (
        status_correct / total
    )

    trace_completeness = (
        trace_complete / total
    )

    end_to_end_accuracy = (
        fully_correct / total
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "--- CONTROLLED FLOW GENEL SONUCU ---"
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
        "Doğru tool status:",
        status_correct,
    )

    print(
        "Eksiksiz trace:",
        trace_complete,
    )

    print(
        "Tam doğru akış:",
        fully_correct,
    )

    print(
        "Route Accuracy:",
        f"%{route_accuracy * 100:.2f}",
    )

    print(
        "Tool Selection Accuracy:",
        f"%{tool_accuracy * 100:.2f}",
    )

    print(
        "Tool Status Accuracy:",
        f"%{status_accuracy * 100:.2f}",
    )

    print(
        "Trace Completeness:",
        f"%{trace_completeness * 100:.2f}",
    )

    print(
        "End-to-End Controlled Flow Accuracy:",
        f"%{end_to_end_accuracy * 100:.2f}",
    )

    # =================================================
    # YETKİSİZ TOOL ÇAĞRISI DENEYLERİ
    # =================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "--- YETKİSİZ TOOL ÇAĞRISI DENEYİ ---"
    )

    unauthorized_cases = [

        {
            "route": QueryRoute.CALCULATOR,
            "tool": ToolName.RETRIEVER,
            "query": "5 + 5 kaç?",
        },

        {
            "route": QueryRoute.RETRIEVAL,
            "tool": ToolName.CALCULATOR,
            "query": "Python nasıl kurulur?",
        },

        {
            "route": QueryRoute.OUT_OF_SCOPE,
            "tool": ToolName.RETRIEVER,
            "query": "Türkiye'nin başkenti nedir?",
        },

        {
            "route": QueryRoute.INVALID,
            "tool": ToolName.CALCULATOR,
            "query": "!!!",
        },
    ]

    blocked_count = 0

    for case in unauthorized_cases:

        response = execute_tool(
            route=case["route"],
            tool=case["tool"],
            query=case["query"],
            chunks=chunks,
            vectorizer=vectorizer,
            tfidf_matrix=tfidf_matrix,
        )

        blocked = (
            response["status"]
            == "blocked"
        )

        if blocked:
            blocked_count += 1

        print(
            "\nRoute:",
            case["route"].value,
        )

        print(
            "Zorlanan tool:",
            case["tool"].value,
        )

        print(
            "Status:",
            response["status"],
        )

        print(
            "Engellendi:",
            "EVET"
            if blocked
            else "HAYIR",
        )

    unauthorized_total = len(
        unauthorized_cases
    )

    block_rate = (
        blocked_count
        / unauthorized_total
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "--- TOOL YETKİ KONTROLÜ SONUCU ---"
    )

    print(
        "Yetkisiz çağrı:",
        unauthorized_total,
    )

    print(
        "Engellenen çağrı:",
        blocked_count,
    )

    print(
        "Tool Block Rate:",
        f"%{block_rate * 100:.2f}",
    )


if __name__ == "__main__":
    main()