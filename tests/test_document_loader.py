from pathlib import Path
import tempfile #testler için geçici dosya ve klasörler oluşturmak için kullanılır.test bitince otomatik temizler

from src.document_loader import (
    calculate_cleaning_ratio,
    load_document,
    load_documents,
)
from src.text_cleaner import clean_text


def test_clean_text() -> None:
    """Fazla boşlukların ve boş satırların temizlenmesini test eder."""

    raw_text = "Python     kurulumu\n\n\n\nçok     önemlidir."

    cleaned_text = clean_text(raw_text)

    expected_text = "Python kurulumu\n\nçok önemlidir."

    assert cleaned_text == expected_text


def test_cleaning_ratio() -> None:
    """Temizleme oranı hesabını test eder."""

    ratio = calculate_cleaning_ratio(
        raw_char_count=100,
        cleaned_char_count=90,
    )

    assert ratio == 10.0


def test_empty_raw_text_ratio() -> None:
    """Ham metin boş olduğunda sıfıra bölme yapılmamasını test eder."""

    ratio = calculate_cleaning_ratio(
        raw_char_count=0,
        cleaned_char_count=0,
    )

    assert ratio == 0.0


def test_markdown_document() -> None:
    """Gerçek bir Markdown dosyasının okunmasını test eder."""

    file_path = Path("data/python_kurulumu.md")

    document = load_document(file_path)

    assert document is not None
    assert document["source"] == "python_kurulumu.md"
    assert document["extension"] == ".md"
    assert document["cleaned_text"]

def test_txt_document() -> None:
    """TXT dosyasının UTF-8 olarak yüklenmesini test eder."""

    with tempfile.TemporaryDirectory() as temp_dir:#geçici bir klasör oluşturuyor
        file_path = Path(temp_dir) / "ornek.txt"

        file_path.write_text(
            "Türkçe karakterler: ç, ğ, ı, ö, ş, ü.",
            encoding="utf-8",
        )

        document = load_document(file_path)

        assert document is not None
        assert document["source"] == "ornek.txt"
        assert document["extension"] == ".txt"
        assert "Türkçe karakterler" in document["cleaned_text"]

def test_empty_document() -> None: #boş dosya testini yapar
    """Boş dokümanın sisteme alınmamasını test eder."""

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "bos_dosya.md"

        file_path.write_text(
            "",
            encoding="utf-8",
        )

        document = load_document(file_path)

        assert document is None   

def test_unsupported_extension() -> None:
    """Desteklenmeyen dosya türünün işleme alınmamasını test eder."""

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "ornek.pdf"

        file_path.write_text(
            "Bu dosya işleme alınmamalıdır.",
            encoding="utf-8",
        )

        document = load_document(file_path)

        assert document is None

def test_missing_directory() -> None:
    """Olmayan veri klasöründe açıklayıcı hata üretilmesini test eder."""

    with tempfile.TemporaryDirectory() as temp_dir:
        missing_directory = Path(temp_dir) / "olmayan_klasor"

        try:
            load_documents(str(missing_directory))

        except FileNotFoundError:
            return

        raise AssertionError(
            "Olmayan klasör için FileNotFoundError bekleniyordu."
        )


def test_load_all_documents() -> None:
    """Data klasöründeki teknik dokümanların yüklenmesini test eder."""

    documents = load_documents("data")

    assert len(documents) == 12


def main() -> None:
    tests = [
        ("Metin temizleme testi", test_clean_text),
        ("Temizleme oranı testi", test_cleaning_ratio),
        ("Sıfıra bölme kontrolü", test_empty_raw_text_ratio),
        ("Markdown yükleme testi", test_markdown_document),
        ("TXT yükleme testi", test_txt_document),
        ("Boş doküman testi", test_empty_document),
        ("Desteklenmeyen uzantı testi", test_unsupported_extension),
        ("Olmayan klasör testi", test_missing_directory),
        ("Tüm dokümanları yükleme testi", test_load_all_documents),
    ]

    successful_tests = 0

    print("\n--- 5. GÜN TEST SONUÇLARI ---\n")

    for test_name, test_function in tests:
        try:
            test_function()

            successful_tests += 1

            print(f"[BAŞARILI] {test_name}")

        except AssertionError:
            print(f"[BAŞARISIZ] {test_name}")

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

    print("\n------------------------------")

    print(f"Toplam test: {total_tests}")
    print(f"Başarılı test: {successful_tests}")

    print(
        f"Test başarı oranı: "
        f"%{success_rate:.2f}"
    )


if __name__ == "__main__":
    main()

