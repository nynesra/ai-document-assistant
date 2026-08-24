from pathlib import Path#Dosya ve klasör yollarıyla çalışmayı kolaylaştırır.
from typing import TypedDict

from src.text_cleaner import clean_text


SUPPORTED_EXTENSIONS = {".md", ".txt"}#sistem sadece bu uzantılara sahip dosyaları kabul edecek.


class Document(TypedDict):
    """Yüklenen bir teknik dokümanın yapısını tanımlar."""

    source: str
    extension: str
    raw_text: str
    cleaned_text: str
    raw_char_count: int
    cleaned_char_count: int
    cleaning_ratio: float


def calculate_cleaning_ratio( #temizleme işleminin metni ne kadar değiştirdiği ölçülür.
    raw_char_count: int,
    cleaned_char_count: int,
) -> float:
    """Metin temizleme işleminin yüzde olarak etkisini hesaplar."""

    if raw_char_count == 0: #bu blok önemli çünkü ham metnin uzunlıuğu sıfır olursa sıfıra bölme tanımsızlığı ortaya çıkar.        return 0.0
        return 0.0
    removed_char_count = raw_char_count - cleaned_char_count

    ratio = (
        removed_char_count
        / raw_char_count
    ) * 100

    return ratio


def load_document( #bu fonksiyon tek bir dosyayı işler.
    file_path: Path,
) -> Document | None:
    """Tek bir Markdown veya TXT dosyasını okur ve temizler."""

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS: #dosyanın uzantısı uygun mu değil mi bakar.(.md, .txt)
        return None

    raw_text = file_path.read_text(
        encoding="utf-8"
    )

    cleaned_text = clean_text(raw_text)#text_cleaner.py çalıştırır.burada document_loader ve text_cleaner birbirine bağlandı.

    if not cleaned_text: #boş doküman kontrolü.
        return None

    raw_char_count = len(raw_text)#ham metin karakter sayısı
    cleaned_char_count = len(cleaned_text)#temzi metin karakter sayısı.

    cleaning_ratio = calculate_cleaning_ratio(
        raw_char_count=raw_char_count,
        cleaned_char_count=cleaned_char_count,
    )

    document: Document = {
        "source": file_path.name,
        "extension": file_path.suffix.lower(),
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "raw_char_count": raw_char_count,
        "cleaned_char_count": cleaned_char_count,
        "cleaning_ratio": cleaning_ratio,
    }

    return document


def load_documents(
    data_directory: str = "data",
) -> list[Document]:
    """Verilen klasördeki desteklenen tüm dokümanları yükler."""

    directory = Path(data_directory)

    if not directory.exists():
        raise FileNotFoundError(
            f"Veri klasörü bulunamadı: {data_directory}"
        )

    if not directory.is_dir():#verilen yol klasör mü değil mi kontrol.
        raise NotADirectoryError(
            f"Belirtilen yol bir klasör değil: {data_directory}"
        )

    documents: list[Document] = []

    for file_path in sorted(directory.iterdir()):#data içindeki tğm elemanları tek tek gezer.

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:#desteklenmeyen dosyaları atlar
            continue

        try:
            document = load_document(file_path)

            if document is not None:
                documents.append(document)
            else:
                print(
                    f"Uyarı: Boş veya desteklenmeyen dosya atlandı: "
                    f"{file_path.name}"
                )

        except UnicodeDecodeError:
            print(
                f"Uyarı: UTF-8 olarak okunamayan dosya atlandı: "#Burası hata toleransı.
                f"{file_path.name}"
            )

    return documents


def print_document_summary(
    documents: list[Document],
) -> None:
    """Yüklenen dokümanların özet bilgilerini ekrana yazdırır."""

    if not documents:
        print("Yüklenecek geçerli doküman bulunamadı.")
        return

    print("\n--- DOKÜMAN YÜKLEME SONUÇLARI ---\n")

    for document in documents:

        print(f"Kaynak: {document['source']}")
        print(f"Dosya türü: {document['extension']}")
        print(
            f"Ham karakter sayısı: "
            f"{document['raw_char_count']}"
        )
        print(
            f"Temiz karakter sayısı: "
            f"{document['cleaned_char_count']}"
        )
        print(
            f"Temizleme oranı: "
            f"%{document['cleaning_ratio']:.2f}"
        )

        print("-" * 40)

    total_cleaned_characters = sum( #bütün dökümanların temiz karakter sayıları toplanır
        document["cleaned_char_count"]
        for document in documents
    )

    average_document_length = (#ortalama hesaplanır.
        total_cleaned_characters
        / len(documents)
    )

    print(
        f"\nToplam yüklenen doküman: "
        f"{len(documents)}"
    )

    print(
        f"Ortalama temiz doküman uzunluğu: "
        f"{average_document_length:.2f} karakter"
    )


def main() -> None:
    """Doküman yükleme modülünü test eder."""

    try:
        documents = load_documents("data")

        print_document_summary(documents)

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Hata: {error}")


if __name__ == "__main__":
    main()

    """
data/
   ↓
document_loader.py
   ↓
.md ve .txt dosyalarını bul
   ↓
UTF-8 ile oku
   ↓
text_cleaner.py
   ↓
Metni temizle
   ↓
Karakter sayılarını hesapla
   ↓
Temizleme oranını hesapla
   ↓
Document yapısına dönüştür
   ↓
Liste olarak döndür   bu kod bunu yapıyor.4. günde bilgi python kodunun içindeydi bu sayede gerçek dosyalar içinde.
KNOWLADGE_BASE = [...]"""
