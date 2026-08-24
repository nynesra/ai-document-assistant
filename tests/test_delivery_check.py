from evaluation.day19_delivery_check import (
    build_delivery_report,
)


def test_required_directories_exist():
    """
    Teslim için gerekli bütün temel
    klasörler mevcut olmalıdır.
    """

    report = build_delivery_report()

    assert (
        report["missing_directories"]
        == []
    )


def test_required_files_exist():
    """
    Teslim için gerekli bütün kritik
    dosyalar mevcut olmalıdır.
    """

    report = build_delivery_report()

    assert (
        report["missing_files"]
        == []
    )


def test_knowledge_base_document_count():
    """
    Case kapsamında bilgi tabanında
    10-20 teknik doküman bulunmalıdır.
    """

    report = build_delivery_report()

    knowledge_base = report[
        "knowledge_base"
    ]

    assert (
        knowledge_base["count"]
        >= 10
    )

    assert (
        knowledge_base["count"]
        <= 20
    )

    assert (
        knowledge_base[
            "within_target"
        ]
        is True
    )


def test_gold_eval_delivery_data():
    """
    Gold Evaluation Set 20 kayıt içermeli
    ve sonuç dosyası okunabilir olmalıdır.
    """

    report = build_delivery_report()

    assert (
        report["eval_set"][
            "valid_count"
        ]
        is True
    )

    assert (
        report["eval_set"]["count"]
        == 20
    )

    assert (
        report["eval_results"][
            "readable"
        ]
        is True
    )

    assert (
        report["eval_results"][
            "total_queries"
        ]
        == 20
    )

    assert (
        report["eval_results"][
            "error_count"
        ]
        == 0
    )


def test_project_is_delivery_ready():
    """
    Bütün kritik teslim koşullarının
    birlikte sağlanması gerekir.
    """

    report = build_delivery_report()

    assert (
        report[
            "critical_delivery_ready"
        ]
        is True
    )
    