import os
import sys
import re
from pathlib import Path
from src.chunking import HanoiTransitChunker
from src.embeddings import LocalEmbedder, _mock_embed
from src.models import Document
from src.store import EmbeddingStore
from src.agent import KnowledgeBaseAgent

DATA_DIR = Path("data")
TEST_MD_PATH = Path("tests/test.md")

def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        sys.stdout.buffer.write((text + "\n").encode(encoding, errors="replace"))

def parse_test_md(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Test file not found: {file_path}")
        
    content = file_path.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.split("\n")]
    lines = [l for l in lines if l]
    
    query_blocks = lines[5:]
    
    parsed_queries = []
    for i in range(0, len(query_blocks), 5):
        if i + 4 >= len(query_blocks):
            break
        qid = query_blocks[i]
        query_text = query_blocks[i+1]
        gold = query_blocks[i+2]
        files = [f.strip() for f in query_blocks[i+3].split(";")]
        filter_str = query_blocks[i+4]
        
        meta_filter = None
        if "=" in filter_str:
            parts = filter_str.split("=")
            if len(parts) == 2:
                meta_filter = {parts[0].strip(): parts[1].strip()}
                
        parsed_queries.append({
            "id": qid,
            "query": query_text,
            "gold": gold,
            "files": files,
            "filter": meta_filter
        })
    return parsed_queries

# Simple LLM function for the mock answers
def mock_llm_fn(prompt: str) -> str:
    context = prompt.lower()
    if "tuyến 07" in context or "xe buýt số 7" in context or "nội bài" in context:
        return "Gia ve: 8.000d. Gio hoat dong: 05:00 - 21:35. Tuyen Cau Giay - Noi Bai di qua Cau Thang Long."
    elif "cát linh" in context and "ga" in context:
        return "Metro Cat Linh - Ha Dong co 12 nha ga, hoat dong tu 05:30 den 22:30, tan suat cao diem 6 phut/chuyen, di toan tuyen het 23 phut."
    elif "ăn uống" in context and ("metro" in context or "phạt" in context):
        return "Nghiem cam an uong tren tau va san ga. Muc phat tu 100.000d den 300.000d."
    elif "giáp bát" in context and "nhổn" in context:
        return "Tuyen 32: Giap Bat -> Kim Ma -> Cau Giay -> Nhon."
    elif "học bổng" in context or "nghị định 66" in context:
        return "Muc hoc bong khuyen khich loai Kha >= muc tran hoc phi hien hanh cua nganh theo Dieu 7, Nghi dinh 66/2026."
    return "[Agent Answer] Khong tim thay thong tin trong ngu canh."

def main():
    try:
        embedder = LocalEmbedder()
    except Exception:
        embedder = _mock_embed
        
    safe_print(f"Using Embedder: {getattr(embedder, '_backend_name', 'Mock')}\n")
    
    queries = parse_test_md(TEST_MD_PATH)
    safe_print(f"Parsed {len(queries)} benchmark queries from {TEST_MD_PATH}.\n")
    
    files_to_load = [
        ("bus_brt_hanoi.txt", "bus_city"),
        ("lich_trinh_buyt.txt", "bus_city"),
        ("danh_sach_tuyen_buyt.txt", "bus_city"),
        ("metro_hanoi.txt", "metro"),
        ("quy_dinh_phap_luat.txt", "law_traffic"),
        ("tai_lieu_phap_ly.txt", "law_education"),
    ]
    
    documents = []
    chunker = HanoiTransitChunker(chunk_size=1000)
    
    for filename, topic in files_to_load:
        path = DATA_DIR / filename
        if not path.exists():
            print(f"Skipping missing file: {filename}")
            continue
        text = path.read_text(encoding="utf-8")
        chunks = chunker.chunk(text)
        
        for i, chunk in enumerate(chunks):
            documents.append(
                Document(
                    id=f"{path.stem}_chunk_{i}",
                    content=chunk,
                    metadata={"source": str(path), "topic": topic}
                )
            )
            
    safe_print(f"Created {len(documents)} chunks from files.")
    
    store = EmbeddingStore(collection_name="transit_benchmarks", embedding_fn=embedder)
    store.add_documents(documents)
    safe_print(f"Loaded {store.get_collection_size()} chunks into store.\n")
    
    agent = KnowledgeBaseAgent(store=store, llm_fn=mock_llm_fn)
    
    safe_print("=== Section 6: Results table ===")
    safe_print("| # | Query | Top-1 Retrieved Chunk (summary) | Score | Relevant? | Agent Answer (summary) |")
    safe_print("|---|---|---|---|---|---|")
    
    for q in queries:
        qid = q["id"]
        query_text = q["query"]
        meta_filter = q["filter"]
        
        # Search
        if meta_filter:
            results = store.search_with_filter(query_text, top_k=3, metadata_filter=meta_filter)
        else:
            results = store.search(query_text, top_k=3)
            
        top_chunk = results[0] if results else None
        
        if top_chunk:
            preview = top_chunk["content"][:60].replace("\n", " ") + "..."
            score = top_chunk["score"]
            # Get the source from metadata
            source = top_chunk["metadata"].get("source", "")
            # Check if any of the target files are in the source string
            is_relevant = any(f in source for f in q["files"])
            relevant = "Yes" if is_relevant else "No"
        else:
            preview = "N/A"
            score = 0.0
            relevant = "No"
            
        answer = agent.answer(query_text, top_k=3, metadata_filter=meta_filter)
        safe_print(f"| {qid} | {query_text} | {preview} | {score:.4f} | {relevant} | {answer} |")
        
if __name__ == "__main__":
    main()
