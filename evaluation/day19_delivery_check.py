import json
from pathlib import Path


PROJECT_ROOT = Path(".")


REQUIRED_DIRECTORIES = [
    "data",
    "src",
    "tests",
    "evaluation",
    "docs",
    "logs",
]


REQUIRED_FILES = [
    # ==========================================
    # PROJE / UI
    # ==========================================
    "README.md",
    "ui_app.py",

    # ==========================================
    # CORE
    # ==========================================
    "src/document_loader.py",
    "src/chunker.py",
    "src/retriever.py",
    "src/query_router.py",
    "src/calculator_tool.py",
    "src/decision_flow.py",
    "src/tool_registry.py",
    "src/tool_executor.py",
    "src/controlled_flow.py",
    "src/guardrails.py",
    "src/trace_logger.py",
    "src/ui_helpers.py",

    # ==========================================
    # EVALUATION
    # ==========================================
    "evaluation/eval_set.json",
    "evaluation/day17_eval_results.json",

    # ==========================================
    # DOKÜMANTASYON
    # ==========================================
    "docs/day10_threshold_experiments.md",
    "docs/day11_embedding_retrieval.md",
    "docs/day13_decision_flow.md",
    "docs/day14_controlled_tool_calls.md",
    "docs/day15_guardrails.md",
    "docs/day16_evaluation_set.md",
    "docs/day17_gold_evaluation.md",
    "docs/day18_ui_logging.md",
]


def check_directories():
    """
    Zorunlu proje klasörlerinin varlığını kontrol eder.
    """

    results = []

    for directory in REQUIRED_DIRECTORIES:

        path = PROJECT_ROOT / directory

        results.append({
            "path": directory,
            "exists": path.is_dir(),
        })

    return results


def check_files():
    """
    Zorunlu proje dosyalarının varlığını kontrol eder.
    """

    results = []

    for file_path in REQUIRED_FILES:

        path = PROJECT_ROOT / file_path

        results.append({
            "path": file_path,
            "exists": path.is_file(),
        })

    return results


def count_knowledge_base_documents():
    """
    data klasöründeki Markdown ve TXT
    dokümanlarının sayısını hesaplar.
    """

    data_path = PROJECT_ROOT / "data"

    markdown_files = list(
        data_path.glob("*.md")
    )

    text_files = list(
        data_path.glob("*.txt")
    )

    documents = (
        markdown_files
        + text_files
    )

    return {
        "count": len(documents),
        "documents": sorted(
            [
                file.name
                for file in documents
            ]
        ),
        "target_min": 10,
        "target_max": 20,
        "within_target": (
            10 <= len(documents) <= 20
        ),
    }


def check_readme():
    """
    README dosyasının var ve boş olmayan
    bir dosya olduğunu kontrol eder.
    """

    path = PROJECT_ROOT / "README.md"

    exists = path.is_file()

    size = (
        path.stat().st_size
        if exists
        else 0
    )

    return {
        "exists": exists,
        "size_bytes": size,
        "non_empty": (
            exists
            and size > 0
        ),
    }


def check_eval_set():
    """
    Gold Evaluation Set'in okunabilir olduğunu
    ve 20 kayıt içerdiğini kontrol eder.
    """

    path = (
        PROJECT_ROOT
        / "evaluation"
        / "eval_set.json"
    )

    if not path.is_file():

        return {
            "exists": False,
            "readable": False,
            "count": 0,
            "expected_count": 20,
            "valid_count": False,
        }

    try:

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

    except (
        json.JSONDecodeError,
        OSError,
    ):

        return {
            "exists": True,
            "readable": False,
            "count": 0,
            "expected_count": 20,
            "valid_count": False,
        }

    count = len(data)

    return {
        "exists": True,
        "readable": True,
        "count": count,
        "expected_count": 20,
        "valid_count": (
            count == 20
        ),
    }


def check_eval_results():
    """
    17. gün evaluation sonuç dosyasının
    temel metriklerini kontrol eder.
    """

    path = (
        PROJECT_ROOT
        / "evaluation"
        / "day17_eval_results.json"
    )

    if not path.is_file():

        return {
            "exists": False,
            "readable": False,
        }

    try:

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

    except (
        json.JSONDecodeError,
        OSError,
    ):

        return {
            "exists": True,
            "readable": False,
        }

    general_metrics = data.get(
        "general_metrics",
        {},
    )

    return {
        "exists": True,
        "readable": True,
        "total_queries": data.get(
            "total_queries"
        ),
        "end_to_end_accuracy": (
            general_metrics.get(
                "end_to_end_accuracy"
            )
        ),
        "error_count": len(
            data.get(
                "errors",
                [],
            )
        ),
    }


