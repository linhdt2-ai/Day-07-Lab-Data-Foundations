import sys
from pathlib import Path

# Đảm bảo import từ project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.chunking import compute_similarity
from src.embeddings import _mock_embed

pairs = [
    ("Xe buýt số 7 chạy từ Cầu Giấy đến sân bay Nội Bài.",
     "Tuyến 7: Cầu Giấy – Nội Bài, giá 8.000đ, giờ 05:00–21:35."),

    ("Metro Cát Linh – Hà Đông có 12 ga, khai thác từ 2021.",
     "Tuyến xe buýt nhanh BRT Kim Mã – Yên Nghĩa dài 14.7 km."),

    ("Không được ăn uống trên tàu metro.",
     "Nghiêm cấm hút thuốc trong khu vực nhà ga metro."),

    ("Học bổng loại Khá bằng mức trần học phí hiện hành.",
     "Vé tháng toàn mạng xe buýt Hà Nội giá 200.000 đồng."),

    ("Tuyến 32 đi từ Giáp Bát qua Kim Mã đến Nhổn.",
     "Tuyến 32: Bến xe Giáp Bát – Nhổn, giá 7.000đ, tần suất 5–20 phút."),
]

print("\n=== Cosine Similarity Predictions (MockEmbedder) ===")
print(f"{'Pair':<6}  {'Pred':>10}  Câu A (60 ký tự đầu)")
print("-" * 70)
for i, (a, b) in enumerate(pairs, 1):
    va = _mock_embed(a)
    vb = _mock_embed(b)
    score = compute_similarity(va, vb)
    print(f"Pair {i}:  score={score:.4f}  | {a[:60]}...")

print("\nGhi chú: MockEmbedder dùng MD5 hash nên score có thể không phản ánh nghĩa.")
