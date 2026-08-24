from datetime import datetime, timezone

from src.guardrails import check_input_guardrails

from src.query_router import (
    QueryRoute,
    route_query,
)

from src.tool_registry import (
    ToolName,
    select_tool,
)

from src.tool_executor import execute_tool

from src.trace_logger import save_trace


def create_trace(
    query: str,
    route: QueryRoute,
    tool: ToolName,
    tool_response: dict,
    guardrail: dict,
):
    """
    Bir sorgu için alınan guardrail,
    routing ve tool kararlarını
    izlenebilir bir kayıt haline getirir.
    """

    results = tool_response.get(
        "results",
        [],
    )

    top_source = None
    top_score = None

    if results:
        top_source = results[0].get(
            "source"
        )

        top_score = results[0].get(
            "score"
        )

    return {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "query": query,

        "route": route.value,

        "selected_tool": tool.value,

        "tool_status": tool_response[
            "status"
        ],

        "guardrail_allowed": (
            guardrail["allowed"]
        ),

        "guardrail_reason": (
            guardrail["reason"]
        ),

        "message": tool_response[
            "message"
        ],

        "result": tool_response.get(
            "result"
        ),

        "result_count": len(
            results
        ),

        "top_source": top_source,

        "top_score": top_score,
    }


def create_blocked_trace(
    query: str,
    guardrail: dict,
):
    """
    Guardrail tarafından engellenen
    bir sorgu için trace oluşturur.
    """

    return {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "query": query,

        "route": "blocked",

        "selected_tool": "none",

        "tool_status": (
            "guardrail_blocked"
        ),

        "guardrail_allowed": False,

        "guardrail_reason": (
            guardrail["reason"]
        ),

        "message": (
            guardrail["message"]
        ),

        "result": None,

        "result_count": 0,

        "top_source": None,

        "top_score": None,
    }


def run_controlled_flow(
    query: str,
    chunks=None,
    vectorizer=None,
    tfidf_matrix=None,
    top_k: int = 3,
    threshold: float = 0.20,
):
    """
    Kullanıcı sorgusunu:

    Input Guardrail
        ->
    Query Router
        ->
    Tool Selection
        ->
    Controlled Tool Execution
        ->
    Decision Trace
        ->
    JSONL Log

    akışından geçirir.
    """

    # ==========================================
    # 0. INPUT GUARDRAIL
    # ==========================================

    guardrail = check_input_guardrails(
        query
    )

    if not guardrail["allowed"]:

        blocked_trace = create_blocked_trace(
            query=query,
            guardrail=guardrail,
        )

        save_trace(
            blocked_trace
        )

        return {
            "route": "blocked",
            "selected_tool": "none",
            "status": "guardrail_blocked",
            "message": guardrail["message"],
            "result": None,
            "results": [],
            "trace": blocked_trace,
        }

    # ==========================================
    # 1. ROUTING
    # ==========================================

    route = route_query(
        query
    )

    # ==========================================
    # 2. TOOL SELECTION
    # ==========================================

    tool = select_tool(
        route
    )

    # ==========================================
    # 3. TOOL EXECUTION
    # ==========================================

    tool_response = execute_tool(
        route=route,
        tool=tool,
        query=query,
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        top_k=top_k,
        threshold=threshold,
    )

    # ==========================================
    # 4. DECISION TRACE
    # ==========================================

    trace = create_trace(
        query=query,
        route=route,
        tool=tool,
        tool_response=tool_response,
        guardrail=guardrail,
    )

    # ==========================================
    # 5. JSONL LOG
    # ==========================================

    save_trace(
        trace
    )

    # ==========================================
    # 6. RESPONSE
    # ==========================================

    return {
        "route": route.value,
        "selected_tool": tool.value,
        "status": tool_response[
            "status"
        ],
        "message": tool_response[
            "message"
        ],
        "result": tool_response.get(
            "result"
        ),
        "results": tool_response.get(
            "results",
            [],
        ),
        "trace": trace,
    }