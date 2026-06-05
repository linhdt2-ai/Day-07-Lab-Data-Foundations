from __future__ import annotations

import math
import sys
import time
import argparse
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src import Document, EmbeddingStore, GeminiEmbedder, RecursiveChunker, _mock_embed


DATA_DIR = Path("data/hanoi")
CHUNK_SIZE = 2500

QUERIES = [
    {
        "query": "Xe buyt so 7 tu Noi Bai den Cau Giay gia bao nhieu va may gio?",
        "gold": "Gia 8.000d, gio hoat dong 05:00-21:35, tuyen Cau Giay - Noi Bai qua Cau Thang Long",
        "expected": {"danh_sach_tuyen_buyt", "lich_trinh_buyt", "bus_brt_hanoi"},
    },
    {
        "query": "Metro Cat Linh Ha Dong co bao nhieu ga va chay may gio?",
        "gold": "12 ga, hoat dong 05:30-22:30, gio cao diem 6 phut/chuyen, toan tuyen 23 phut",
        "expected": {"metro_hanoi"},
    },
    {
        "query": "Quy dinh ve viec an uong tren metro Ha Noi?",
        "gold": "Nghiem cam an uong; muc phat tu 100.000-300.000d trong tau va san ga",
        "expected": {"quy_dinh_phap_luat", "tai_lieu_phap_ly", "metro_hanoi"},
    },
    {
        "query": "Tu Ben xe Giap Bat den Nhon di tuyen nao?",
        "gold": "Tuyen 32: Giap Bat -> Ma -> Cau Giay -> Nhon",
        "expected": {"danh_sach_tuyen_buyt", "lich_trinh_buyt"},
    },
    {
        "query": "Hoc bong khuyen khich hoc tap loai Kha danh cho sinh vien dai hoc la bao nhieu?",
        "gold": "Muc hoc bong >= muc tran hoc phi hien hanh cua nganh (Dieu 7, Nghi dinh 66/2026)",
        "expected": {"tai_lieu_phap_ly"},
    },
]


class NormalizedEmbedder:
    def __init__(self) -> None:
        self.embedder = GeminiEmbedder()
        self._backend_name = self.embedder._backend_name

    def __call__(self, text: str) -> list[float]:
        time.sleep(1.1)
        vector = self.embedder(text)
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


def load_chunked_documents() -> list[Document]:
    chunker = RecursiveChunker(chunk_size=CHUNK_SIZE)
    documents: list[Document] = []

    for path in sorted(DATA_DIR.glob("*.txt")):
        chunks = chunker.chunk(path.read_text(encoding="utf-8"))
        for index, chunk in enumerate(chunks):
            documents.append(
                Document(
                    id=f"{path.stem}-{index}",
                    content=chunk,
                    metadata={
                        "doc_id": path.stem,
                        "source": str(path),
                        "chunk_index": index,
                        "category": "hanoi_transport",
                    },
                )
            )

    return documents


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=["gemini", "mock"], default="gemini")
    args = parser.parse_args()

    load_dotenv(override=False)

    docs = load_chunked_documents()
    embedder = NormalizedEmbedder() if args.provider == "gemini" else _mock_embed
    store = EmbeddingStore(collection_name="hanoi_gemini_eval", embedding_fn=embedder)
    store.add_documents(docs)

    print(f"Embedding backend: {getattr(embedder, '_backend_name', args.provider)}")
    print(f"Chunk size: {CHUNK_SIZE}")
    print(f"Stored chunks: {store.get_collection_size()}")
    print()

    relevant_top3 = 0
    for index, item in enumerate(QUERIES, start=1):
        results = store.search(item["query"], top_k=3)
        top_docs = [result["metadata"]["doc_id"] for result in results]
        is_relevant = any(doc_id in item["expected"] for doc_id in top_docs)
        relevant_top3 += int(is_relevant)

        print(f"{index}. {item['query']}")
        print(f"   gold: {item['gold']}")
        print(f"   expected: {', '.join(sorted(item['expected']))}")
        print(f"   top3 relevant: {'yes' if is_relevant else 'no'}")
        for rank, result in enumerate(results, start=1):
            metadata = result["metadata"]
            preview = " ".join(result["content"].split())[:140]
            print(
                f"   {rank}) score={result['score']:.4f} "
                f"doc={metadata['doc_id']} chunk={metadata['chunk_index']} "
                f"preview={preview}"
            )
        print()

    print(f"Relevant in top-3: {relevant_top3} / {len(QUERIES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
