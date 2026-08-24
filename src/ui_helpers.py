def get_ui_result_type(
    response: dict,
) -> str:
    """
    Controlled Flow sonucunun UI üzerinde
    hangi tür mesajla gösterileceğini belirler.
    """

    route = response.get("route")
    status = response.get("status")

    if (
        route == "calculator"
        and status == "success"
    ):
        return "calculator_success"

    if (
        route == "retrieval"
        and status == "success"
    ):
        return "retrieval_success"

    if (
        route == "retrieval"
        and status == "insufficient_source"
    ):
        return "insufficient_source"

    if route == "out_of_scope":
        return "out_of_scope"

    if route == "invalid":
        return "invalid"

    if status == "guardrail_blocked":
        return "guardrail_blocked"

    return "error"


def get_recent_traces(
    traces: list,
    limit: int = 5,
) -> list:
    """
    UI üzerinde gösterilecek en son
    decision trace kayıtlarını döndürür.

    En yeni kayıt ilk sırada olacak
    şekilde sonuç üretir.
    """

    if limit <= 0:
        raise ValueError(
            "Log limiti sıfırdan büyük olmalıdır."
        )

    recent = traces[-limit:]

    return list(
        reversed(recent)
    )