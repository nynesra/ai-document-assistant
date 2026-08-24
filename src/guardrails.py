import re
import unicodedata
from enum import Enum


MAX_QUERY_LENGTH = 500


class GuardrailReason(str, Enum):
    ALLOWED = "allowed"
    TOO_LONG = "too_long"
    PROMPT_INJECTION = "prompt_injection"
    CONTROL_CHARACTER = "control_character"


PROMPT_INJECTION_PATTERNS = [

    # ==========================================
    # TÜRKÇE - TALİMAT / KURAL AŞMA
    # ==========================================

    (
        r"önceki\s+"
        r"(?:talimatlari|kurallari|yönergeleri)\s+"
        r"(?:görmezden\s+gel|yok\s+say)"
    ),

    r"sistem\s+talimatlarini\s+unut",

    r"kurallari\s+yok\s+say",

    # ==========================================
    # TÜRKÇE - SİSTEM PROMPTU / MESAJI
    # ==========================================

    r"sistem\s+mesajini\s+göster",

    r"sistem\s+promptunu\s+göster",

    # ==========================================
    # İNGİLİZCE - TALİMAT AŞMA
    # ==========================================

    (
        r"ignore\s+"
        r"(?:previous|prior)\s+"
        r"instructions"
    ),

    (
        r"disregard\s+"
        r"(?:previous|prior)\s+"
        r"instructions"
    ),

    # ==========================================
    # İNGİLİZCE - SYSTEM PROMPT
    # ==========================================

    r"reveal\s+the\s+system\s+prompt",

    r"show\s+the\s+system\s+prompt",
]


def normalize_guardrail_text(
    query: str,
) -> str:
    """
    Guardrail karşılaştırmalarından önce metni
    Unicode, büyük/küçük harf ve Türkçe karakter
    farklılıklarına karşı normalize eder.
    """

    normalized = unicodedata.normalize(
        "NFKC",
        query,
    )

    # Unicode uyumlu küçük harf dönüşümü.
    # İngilizce "Ignore" gibi kelimeleri bozmaz.
    normalized = normalized.casefold()

    # Büyük Türkçe İ dönüşümünden oluşabilen
    # combining dot karakterini kaldır.
    normalized = normalized.replace(
        "\u0307",
        "",
    )

    # Guardrail karşılaştırmalarında i / ı
    # varyasyonlarını tek biçime indir.
    normalized = normalized.replace(
        "ı",
        "i",
    )

    # Fazla boşluk, tab ve satır sonlarını
    # tek boşluğa dönüştür.
    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    return normalized.strip()


def contains_control_characters(
    query: str,
) -> bool:
    """
    Normal satır sonu ve tab karakterleri dışında
    kontrol karakteri bulunup bulunmadığını
    kontrol eder.
    """

    for char in query:
        code = ord(char)

        if code < 32 and char not in (
            "\n",
            "\r",
            "\t",
        ):
            return True

    return False


def contains_prompt_injection(
    query: str,
) -> bool:
    """
    Açık talimat aşma girişimlerini kontrollü
    pattern eşleşmesiyle kontrol eder.
    """

    normalized = normalize_guardrail_text(
        query
    )

    for pattern in PROMPT_INJECTION_PATTERNS:

        if re.search(
            pattern,
            normalized,
        ):
            return True

    return False


def check_input_guardrails(
    query: str,
) -> dict:
    """
    Kullanıcı sorgusunu routing işleminden önce
    temel güvenlik kontrollerinden geçirir.
    """

    # ==========================================
    # QUERY LENGTH
    # ==========================================

    if len(query) > MAX_QUERY_LENGTH:

        return {
            "allowed": False,
            "reason": (
                GuardrailReason
                .TOO_LONG
                .value
            ),
            "message": (
                "Sorgu izin verilen maksimum "
                "uzunluğu aşmaktadır."
            ),
        }

    # ==========================================
    # CONTROL CHARACTER
    # ==========================================

    if contains_control_characters(
        query
    ):

        return {
            "allowed": False,
            "reason": (
                GuardrailReason
                .CONTROL_CHARACTER
                .value
            ),
            "message": (
                "Sorguda desteklenmeyen "
                "kontrol karakterleri bulundu."
            ),
        }

    # ==========================================
    # PROMPT INJECTION
    # ==========================================

    if contains_prompt_injection(
        query
    ):

        return {
            "allowed": False,
            "reason": (
                GuardrailReason
                .PROMPT_INJECTION
                .value
            ),
            "message": (
                "Sistem talimatlarını değiştirmeye "
                "yönelik bir girişim algılandı."
            ),
        }

    # ==========================================
    # ALLOWED
    # ==========================================

    return {
        "allowed": True,
        "reason": (
            GuardrailReason
            .ALLOWED
            .value
        ),
        "message": (
            "Input guardrail kontrolü başarılı."
        ),
    }