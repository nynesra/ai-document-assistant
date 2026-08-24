def build_prompt(question: str, context: str) -> str:
    """Kullanıcı sorusu ve bağlamdan kaynak kontrollü prompt oluşturur."""

    if not question.strip():
        raise ValueError("Kullanıcı sorusu boş bırakılamaz.")
    """strip() metnin başındaki ve sonundaki boşlukları kaldırır."""

    if not context.strip():
        context = "Bilgi tabanında ilgili bir içerik bulunamadı."

    prompt = f"""
ROL:
Sen teknik dokümanlara dayalı cevap veren bir AI Doküman Asistanısın.

GÖREV:
Kullanıcının sorusuna yalnızca verilen bağlamı kullanarak cevap ver.

BAĞLAM:
{context} #fonksiyona gönderilen döküman bilgisi.

KULLANICI SORUSU:
{question}

KURALLAR:
1. Bağlamda olmayan bilgileri üretme.
2. Kısa ve anlaşılır cevap ver.
3. Kullanılan kaynağı belirt.
4. Bağlam yetersizse kesin cevap verme.
5. Yeterli bilgi yoksa bilgi tabanında yeterli kaynak bulunmadığını söyle.

CEVAP:
""".strip()

    return prompt


def main() -> None:#fonksiyon bir değer döndürmez.işlemi gerçekleştirir ekrana yazdırır.
    sample_context = (
        "Kaynak: servis_kurulumu.md\n"
        "Uygulamayı çalıştırmadan önce gerekli Python paketleri "
        "requirements.txt dosyasından yüklenmelidir."
    )

    question = input("Sorunuzu yazın: ").strip()

    try:
        prompt = build_prompt( #daha önce tanımlanan build_prompt fonksiyonunu çağırır ve promptu oluşturur.
            question=question,
            context=sample_context
        )
        print("\n--- OLUŞTURULAN PROMPT ---\n")
        print(prompt)
    except ValueError as error:
        print(f"Hata: {error}")


if __name__ == "__main__":
    main()

"""bu program henüz yapay zekadan cevap almıyor.kullanıcı sorusunu ve
döküman balamını kullanarak modele göndereceğimiz promptu hazırlıyor."""
