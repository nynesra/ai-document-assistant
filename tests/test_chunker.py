from src.chunker import (
    calculate_step,
    chunk_document,
    chunk_documents,
    validate_chunk_parameters,
)

from src.document_loader import load_documents


def test_calculate_step() -> None:
    """Chunklar arasındaki ilerleme miktarını test eder."""

    step = calculate_step(
        chunk_size=500,
        overlap=100,
    )

    assert step == 400


def test_standard_chunking() -> None:
    """1100 karakterlik metnin doğru chunklara ayrılmasını test eder."""

    text = "A" * 1100

    chunks = chunk_document(
        source="ornek.md",
        text=text,
        chunk_size=500,
        overlap=100,
    )

    assert len(chunks) == 3

    assert chunks[0]["start_char"] == 0
    assert chunks[0]["end_char"] == 500

    assert chunks[1]["start_char"] == 400
    assert chunks[1]["end_char"] == 900

    assert chunks[2]["start_char"] == 800
    assert chunks[2]["end_char"] == 1100


def test_overlap_amount() -> None:
    """İki ardışık chunk arasındaki overlap miktarını test eder."""

    text = "A" * 1100

    chunks = chunk_document(
        source="ornek.md",
        text=text,
        chunk_size=500,
        overlap=100,
    )

    first_end = chunks[0]["end_char"]
    second_start = chunks[1]["start_char"]

    actual_overlap = first_end - second_start

    assert actual_overlap == 100


def test_short_document() -> None:
    """Chunk boyutundan kısa dokümanın tek chunk olmasını test eder."""

    text = "A" * 300

    chunks = chunk_document(
        source="kisa.md",
        text=text,
        chunk_size=500,
        overlap=100,
    )

    assert len(chunks) == 1

    assert chunks[0]["start_char"] == 0
    assert chunks[0]["end_char"] == 300

    assert len(chunks[0]["text"]) == 300


def test_empty_text() -> None:
    """Boş metnin chunk oluşturmamasını test eder."""

    chunks = chunk_document(
        source="bos.md",
        text="",
        chunk_size=500,
        overlap=100,
    )

    assert chunks == []


def test_invalid_chunk_size() -> None:
    """Sıfır chunk_size değerinin hata üretmesini test eder."""

    try:
        validate_chunk_parameters(
            chunk_size=0,
            overlap=0,
        )

    except ValueError:
        return

    raise AssertionError(
        "chunk_size=0 için ValueError bekleniyordu."
    )


def test_negative_overlap() -> None:
    """Negatif overlap değerinin hata üretmesini test eder."""

    try:
        validate_chunk_parameters(
            chunk_size=500,
            overlap=-50,
        )

    except ValueError:
        return

    raise AssertionError(
        "Negatif overlap için ValueError bekleniyordu."
    )


def test_overlap_equal_chunk_size() -> None:
    """Overlap chunk_size değerine eşitse hata oluşmasını test eder."""

    try:
        validate_chunk_parameters(
            chunk_size=500,
            overlap=500,
        )

    except ValueError:
        return

    raise AssertionError(
        "overlap >= chunk_size için ValueError bekleniyordu."
    )


def test_chunk_metadata() -> None:
    """Chunk metadata bilgilerinin doğru tutulmasını test eder."""

    text = """# Servis Kurulumu

Bu bölüm servis kurulumu hakkında bilgi verir.

## Paketlerin Yüklenmesi

Paketler pip komutu kullanılarak yüklenir.
"""

    chunks = chunk_document(
        source="servis_kurulumu.md",
        text=text,
        chunk_size=80,
        overlap=20,
    )

    first_chunk = chunks[0]

    assert first_chunk["source"] == "servis_kurulumu.md"
    assert first_chunk["section"] == "Servis Kurulumu"
    assert first_chunk["chunk_id"] == "servis_kurulumu.md_0"
    assert first_chunk["chunk_index"] == 0
    assert first_chunk["start_char"] == 0


def test_real_documents() -> None:
    """Gerçek bilgi tabanındaki dokümanların chunklanmasını test eder."""

    documents = load_documents("data")

    chunks = chunk_documents(
        documents=documents,
        chunk_size=500,
        overlap=100,
    )

    assert len(documents) == 12
    assert len(chunks) == 37


def main() -> None:
    """Chunking modülüne ait testleri çalıştırır."""

    tests = [
        ("Step hesaplama testi", test_calculate_step),
        ("Standart chunking testi", test_standard_chunking),
        ("Overlap miktarı testi", test_overlap_amount),
        ("Kısa doküman testi", test_short_document),
        ("Boş metin testi", test_empty_text),
        ("Geçersiz chunk_size testi", test_invalid_chunk_size),
        ("Negatif overlap testi", test_negative_overlap),
        (
            "Overlap eşitlik testi",
            test_overlap_equal_chunk_size,
        ),
        ("Chunk metadata testi", test_chunk_metadata),
        ("Gerçek doküman chunk testi", test_real_documents),
    ]

    successful_tests = 0

    print("\n--- 6. GÜN CHUNKING TEST SONUÇLARI ---\n")

    for test_name, test_function in tests:
        try:
            test_function()

            successful_tests += 1

            print(f"[BAŞARILI] {test_name}")

        except AssertionError as error:
            print(
                f"[BAŞARISIZ] {test_name}: {error}"
            )

        except Exception as error:
            print(
                f"[HATA] {test_name}: "
                f"{type(error).__name__}: {error}"
            )

    total_tests = len(tests)

    success_rate = (
        successful_tests
        / total_tests
    ) * 100

    print("\n------------------------------------")

    print(f"Toplam test: {total_tests}")
    print(f"Başarılı test: {successful_tests}")

    print(
        f"Test başarı oranı: "
        f"%{success_rate:.2f}"
    )


if __name__ == "__main__":
    main()