from enum import Enum

from src.query_router import QueryRoute


class ToolName(str, Enum):
    NONE = "none"
    CALCULATOR = "calculator"
    RETRIEVER = "retriever"


def select_tool(route: QueryRoute) -> ToolName:
    """
    Query Router tarafından verilen route'a göre
    kullanılmasına izin verilen aracı belirler.

    INVALID ve OUT_OF_SCOPE sorgularında
    hiçbir tool çalıştırılmaz.
    """

    if route == QueryRoute.CALCULATOR:
        return ToolName.CALCULATOR

    if route == QueryRoute.RETRIEVAL:
        return ToolName.RETRIEVER

    if route in (
        QueryRoute.INVALID,
        QueryRoute.OUT_OF_SCOPE,
    ):
        return ToolName.NONE

    raise ValueError(
        f"Desteklenmeyen route: {route}"
    )


def is_tool_allowed(
    route: QueryRoute,
    tool: ToolName,
) -> bool:
    """
    Verilen route için seçilen tool'un
    çalıştırılmasına izin verilip verilmediğini
    kontrol eder.
    """

    expected_tool = select_tool(route)

    return tool == expected_tool