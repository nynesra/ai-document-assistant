import ast
import math
import operator


ALLOWED_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_node(node):
    """
    AST düğümünü yalnızca izin verilen
    matematik işlemleriyle değerlendirir.
    """

    if isinstance(node, ast.Expression):
        return _evaluate_node(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            raise ValueError(
                "Boolean değerler desteklenmiyor."
            )

        if isinstance(
            node.value,
            (int, float),
        ):
            return node.value

        raise ValueError(
            "Yalnızca sayısal değerler kullanılabilir."
        )

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)

        if operator_type not in ALLOWED_BINARY_OPERATORS:
            raise ValueError(
                "Bu matematik işlemi desteklenmiyor."
            )

        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)

        operation = (
            ALLOWED_BINARY_OPERATORS[
                operator_type
            ]
        )

        try:
            return operation(
                left,
                right,
            )

        except ZeroDivisionError as exc:
            raise ValueError(
                "Sıfıra bölme işlemi yapılamaz."
            ) from exc

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)

        if operator_type not in ALLOWED_UNARY_OPERATORS:
            raise ValueError(
                "Bu tekli işlem desteklenmiyor."
            )

        operand = _evaluate_node(
            node.operand
        )

        operation = (
            ALLOWED_UNARY_OPERATORS[
                operator_type
            ]
        )

        return operation(operand)

    raise ValueError(
        "İfadede desteklenmeyen bir yapı bulundu."
    )


def calculate(expression: str):
    """
    Güvenli şekilde basit matematik
    ifadelerini hesaplar.

    Desteklenen işlemler:
    +  -  *  /
    """

    if not expression:
        raise ValueError(
            "Matematik ifadesi boş olamaz."
        )

    expression = expression.strip()

    if not expression:
        raise ValueError(
            "Matematik ifadesi boş olamaz."
        )

    if len(expression) > 200:
        raise ValueError(
            "Matematik ifadesi çok uzun."
        )

    # Türkçe kullanımda ondalık virgül
    # girilirse noktaya dönüştür.
    expression = expression.replace(
        ",",
        ".",
    )

    try:
        parsed_expression = ast.parse(
            expression,
            mode="eval",
        )

    except SyntaxError as exc:
        raise ValueError(
            "Geçersiz matematik ifadesi."
        ) from exc

    result = _evaluate_node(
        parsed_expression
    )

    if not isinstance(
        result,
        (int, float),
    ):
        raise ValueError(
            "Hesaplama sonucu sayısal değil."
        )

    if not math.isfinite(result):
        raise ValueError(
            "Geçersiz hesaplama sonucu."
        )

    return result