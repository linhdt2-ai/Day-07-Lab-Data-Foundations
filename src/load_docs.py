import sys
from pathlib import Path

# Đảm bảo import từ project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.models import Document
from src.store import EmbeddingStore
from src.embeddings import _mock_embed

DOCS_WITH_META = [
    ("data/bus_brt_hanoi.txt",        {"source": "bus_brt_hanoi",    "lang": "vi", "type": "route_info",   "topic": "bus_airport_brt"}),
    ("data/buyt_online_hanoi.txt",    {"source": "buyt_online",      "lang": "vi", "type": "route_info",   "topic": "bus_city"}),
    ("data/danh_sach_tuyen_buyt.txt", {"source": "danh_sach_tuyen",  "lang": "vi", "type": "route_list",   "topic": "bus_city"}),
    ("data/lich_trinh_buyt.txt",      {"source": "lich_trinh_buyt",  "lang": "vi", "type": "route_detail", "topic": "bus_city"}),
    ("data/metro_hanoi.txt",          {"source": "metro_hanoi",      "lang": "vi", "type": "route_info",   "topic": "metro"}),
    ("data/quy_dinh_phap_luat.txt",   {"source": "quy_dinh",         "lang": "vi", "type": "regulation",   "topic": "law_traffic"}),
    ("data/tai_lieu_phap_ly.txt",     {"source": "tai_lieu_phap_ly", "lang": "vi", "type": "legal_doc",    "topic": "law_education"}),
]

def load_store(chunker, collection_name="phase2"):
    store = EmbeddingStore(collection_name=collection_name, embedding_fn=_mock_embed)
    all_docs = []
    file_stats = {}
    for path_str, meta in DOCS_WITH_META:
        p = ROOT / path_str
        if not p.exists():
            print(f"  ⚠ Missing: {path_str}")
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        chunks = chunker.chunk(text)
        file_stats[p.name] = len(chunks)
        for j, chunk in enumerate(chunks):
            all_docs.append(Document(
                id=f"{p.stem}_c{j}",
                content=chunk,
                metadata={**meta, "chunk_index": j},
            ))
    store.add_documents(all_docs)
    print(f"  ✓ Total chunks: {store.get_collection_size()} from {len(file_stats)} files")
    for fname, cnt in file_stats.items():
        print(f"    {fname:<35s}: {cnt:4d} chunks")
    return store

if __name__ == "__main__":
    from src.chunking import SentenceChunker
    print("\n=== Test Load (SentenceChunker max=3) ===")
    store = load_store(SentenceChunker(max_sentences_per_chunk=3))