def count_test_files():
    """
    tests klasöründeki pytest dosyalarını sayar.
    """

    tests_path = PROJECT_ROOT / "tests"

    test_files = sorted(
        tests_path.glob(
            "test_*.py"
        )
    )

    return {
        "count": len(test_files),
        "files": [
            file.name
            for file in test_files
        ],
        "has_tests": (
            len(test_files) > 0
        ),
    }


def build_delivery_report():

    directories = check_directories()
    files = check_files()

    kb_documents = (
        count_knowledge_base_documents()
    )

    readme = check_readme()

    eval_set = check_eval_set()

    eval_results = (
        check_eval_results()
    )

    tests = count_test_files()

    missing_directories = [
        item["path"]
        for item in directories
        if not item["exists"]
    ]

    missing_files = [
        item["path"]
        for item in files
        if not item["exists"]
    ]

    critical_ok = (
        len(missing_directories) == 0
        and len(missing_files) == 0
        and readme["non_empty"]
        and eval_set["valid_count"]
        and eval_results.get(
            "readable",
            False,
        )
        and tests["has_tests"]
    )

    return {
        "directories": directories,
        "files": files,
        "missing_directories":
            missing_directories,
        "missing_files":
            missing_files,
        "knowledge_base":
            kb_documents,
        "readme":
            readme,
        "eval_set":
            eval_set,
        "eval_results":
            eval_results,
        "tests":
            tests,
        "critical_delivery_ready":
            critical_ok,
    }


def save_report(
    report,
):
    """
    Teslim kontrol sonucunu JSON olarak kaydeder.
    """

    output_path = (
        PROJECT_ROOT
        / "evaluation"
        / "day19_delivery_check.json"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_path


def print_report(
    report,
    output_path,
):

    print(
        "\n--- 19. GÜN TESLİM KONTROLÜ ---"
    )

    print(
        "\nZorunlu klasör:"
    )

    print(
        f"{len(REQUIRED_DIRECTORIES)} "
        f"/ {len(REQUIRED_DIRECTORIES)} kontrol edildi."
    )

    print(
        "Eksik klasör:",
        len(
            report[
                "missing_directories"
            ]
        ),
    )

    print(
        "\nZorunlu dosya:"
    )

    print(
        f"{len(REQUIRED_FILES)} "
        f"/ {len(REQUIRED_FILES)} kontrol edildi."
    )

    print(
        "Eksik dosya:",
        len(
            report[
                "missing_files"
            ]
        ),
    )

    print(
        "\nREADME:"
    )

    print(
        "Dosya:",
        report[
            "readme"
        ][
            "exists"
        ],
    )

    print(
        "Boş değil:",
        report[
            "readme"
        ][
            "non_empty"
        ],
    )

    print(
        "\nBilgi tabanı:"
    )

    print(
        "Doküman sayısı:",
        report[
            "knowledge_base"
        ][
            "count"
        ],
    )

    print(
        "Hedef aralıkta (10-20):",
        report[
            "knowledge_base"
        ][
            "within_target"
        ],
    )

    print(
        "\nGold Evaluation Set:"
    )

    print(
        "Kayıt:",
        report[
            "eval_set"
        ][
            "count"
        ],
    )

    print(
        "20 kayıt doğru:",
        report[
            "eval_set"
        ][
            "valid_count"
        ],
    )

    print(
        "\nEvaluation Results:"
    )

    print(
        "Toplam sorgu:",
        report[
            "eval_results"
        ].get(
            "total_queries"
        ),
    )

    print(
        "End-to-End Accuracy:",
        report[
            "eval_results"
        ].get(
            "end_to_end_accuracy"
        ),
    )

    print(
        "Hata sayısı:",
        report[
            "eval_results"
        ].get(
            "error_count"
        ),
    )

    print(
        "\nTest dosyası sayısı:",
        report[
            "tests"
        ][
            "count"
        ],
    )

    print(
        "\n--- TESLİM DURUMU ---"
    )

    print(
        "Kritik bileşenler hazır:",
        report[
            "critical_delivery_ready"
        ],
    )

    if report[
        "missing_directories"
    ]:

        print(
            "\nEksik klasörler:"
        )

        for item in report[
            "missing_directories"
        ]:
            print(
                "-",
                item,
            )

    if report[
        "missing_files"
    ]:

        print(
            "\nEksik dosyalar:"
        )

        for item in report[
            "missing_files"
        ]:
            print(
                "-",
                item,
            )

    if not report[
        "knowledge_base"
    ][
        "within_target"
    ]:

        print(
            "\nUYARI:"
        )

        print(
            "Bilgi tabanındaki doküman "
            "sayısı 10-20 hedef aralığında değil."
        )

    print(
        "\nSonuç dosyası:",
        output_path,
    )


def main():

    report = build_delivery_report()

    output_path = save_report(
        report
    )

    print_report(
        report,
        output_path,
    )


if __name__ == "__main__":
    main()