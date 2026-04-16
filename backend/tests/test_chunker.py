"""Tests for the text chunker service."""

from app.services.chunker import TextChunker


def test_chunker_basic():
    """Chunker produces non-empty chunks from text."""
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    text = "A" * 250
    chunks = chunker.chunk(text)

    assert len(chunks) > 1
    assert all("text" in c for c in chunks)
    assert all("id" in c for c in chunks)


def test_chunker_short_text():
    """Single chunk for text shorter than chunk_size."""
    chunker = TextChunker(chunk_size=500, chunk_overlap=50)
    text = "Short text."
    chunks = chunker.chunk(text)

    assert len(chunks) == 1
    assert chunks[0]["text"] == "Short text."


def test_chunker_overlap():
    """Chunks overlap by the configured amount."""
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    text = "B" * 200
    chunks = chunker.chunk(text)

    assert chunks[0]["char_end"] > chunks[1]["char_start"]
