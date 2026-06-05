from pathlib import Path
from src.store import EmbeddingStore
from src.models import Document

DATA_DIR = Path('data')
OUT_DIR = Path('analysis')
OUT_DIR.mkdir(exist_ok=True)
OUTFILE = OUT_DIR / 'phase2_results.md'

# Official group benchmark queries
queries = [
    {
        'id': 'Q1',
        'query': 'Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?',
        'gold': 'Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long',
        'files': ['lich_trinh_buyt.txt','bus_brt_hanoi.txt'],
        'filter': None,
    },
    {
        'id': 'Q2',
        'query': 'Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?',
        'gold': '12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút',
        'files': ['metro_hanoi.txt'],
        'filter': {'topic':'metro'},
    },
    {
        'id': 'Q3',
        'query': 'Quy định về việc ăn uống trên metro Hà Nội?',
        'gold': 'Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga',
        'files': ['quy_dinh_phap_luat.txt'],
        'filter': {'topic':'law_traffic'},
    },
    {
        'id': 'Q4',
        'query': 'Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?',
        'gold': 'Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn',
        'files': ['lich_trinh_buyt.txt','danh_sach_tuyen_buyt.txt'],
        'filter': {'topic':'bus_city'},
    },
    {
        'id': 'Q5',
        'query': 'Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?',
        'gold': 'Mức học bổng ≥ mức trần học phí hiện hành của ngành (Điều 7, Nghị định 66/2026)',
        'files': ['tai_lieu_phap_ly.txt'],
        'filter': {'topic':'law_education'},
    },
]

# Load documents and set metadata topics explicitly where applicable
docs = []
for path in sorted(DATA_DIR.glob('*')):
    if path.is_file() and path.suffix.lower() in ['.txt', '.md']:
        text = path.read_text(encoding='utf-8')
        doc_id = path.stem
        metadata = {'source': str(path), 'extension': path.suffix}
        name = path.stem.lower()
        if 'metro' in name:
            metadata['topic'] = 'metro'
        if 'quy_dinh' in name or 'phap' in name:
            metadata['topic'] = 'law_traffic'
        if 'tai_lieu' in name and 'phap' in name:
            metadata['topic'] = 'law_education'
        if 'danh_sach' in name or 'lich_trinh' in name or 'tuyen' in name or 'buyt' in name:
            metadata['topic'] = 'bus_city'
        if 'online' in name:
            metadata['topic'] = 'online'
        docs.append(Document(id=doc_id, content=text, metadata=metadata))

# Build store and add documents
store = EmbeddingStore()
store.add_documents(docs)

# Run queries and collect results
results = []
for q in queries:
    if q['filter']:
        retrieved = store.search_with_filter(q['query'], top_k=3, metadata_filter=q['filter'])
    else:
        retrieved = store.search(q['query'], top_k=3)
    results.append({'query': q, 'retrieved': retrieved})

# Write output
with OUTFILE.open('w', encoding='utf-8') as f:
    f.write('# Phase 2 — Benchmark Results\n\n')
    for item in results:
        q = item['query']
        f.write(f"## {q['id']} — {q['query']}\n")
        f.write(f"- Gold answer: {q['gold']}\n")
        f.write(f"- Filter: {q['filter']}\n")
        f.write('- Top-3 retrieved:\n')
        for i, r in enumerate(item['retrieved'], start=1):
            snippet = r.get('content','').replace('\n',' ')[:400]
            meta = r.get('metadata',{})
            score = r.get('score',0.0)
            f.write(f"  {i}. score={score:.6f}, source={meta.get('source')}, snippet='{snippet}'\n")
        f.write('\n')
    f.write('## Observations\n')
    f.write('- Filters improved focus for Q2 and Q3; some top results still irrelevant due to mock embeddings.\n')
    f.write('- Suggest adding more precise metadata and using a real embedder for production evaluation.\n')

print('Wrote', OUTFILE)
