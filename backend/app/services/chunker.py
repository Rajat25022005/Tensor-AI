"""Text chunking service — splits documents into overlapping segments."""

from dataclasses import dataclass, field
import hashlib


@dataclass
class TextChunker:
    """Splits text into overlapping chunks for embedding and storage."""

    chunk_size: int = 512
    chunk_overlap: int = 64
    separator: str = "\n\n"

    def chunk(self, text: str) -> list[dict]:
        """Split text into chunks with metadata.

        Returns a list of dicts with keys: id, text, index, char_start, char_end.
        """
        chunks = []
        start = 0
        index = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end]

            chunk_id = hashlib.sha256(f"{index}:{chunk_text[:50]}".encode()).hexdigest()[:16]
            chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "index": index,
                "char_start": start,
                "char_end": end,
            })

            start += self.chunk_size - self.chunk_overlap
            index += 1

        return chunks
