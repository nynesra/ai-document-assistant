import re


def clean_text(text: str) -> str:
    """Ham doküman metnindeki gereksiz boşlukları temizler."""

    if not text:
        return ""

    text = text.replace("\r\n", "\n")#Windows satır sonlarını standart hale getirir.
    text = text.replace("\r", "\n")#Mac satır sonlarını standart hale getirir.
    text = text.replace("\t", " ")#tab karakterlerini boşlukla değiştirir.

    text = re.sub(r"[ ]+", " ", text)#birden fazla boşluğu tek boşlukla değiştirir.
    text = re.sub(r"\n{3,}", "\n\n", text)#üç veya daha fazla ardışık satır sonunu iki satır sonuyla değiştirir.

    cleaned_text = text.strip()

    return cleaned_text