import re #regular expression yani düzenli ifade modülü.
from typing import TypedDict #typing modulünden TypedDict sınıfını içeri aktarır.


class KnowledgeItem(TypedDict):
    """Bilgi tabanındaki bir kaydın yapısını tanımlar."""
#Bilgi tabanındaki her kayıtta aşağıdaki alanların bulunmmasını sağlar.
    source: str
    keywords: list[str]
    answer: str


KNOWLEDGE_BASE: list[KnowledgeItem] = [  #KnowledgeItem adında bir bilgi tabanı oluşturuldu.
    {
        "source": "servis_kurulumu.md",
        "keywords": [
            "servis",
            "yerel",
            "yerelde",
            "çalıştırmak",
            "çalıştırılır",
            "başlatmak",
            "uygulama",
            "uygulamayı",
            "requirements",
            "paket",
        ],
        "answer": (
            "Uygulamayı yerelde çalıştırmadan önce gerekli Python "
            "paketleri requirements.txt dosyasından yüklenmelidir."
        ),
    },
    {
        "source": "model_degerlendirme.md",
        "keywords": [
            "model",
            "değerlendirme",
            "metrik",
            "metrikler",
            "accuracy",
            "precision",
            "recall",
            "f1",
            "sınıflandırma",
        ],
        "answer": (
            "Bir sınıflandırma modelinin değerlendirilmesinde accuracy, "
            "precision, recall ve F1-score metrikleri takip edilebilir."
        ),
    },
    {
        "source": "hata_cozumleri.md",
        "keywords": [
            "hata",
            "module",
            "modulenotfounderror",
            "paket",
            "bulunamadı",
            "çözüm",
            "kurulum",
        ],
        "answer": (
            "ModuleNotFoundError hatasında eksik Python paketinin "
            "kurulup kurulmadığı kontrol edilmelidir."
        ),
    },
]


STOP_WORDS = {
    "bir",
    "bu",
    "için",
    "ile",
    "ve",
    "veya",
    "nasıl",
    "nedir",
    "nelerdir",
    "hangi",
    "ne",
    "mı",
    "mi",
    "mu",
    "mü",
    "da",
    "de",
}


def tokenize(text: str) -> set[str]:
    """Metni temizler ve anlamlı kelimelerden oluşan bir kümeye dönüştürür."""

    normalized_text = text.casefold().replace("i̇", "i")

    words = re.findall(
        r"[a-zçğıöşü0-9]+",
        normalized_text,
    )

    meaningful_words = {#küme kullanıldığı için her kelime yalnızca bir kere alınır.
        word
        for word in words
        if word not in STOP_WORDS and len(word) > 1
    }

    return meaningful_words


def calculate_overlap_score(
    query_tokens: set[str],#kullanıcı sorusundan çıkarılmış kelimeler kümesi.
    keywords: list[str],#bilgi tabanındaki kayıtlardan çıkarılmış anahtar kelimeler listesi.
) -> float:
    """Soru kelimeleri ile anahtar kelimeler arasındaki eşleşme oranını hesaplar."""

    if not query_tokens:
        return 0.0

    keyword_set = set(keywords)

    common_words = query_tokens.intersection(keyword_set)

    score = len(common_words) / len(query_tokens)#eşleşme skorunu hesaplar.

    return score


def search_knowledge_base(#kullanıcı sorusuna en yakın bilgi tabanı kaydını bulur.
    query: str,
) -> tuple[KnowledgeItem | None, float]:#| işareti veya anlamına gelir.
    """Soruya en yakın bilgi tabanı kaydını bulur."""

    query_tokens = tokenize(query)

    best_item: KnowledgeItem | None = None
    best_score = 0.0

    for item in KNOWLEDGE_BASE:# bilgi tababnınıdaki tüm kayıtları sırayla dolaşır.
        score = calculate_overlap_score(
            query_tokens=query_tokens,
            keywords=item["keywords"],
        )

        if score > best_score:
            best_score = score
            best_item = item

    return best_item, best_score


def answer_question(
    query: str,
    threshold: float = 0.20,#eşik değeri parametresi, eşleşme skorunun bu değerin altında olması durumunda güvenli ret mesajı döndürülür.
) -> str:
    """Soruyu cevaplar veya yeterli bilgi yoksa güvenli ret mesajı verir."""

    if not query.strip():
        raise ValueError("Kullanıcı sorusu boş bırakılamaz.")

    item, score = search_knowledge_base(query)

    if item is None or score < threshold:
        return (
            "Bu soruyu cevaplamak için bilgi tabanında yeterli "
            "kaynak bulunamadı."
        )

    return (
        f"Cevap: {item['answer']}\n"
        f"Kaynak: {item['source']}\n"
        f"Basit eşleşme skoru: {score:.2f}"#ondalıklı sayının virgülden sonra iki basamakla gösterilmesini sağlar.
    )


def main() -> None:
    """Programın başlangıç fonksiyonudur."""

    question = input("Sorunuzu yazın: ").strip()#Terminal üzerinden kullanıcıdan soru alır.

    try:
        result = answer_question(question)

        print("\n--- SİSTEM SONUCU ---\n")
        print(result)

    except ValueError as error:
        print(f"Hata: {error}")


if __name__ == "__main__":
    main()