import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.chunking import ChunkingStrategyComparator

FILES = {
    "bus_brt_hanoi":        "data/bus_brt_hanoi.txt",
    "lich_trinh_buyt":      "data/lich_trinh_buyt.txt",
    "metro_hanoi":          "data/metro_hanoi.txt",
    "quy_dinh_phap_luat":   "data/quy_dinh_phap_luat.txt",
    "tai_lieu_phap_ly":     "data/tai_lieu_phap_ly.txt",
}

SAMPLE_LEN = 3000   # chỉ lấy 3000 ký tự đầu để so sánh nhanh

cmp = ChunkingStrategyComparator()

print("\n" + "=" * 70)
print("BASELINE COMPARISON — ChunkingStrategyComparator (chunk_size=300)")
print("=" * 70)
print(f"{'File':<25} {'Strategy':<18} {'Chunks':>6} {'Avg len':>8}")
print("-" * 70)

for name, path_str in FILES.items():
    p = ROOT / path_str
    if not p.exists():
        print(f"  ⚠ Missing: {path_str}")
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    sample = text[:SAMPLE_LEN]
    result = cmp.compare(sample, chunk_size=300)
    first = True
    for strategy, stats in result.items():
        label = name if first else ""
        print(f"  {label:<23} {strategy:<18} {stats['count']:>6}  {stats['avg_length']:>8.1f}")
        first = False
    print()

print("=" * 70)
print("Ghi chú: Chạy trên sample 3000 ký tự đầu mỗi file.")
