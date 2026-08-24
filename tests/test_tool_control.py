import pytest

from src.query_router import QueryRoute

from src.tool_registry import (
    ToolName,
    select_tool,
)

from src.tool_executor import execute_tool

from src.trace_logger import (
    save_trace,
    read_traces,
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
    Retriever testleri için TF-IDF indeksini
    yalnızca bir kez oluşturur.
    """

    return build_tfidf_index()


def test_calculator_route_selects_calculator():
    """
    Calculator route'u yalnızca
    Calculator Tool seçmelidir.
    """

    tool = select_tool(
        QueryRoute.CALCULATOR
    )

    assert tool == ToolName.CALCULATOR


def test_retrieval_route_selects_retriever():
    """
    Retrieval route'u Retriever Tool
    seçmelidir.
    """

    tool = select_tool(
        QueryRoute.RETRIEVAL
    )

    assert tool == ToolName.RETRIEVER


def test_non_tool_routes_select_none():
    """
    INVALID ve OUT_OF_SCOPE sorgularında
    hiçbir gerçek tool seçilmemelidir.
    """

    invalid_tool = select_tool(
        QueryRoute.INVALID
    )

    out_of_scope_tool = select_tool(
        QueryRoute.OUT_OF_SCOPE
    )

    assert invalid_tool == ToolName.NONE

    assert (
        out_of_scope_tool
        == ToolName.NONE
    )


def test_wrong_tool_call_is_blocked():
    """
    Calculator route'unda Retriever Tool
    zorla çağrılmaya çalışılırsa sistem
    işlemi engellemelidir.
    """

    response = execute_tool(
        route=QueryRoute.CALCULATOR,
        tool=ToolName.RETRIEVER,
        query="5 + 5 kaç?",
    )

    assert response["status"] == "blocked"

    assert response["tool"] == "retriever"

    assert response["result"] is None

    assert response["results"] == []


def test_calculator_tool_executes_successfully():
    """
    Doğru route ve doğru tool eşleşmesinde
    Calculator Tool çalışmalıdır.
    """

    response = execute_tool(
        route=QueryRoute.CALCULATOR,
        tool=ToolName.CALCULATOR,
        query="5 + 5 kaç?",
    )

    assert response["status"] == "success"

    assert response["tool"] == "calculator"

    assert response["result"] == 10

    assert response["results"] == []


def test_retriever_tool_executes_successfully(
    tfidf_index,
):
    """
    Doğru route ve Retriever Tool eşleşmesinde
    beklenen doküman kaynağı bulunmalıdır.
    """

    chunks, vectorizer, tfidf_matrix = (
        tfidf_index
    )

    response = execute_tool(
        route=QueryRoute.RETRIEVAL,
        tool=ToolName.RETRIEVER,
        query="Python nasıl kurulur?",
        chunks=chunks,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
    )

    assert response["status"] == "success"

    assert response["tool"] == "retriever"

    assert len(response["results"]) > 0

    assert (
        response["results"][0]["source"]
        == "python_kurulumu.md"
    )

    assert (
        response["results"][0]["score"]
        >= 0.20
    )


def test_trace_logger_round_trip(
    tmp_path,
):
    """
    Trace kaydı JSONL dosyasına yazılmalı
    ve aynı içerikle tekrar okunabilmelidir.
    """

    log_path = (
        tmp_path
        / "decision_trace.jsonl"
    )

    trace = {
        "timestamp": (
            "2026-08-21T10:00:00+00:00"
        ),
        "query": "5 + 5 kaç?",
        "route": "calculator",
        "selected_tool": "calculator",
        "tool_status": "success",
        "message": (
            "Calculator Tool başarıyla "
            "çalıştırıldı."
        ),
        "result": 10,
        "result_count": 0,
        "top_source": None,
        "top_score": None,
    }

    save_trace(
        trace=trace,
        log_path=log_path,
    )

    traces = read_traces(
        log_path=log_path
    )

    assert len(traces) == 1

    assert traces[0] == trace


def test_controlled_flow_creates_trace(
    monkeypatch,
):
    """
    Controlled Flow içerisinde route,
    tool ve sonuç bilgilerinin trace
    kaydına doğru aktarılması gerekir.
    """

    # Test sırasında gerçek logs klasörüne
    # kayıt yazılmasını engelle.
    monkeypatch.setattr(
        "src.controlled_flow.save_trace",
        lambda trace: None,
    )

    response = run_controlled_flow(
        "5 + 5 kaç?"
    )

    trace = response["trace"]

    assert trace["query"] == "5 + 5 kaç?"

    assert trace["route"] == "calculator"

    assert (
        trace["selected_tool"]
        == "calculator"
    )

    assert (
        trace["tool_status"]
        == "success"
    )

    assert trace["result"] == 10

    assert trace["result_count"] == 0

    assert trace["top_source"] is None

    assert trace["top_score"] is None