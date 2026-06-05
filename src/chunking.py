from __future__ import annotations

import math
import re


class FixedSizeChunker:
    """
    Split text into fixed-size chunks with optional overlap.

    Rules:
        - Each chunk is at most chunk_size characters long.
        - Consecutive chunks share overlap characters.
        - The last chunk contains whatever remains.
        - If text is shorter than chunk_size, return [text].
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]

        step = self.chunk_size - self.overlap
        chunks: list[str] = []
        for start in range(0, len(text), step):
            chunk = text[start : start + self.chunk_size]
            chunks.append(chunk)
            if start + self.chunk_size >= len(text):
                break
        return chunks


class SentenceChunker:
    """
    Split text into chunks of at most max_sentences_per_chunk sentences.

    Sentence detection: split on ". ", "! ", "? " or ".\n".
    Strip extra whitespace from each chunk.
    """

    def __init__(self, max_sentences_per_chunk: int = 3) -> None:
        self.max_sentences_per_chunk = max(1, max_sentences_per_chunk)

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        
        # Split into sentences using lookbehind for sentence-ending punctuation followed by space or newline
        sentences = re.split(r'(?<=\. |\! |\? |\.\n)', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        for i in range(0, len(sentences), self.max_sentences_per_chunk):
            chunk_sentences = sentences[i : i + self.max_sentences_per_chunk]
            chunks.append(" ".join(chunk_sentences))
        return chunks


class RecursiveChunker:
    """
    Recursively split text using separators in priority order.

    Default separator priority:
        ["\n\n", "\n", ". ", " ", ""]
    """

    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def __init__(self, separators: list[str] | None = None, chunk_size: int = 500) -> None:
        self.separators = self.DEFAULT_SEPARATORS if separators is None else list(separators)
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        return self._split(text, self.separators)

    def _split(self, current_text: str, remaining_separators: list[str]) -> list[str]:
        if len(current_text) <= self.chunk_size:
            return [current_text]
        if not remaining_separators:
            # Fall back to character splitting
            return [current_text[i : i + self.chunk_size] for i in range(0, len(current_text), self.chunk_size)]

        sep = remaining_separators[0]
        if sep == "":
            return [current_text[i : i + self.chunk_size] for i in range(0, len(current_text), self.chunk_size)]

        parts = current_text.split(sep)
        chunks: list[str] = []
        current_chunk: list[str] = []
        current_len = 0

        for part in parts:
            if len(part) > self.chunk_size:
                # Flush current chunk
                if current_chunk:
                    chunks.append(sep.join(current_chunk))
                    current_chunk = []
                    current_len = 0
                # Recursively split the oversized part using remaining separators
                sub_chunks = self._split(part, remaining_separators[1:])
                chunks.extend(sub_chunks)
            else:
                sep_len = len(sep) if current_chunk else 0
                if current_len + sep_len + len(part) <= self.chunk_size:
                    current_chunk.append(part)
                    current_len += sep_len + len(part)
                else:
                    if current_chunk:
                        chunks.append(sep.join(current_chunk))
                    current_chunk = [part]
                    current_len = len(part)

        if current_chunk:
            chunks.append(sep.join(current_chunk))

        return [c for c in chunks if c]


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def compute_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    cosine_similarity = dot(a, b) / (||a|| * ||b||)

    Returns 0.0 if either vector has zero magnitude.
    """
    dot_prod = _dot(vec_a, vec_b)
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(x * x for x in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot_prod / (norm_a * norm_b)


class ChunkingStrategyComparator:
    """Run all built-in chunking strategies and compare their results."""

    def compare(self, text: str, chunk_size: int = 200) -> dict:
        fixed = FixedSizeChunker(chunk_size=chunk_size, overlap=int(chunk_size * 0.1))
        sentence = SentenceChunker(max_sentences_per_chunk=3)
        recursive = RecursiveChunker(chunk_size=chunk_size)

        results = {}
        for name, chunker in [("fixed_size", fixed), ("by_sentences", sentence), ("recursive", recursive)]:
            chunks = chunker.chunk(text)
            count = len(chunks)
            avg_length = sum(len(c) for c in chunks) / count if count > 0 else 0.0
            results[name] = {
                "chunks": chunks,
                "count": count,
                "avg_length": avg_length
            }
        return results


class HanoiTransitChunker:
    """
    Custom chunking strategy for Hanoi Public Transit data.
    Splits text by route headers (e.g., 'Tuyến', 'Tuyến số', 'Lộ trình')
    to ensure each bus route or metro line remains in a single coherent chunk.
    """
    def __init__(self, chunk_size: int = 1000) -> None:
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        raw_paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = []
        current_len = 0
        for para in raw_paragraphs:
            para_stripped = para.strip()
            if not para_stripped:
                continue
            
            is_new_route = any(para_stripped.startswith(prefix) for prefix in ["Tuyến", "Tuyến số", "Lộ trình", "Chiều đi", "Chiều về"])
            if is_new_route and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_len = 0
            
            if len(para_stripped) > self.chunk_size:
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = []
                    current_len = 0
                sub_parts = [para_stripped[i:i+self.chunk_size] for i in range(0, len(para_stripped), self.chunk_size)]
                chunks.extend(sub_parts)
            else:
                sep_len = 2 if current_chunk else 0
                if current_len + sep_len + len(para_stripped) <= self.chunk_size:
                    current_chunk.append(para_stripped)
                    current_len += sep_len + len(para_stripped)
                else:
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = [para_stripped]
                    current_len = len(para_stripped)
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
        return chunks
