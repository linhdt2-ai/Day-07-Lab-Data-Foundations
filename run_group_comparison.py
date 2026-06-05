import os
from pathlib import Path
from src.chunking import HanoiTransitChunker, SentenceChunker, RecursiveChunker
from src.embeddings import LocalEmbedder, _mock_embed
from src.models import Document
from src.store import EmbeddingStore

DATA_DIR = Path("data")

# 5 Queries
queries = [
    {"id": 1, "query": "Lộ trình tuyến xe buýt nhanh BRT Hà Nội (Kim Mã - Yên Nghĩa) đi qua những con đường nào?", "filter": None},
    {"id": 2, "query": "Tuyến đường sắt đô thị Cát Linh - Hà Đông dài bao nhiêu km và có bao nhiêu ga?", "filter": {"topic": "metro"}},
    {"id": 3, "query": "Quy định về việc ăn uống trên metro Hà Nội?", "filter": {"topic": "law_traffic"}},
    {"id": 4, "query": "Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?", "filter": {"topic": "bus_city"}},
    {"id": 5, "query": "Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?", "filter": {"topic": "law_education"}}
]

files_to_load = [
    ("bus_brt_hanoi.txt", "bus_city"),
    ("lich_trinh_buyt.txt", "bus_city"),
    ("danh_sach_tuyen_buyt.txt", "bus_city"),
    ("metro_hanoi.txt", "metro"),
    ("quy_dinh_phap_luat.txt", "law_traffic"),
    ("tai_lieu_phap_ly.txt", "law_education"),
]

def run_evaluation(chunker_name, chunker):
    # Load embedder
    try:
        embedder = LocalEmbedder()
    except Exception:
        embedder = _mock_embed
        
    documents = []
    for filename, topic in files_to_load:
        path = DATA_DIR / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        chunks = chunker.chunk(text)
        for i, chunk in enumerate(chunks):
            documents.append(
                Document(
                    id=f"{path.stem}_{chunker_name}_chunk_{i}",
                    content=chunk,
                    metadata={"source": str(path), "topic": topic}
                )
            )
            
    store = EmbeddingStore(collection_name=f"comparison_{chunker_name}", embedding_fn=embedder)
    store.add_documents(documents)
    
    # Evaluate queries
    scores = []
    relevance_count = 0
    for q in queries:
        query_text = q["query"]
        meta_filter = q["filter"]
        
        if meta_filter:
            results = store.search_with_filter(query_text, top_k=1, metadata_filter=meta_filter)
        else:
            results = store.search(query_text, top_k=1)
            
        top_score = results[0]["score"] if results else 0.0
        scores.append(top_score)
        
        # Simple heuristic to determine if retrieved chunk is relevant
        # Check if query keywords are in the top chunk content
        is_relevant = False
        if results:
            content = results[0]["content"].lower()
            if q["id"] == 1 and ("brt" in content or "yên nghĩa" in content):
                is_relevant = True
            elif q["id"] == 2 and ("cát linh" in content or "2a" in content):
                is_relevant = True
            elif q["id"] == 3 and ("ăn uống" in content or "phạt" in content):
                is_relevant = True
            elif q["id"] == 4 and ("32" in content or "giáp bát" in content):
                is_relevant = True
            elif q["id"] == 5 and ("học bổng" in content or "66/2026" in content):
                is_relevant = True
                
        if is_relevant:
            relevance_count += 1
            
    avg_score = sum(scores) / len(scores) if scores else 0.0
    success_rate = relevance_count / len(queries)
    return avg_score, success_rate

def main():
    print("=== Comparing All 3 Strategies on 5 Queries ===")
    
    # Custom Chunker
    custom_chunker = HanoiTransitChunker(chunk_size=1000)
    # Sentence Chunker
    sentence_chunker = SentenceChunker(max_sentences_per_chunk=3)
    # Recursive Chunker
    recursive_chunker = RecursiveChunker(chunk_size=1000)
    
    for name, chunker in [
        ("HanoiTransitChunker (Custom)", custom_chunker),
        ("SentenceChunker", sentence_chunker),
        ("RecursiveChunker", recursive_chunker)
    ]:
        avg_score, success_rate = run_evaluation(name.split(" ")[0].lower(), chunker)
        print(f"Strategy: {name:30} | Avg Sim Score: {avg_score:.4f} | Success Rate (Relevance): {success_rate * 100:.1f}%")

if __name__ == "__main__":
    main()
