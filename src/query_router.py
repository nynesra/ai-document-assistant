import re
from enum import Enum


class QueryRoute(str, Enum):
    INVALID = "invalid"
    CALCULATOR = "calculator"
    RETRIEVAL = "retrieval"
    OUT_OF_SCOPE = "out_of_scope"

KB_KEYWORDS = {
    "python",
    "fastapi",
    "git",
    "repository",
    "repo",
    "sanal ortam",
    "venv",
    "log",
    "loglama",
    "servis",
    "api",
    "veri temizleme",
    "model",
}

def is_knowledge_base_query(query: str) -> bool:
    """
    Sorgunun mevcut teknik doküman bilgi
    tabanının kapsamıyla ilişkili olup
    olmadığını basit ve kontrollü biçimde
    değerlendirir.
    """

    normalized = query.lower().strip()

    return any(
        keyword in normalized
        for keyword in KB_KEYWORDS
    )

def is_valid_query(query: str) -> bool:
    """
    Sorgunun gerçekten anlamlı bir karakter
    içerip içermediğini kontrol eder.
    """

    if not query:
        return False

    query = query.strip()

    if not query:
        return False

    # En az bir harf veya rakam bulunmalı.
    return bool(
        re.search(
            r"[A-Za-zÇĞİÖŞÜçğıöşü0-9]",
            query,
        )
    )


def extract_math_expression(query: str):
    """
    Basit matematiksel sorgulardan
    işlem ifadesini çıkarmaya çalışır.

    Örnek:
    '5 + 5 kaç?' -> '5 + 5'
    '3 x 7 kaç?' -> '3 * 7'
    '20 bölü 4 kaç?' -> '20 / 4'
    """

    normalized = query.lower().strip()

    # -----------------------------------------
    # Farklı matematik gösterimlerini
    # standart operatörlere dönüştür.
    # -----------------------------------------

    normalized = re.sub(
        r"\bx\b",
        "*",
        normalized,
    )

    normalized = re.sub(
        r"\bbölü\b",
        "/",
        normalized,
    )

    # -----------------------------------------
    # Soru kelimelerini kaldır.
    # -----------------------------------------

    removable_words = [
        "kaçtır",
        "kaç",
        "nedir",
        "hesapla",
        "sonucu",
        "sonuç",
    ]

    for word in removable_words:
        normalized = normalized.replace(
            word,
            "",
        )

    normalized = normalized.replace(
        "?",
        "",
    )

    normalized = normalized.strip()

    if not normalized:
        return None

    # Sadece sayı ve izin verilen matematik
    # karakterlerinden oluşuyorsa calculator.
    if re.fullmatch(
        r"[0-9\s\+\-\*\/\(\)\.,]+",
        normalized,
    ):
        return normalized

    return None


def route_query(query: str) -> QueryRoute:
    """
    Kullanıcı sorgusunun hangi işlem
    tarafından ele alınacağını belirler.
    """

    if not is_valid_query(query):
        return QueryRoute.INVALID

    math_expression = extract_math_expression(
        query
    )

    if math_expression is not None:
        return QueryRoute.CALCULATOR

    if is_knowledge_base_query(query):
        return QueryRoute.RETRIEVAL

    return QueryRoute.OUT_OF_SCOPE