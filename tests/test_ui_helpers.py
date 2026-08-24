import pytest

from src.ui_helpers import (
    get_ui_result_type,
    get_recent_traces,
)


def test_calculator_ui_type():
    response = {
        "route": "calculator",
        "status": "success",
    }

    assert (
        get_ui_result_type(response)
        == "calculator_success"
    )


def test_retrieval_ui_type():
    response = {
        "route": "retrieval",
        "status": "success",
    }

    assert (
        get_ui_result_type(response)
        == "retrieval_success"
    )


def test_out_of_scope_ui_type():
    response = {
        "route": "out_of_scope",
        "status": "not_executed",
    }

    assert (
        get_ui_result_type(response)
        == "out_of_scope"
    )


def test_guardrail_ui_type():
    response = {
        "route": "blocked",
        "status": "guardrail_blocked",
    }

    assert (
        get_ui_result_type(response)
        == "guardrail_blocked"
    )


def test_recent_traces_returns_latest_first():
    traces = [
        {"query": "soru 1"},
        {"query": "soru 2"},
        {"query": "soru 3"},
        {"query": "soru 4"},
        {"query": "soru 5"},
        {"query": "soru 6"},
    ]

    recent = get_recent_traces(
        traces,
        limit=5,
    )

    assert len(recent) == 5

    assert (
        recent[0]["query"]
        == "soru 6"
    )

    assert (
        recent[-1]["query"]
        == "soru 2"
    )


def test_recent_trace_invalid_limit():
    with pytest.raises(ValueError):
        get_recent_traces(
            [],
            limit=0,
        )