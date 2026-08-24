from typing import TypedDict

from src.document_loader import Document


class Chunk(TypedDict):
    """Bir dokümandan oluşturulan metin parçasının yapısını tanımlar."""

    source: str
    section: str
    chunk_id: str
    chunk_index: int
    text: str
    start_char: int
    end_char: int

def find_section(
    text: str,
    start_char: int,
) -> str:
    """Chunk başlangıcına en yakın önceki Markdown başlığını bulur."""

    current_section = "Genel"

    current_position = 0

    for line in text.splitlines(keepends=True):
        stripped_line = line.strip()

        if stripped_line.startswith("#"):
            heading = stripped_line.lstrip("#").strip()

            if current_position <= start_char and heading:
                current_section = heading

        if current_position > start_char:
            break

        current_position += len(line)

    return current_section


def validate_chunk_parameters(
    chunk_size: int,
    overlap: int,
) -> None:
    """Chunk boyutu ve overlap değerlerinin geçerli olup olmadığını kontrol eder."""

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size sıfırdan büyük olmalıdır."
        )

    if overlap < 0:
        raise ValueError(
            "overlap negatif olamaz."
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap, chunk_size değerinden küçük olmalıdır."
        )


def calculate_step(
    chunk_size: int,
    overlap: int,
) -> int:
    """Chunklar arasındaki ilerleme miktarını hesaplar."""

    validate_chunk_parameters(
        chunk_size=chunk_size,
        overlap=overlap,
    )

    step = chunk_size - overlap

    return step


def chunk_document(
    source: str,
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[Chunk]:
    """Tek bir dokümanı overlap kullanarak chunklara ayırır."""

    validate_chunk_parameters(
        chunk_size=chunk_size,
        overlap=overlap,
    )

    if not text.strip():
        return []

    chunks: list[Chunk] = []

    step = calculate_step(
        chunk_size=chunk_size,
        overlap=overlap,
    )

    start = 0
    chunk_index = 0

    while start < len(text):
        end = min(
            start + chunk_size,
            len(text),
        )

        chunk_text = text[start:end].strip()

        if chunk_text:
            section = find_section(
                text=text,
                start_char=start,
            )
            
            chunk: Chunk = {
                "source": source,
                "section": section,
                "chunk_id": f"{source}_{chunk_index}",
                "chunk_index": chunk_index,
                "text": chunk_text,
                "start_char": start,
                "end_char": end,
            }

            chunks.append(chunk)

            chunk_index += 1

        if end == len(text):
            break

        start += step

    return chunks


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[Chunk]:
    """Birden fazla dokümanı chunklara ayırır."""

    validate_chunk_parameters(
        chunk_size=chunk_size,
        overlap=overlap,
    )

    all_chunks: list[Chunk] = []

    for document in documents:
        document_chunks = chunk_document(
            source=document["source"],
            text=document["cleaned_text"],
            chunk_size=chunk_size,
            overlap=overlap,
        )

        all_chunks.extend(document_chunks)

    return all_chunks