import json
from pathlib import Path


EVAL_SET_PATH = Path(
    "evaluation/eval_set.json"
)


EXPECTED_TOTAL = 20


VALID_CATEGORIES = {
    "retrieval",
    "calculator",
    "out_of_scope",
    "invalid",
    "guardrail",
}


CATEGORY_PREFIXES = {
    "retrieval": "R",
    "calculator": "C",
    "out_of_scope": "O",
    "invalid": "I",
    "guardrail": "G",
}


BASE_REQUIRED_FIELDS = {
    "id",
    "category",
    "query",
    "expected_route",
    "expected_tool",
    "expected_status",
}


def load_eval_set():
    """
    JSON evaluation set dosyasını yükler.
    """

    if not EVAL_SET_PATH.exists():
        raise FileNotFoundError(
            f"Evaluation set bulunamadı: "
            f"{EVAL_SET_PATH}"
        )

    with EVAL_SET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def validate_total_count(
    eval_set,
    errors,
):
    """
    Evaluation set toplam kayıt sayısını kontrol eder.
    """

    if len(eval_set) != EXPECTED_TOTAL:
        errors.append(
            (
                "Toplam kayıt sayısı hatalı: "
                f"{len(eval_set)} "
                f"(beklenen {EXPECTED_TOTAL})"
            )
        )


def validate_unique_ids(
    eval_set,
    errors,
):
    """
    ID tekrarlarını kontrol eder.
    """

    ids = [
        item.get("id")
        for item in eval_set
    ]

    if len(ids) != len(set(ids)):
        errors.append(
            "Tekrarlanan ID bulundu."
        )


def validate_duplicate_queries(
    eval_set,
    errors,
):
    """
    Aynı sorgunun birden fazla kez
    kullanılıp kullanılmadığını kontrol eder.
    """

    normalized_queries = [
        item.get(
            "query",
            "",
        ).strip().casefold()
        for item in eval_set
    ]

    if (
        len(normalized_queries)
        != len(set(normalized_queries))
    ):
        errors.append(
            "Tekrarlanan sorgu bulundu."
        )


def validate_required_fields(
    eval_set,
    errors,
):
    """
    Her kayıt için zorunlu alanları kontrol eder.
    """

    for item in eval_set:

        item_id = item.get(
            "id",
            "UNKNOWN",
        )

        missing_fields = (
            BASE_REQUIRED_FIELDS
            - set(item.keys())
        )

        if missing_fields:
            errors.append(
                (
                    f"{item_id}: "
                    "Eksik zorunlu alanlar: "
                    f"{sorted(missing_fields)}"
                )
            )


def validate_categories(
    eval_set,
    errors,
):
    """
    Kategori değerlerinin izin verilen
    kategorilerden biri olup olmadığını kontrol eder.
    """

    for item in eval_set:

        item_id = item.get(
            "id",
            "UNKNOWN",
        )

        category = item.get(
            "category"
        )

        if category not in VALID_CATEGORIES:
            errors.append(
                (
                    f"{item_id}: "
                    f"Geçersiz kategori: {category}"
                )
            )


def validate_id_prefixes(
    eval_set,
    errors,
):
    """
    ID prefix'inin kategori ile uyumlu
    olup olmadığını kontrol eder.

    Örnek:
    retrieval -> R01
    calculator -> C01
    """

    for item in eval_set:

        item_id = item.get(
            "id",
            "",
        )

        category = item.get(
            "category"
        )

        expected_prefix = (
            CATEGORY_PREFIXES.get(
                category
            )
        )

        if (
            expected_prefix is not None
            and not item_id.startswith(
                expected_prefix
            )
        ):
            errors.append(
                (
                    f"{item_id}: "
                    "Kategori-ID prefix uyumsuzluğu. "
                    f"Kategori: {category}, "
                    f"beklenen prefix: "
                    f"{expected_prefix}"
                )
            )


def validate_category_specific_fields(
    eval_set,
    errors,
):
    """
    Kategoriye özel zorunlu alanları kontrol eder.
    """

    for item in eval_set:

        item_id = item.get(
            "id",
            "UNKNOWN",
        )

        category = item.get(
            "category"
        )

        # ======================================
        # RETRIEVAL
        # ======================================

        if category == "retrieval":

            expected_sources = item.get(
                "expected_sources"
            )

            if (
                not isinstance(
                    expected_sources,
                    list,
                )
                or len(expected_sources) == 0
            ):
                errors.append(
                    (
                        f"{item_id}: "
                        "Retrieval kaydında "
                        "expected_sources eksik "
                        "veya boş."
                    )
                )

        # ======================================
        # CALCULATOR
        # ======================================

        elif category == "calculator":

            if (
                "expected_result"
                not in item
            ):
                errors.append(
                    (
                        f"{item_id}: "
                        "Calculator kaydında "
                        "expected_result eksik."
                    )
                )

        # ======================================
        # GUARDRAIL
        # ======================================

        elif category == "guardrail":

            if (
                "expected_guardrail_reason"
                not in item
            ):
                errors.append(
                    (
                        f"{item_id}: "
                        "Guardrail kaydında "
                        "expected_guardrail_reason "
                        "eksik."
                    )
                )


def validate_expected_routes(
    eval_set,
    errors,
):
    """
    Kategori ile beklenen route arasındaki
    temel uyumu kontrol eder.
    """

    expected_routes = {
        "retrieval": "retrieval",
        "calculator": "calculator",
        "out_of_scope": "out_of_scope",
        "invalid": "invalid",
        "guardrail": "blocked",
    }

    for item in eval_set:

        item_id = item.get(
            "id",
            "UNKNOWN",
        )

        category = item.get(
            "category"
        )

        actual_route = item.get(
            "expected_route"
        )

        expected_route = (
            expected_routes.get(
                category
            )
        )

        if (
            expected_route is not None
            and actual_route
            != expected_route
        ):
            errors.append(
                (
                    f"{item_id}: "
                    "Kategori-route uyumsuzluğu. "
                    f"Beklenen: {expected_route}, "
                    f"bulunan: {actual_route}"
                )
            )


def validate_eval_set(
    eval_set,
):
    """
    Bütün validation kontrollerini çalıştırır.
    """

    errors = []

    validate_total_count(
        eval_set,
        errors,
    )

    validate_unique_ids(
        eval_set,
        errors,
    )

    validate_duplicate_queries(
        eval_set,
        errors,
    )

    validate_required_fields(
        eval_set,
        errors,
    )

    validate_categories(
        eval_set,
        errors,
    )

    validate_id_prefixes(
        eval_set,
        errors,
    )

    validate_category_specific_fields(
        eval_set,
        errors,
    )

    validate_expected_routes(
        eval_set,
        errors,
    )

    return errors


def print_summary(
    eval_set,
    errors,
):
    """
    Validation sonucunu terminale yazdırır.
    """

    print(
        "\n--- 16. GÜN EVALUATION SET VALIDATION ---"
    )

    print(
        "Toplam kayıt:",
        len(eval_set),
    )

    print(
        "Validation hata sayısı:",
        len(errors),
    )

    if errors:

        print(
            "\n--- VALIDATION HATALARI ---"
        )

        for error in errors:
            print(
                "-",
                error,
            )

    else:

        print(
            "Sonuç: Evaluation set geçerli."
        )


def main():

    eval_set = load_eval_set()

    errors = validate_eval_set(
        eval_set
    )

    print_summary(
        eval_set,
        errors,
    )


if __name__ == "__main__":
    main()