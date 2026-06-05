import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.chunking import SentenceChunker, RecursiveChunker, FixedSizeChunker
from src.agent import KnowledgeBaseAgent
from load_docs import load_store   # import local

# ─── 5 Benchmark queries ──────────────────────────────────────────────────────
QUERIES = [
    ("Q1", "Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?",
     None),
    ("Q2", "Metro Cát Linh Hà Đông có bao nhiêu ga và chạy mấy giờ?",
     {"topic": "metro"}),
    ("Q3", "Quy định về việc ăn uống trên metro Hà Nội?",
     {"topic": "law_traffic"}),
    ("Q4", "Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?",
     {"topic": "bus_city"}),
    ("Q5", "Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?",
     {"topic": "law_education"}),
]

# ─── Các strategies cần so sánh ──────────────────────────────────────────────
STRATEGIES = [
    ("SentenceChunker(max=3)",     SentenceChunker(max_sentences_per_chunk=3)),
    ("RecursiveChunker(size=500)", RecursiveChunker(chunk_size=500)),
    ("FixedSize(400, ol=80)",      FixedSizeChunker(chunk_size=400, overlap=80)),
]

# ─── Mock LLM: chỉ echo context đầu tiên ─────────────────────────────────────
def mock_llm(prompt: str) -> str:
    lines = prompt.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped and stripped.startswith("[") and "]" in stripped:
            return stripped[:120]
    return "[Không tìm thấy context phù hợp]"

def check_relevant(content: str, qid: str) -> bool:
    """Heuristic: kiểm tra chunk có chứa từ khóa gold answer không."""
    content_lower = content.lower()
    checks = {
        "Q1": ["số 7", "nội bài", "cầu giấy", "8.000", "05:00", "21:35"],
        "Q2": ["12 ga", "05:30", "22:30", "cát linh"],
        "Q3": ["ăn uống", "nghiêm cấm", "100.000", "300.000"],
        "Q4": ["tuyến 32", "giáp bát", "nhổn"],
        "Q5": ["học bổng", "loại khá", "học phí", "khuyến khích"],
    }
    keywords = checks.get(qid, [])
    return any(kw in content_lower for kw in keywords)

# ─── Chạy benchmark ───────────────────────────────────────────────────────────
all_results = {}   # {strategy_name: {qid: hit?}}

for strat_name, chunker in STRATEGIES:
    print(f"\n{'=' * 68}")
    print(f"  Strategy: {strat_name}")
    print("=" * 68)

    store = load_store(chunker, collection_name=strat_name)
    agent = KnowledgeBaseAgent(store=store, llm_fn=mock_llm)

    q_results = {}
    for qid, query, flt in QUERIES:
        print(f"\n  {qid}: {query}")
        if flt:
            results = store.search_with_filter(query, top_k=3, metadata_filter=flt)
            print(f"       [filter={flt}]")
        else:
            results = store.search(query, top_k=3)

        hit = False
        for rank, r in enumerate(results, 1):
            src     = r["metadata"].get("source", "?")
            topic   = r["metadata"].get("topic", "?")
            score   = r["score"]
            preview = r["content"][:80].replace("\n", " ").replace("\r", "")
            relevant_mark = "✓" if check_relevant(r["content"], qid) else " "
            print(f"    [{rank}]{relevant_mark} {score:.3f} | {src:<22} | {preview}...")
            if check_relevant(r["content"], qid):
                hit = True

        q_results[qid] = hit

    all_results[strat_name] = q_results
    total = sum(1 for v in q_results.values() if v)
    print(f"\n  → Score: {total}/5 queries có chunk relevant trong top-3")

# ─── Bảng tổng hợp ────────────────────────────────────────────────────────────
print("\n\n" + "=" * 68)
print("  BẢNG SO SÁNH TỔNG HỢP")
print("=" * 68)
header = f"  {'Strategy':<30} " + "  ".join(f"{q[0]:>4}" for q in QUERIES) + "  Score"
print(header)
print("-" * 68)
for strat_name, q_results in all_results.items():
    score = sum(1 for v in q_results.values() if v)
    marks = "  ".join("  ✓ " if q_results[q[0]] else "  ✗ " for q in QUERIES)
    print(f"  {strat_name:<30} {marks}   {score}/5")
print("=" * 68)
print("\n  ✓ = chunk relevant xuất hiện trong top-3")
print("  ✗ = không có chunk relevant trong top-3")
