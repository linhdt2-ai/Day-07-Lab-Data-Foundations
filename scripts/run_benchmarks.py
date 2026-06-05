from pathlib import Path
from src.chunking import ChunkingStrategyComparator
from src.store import EmbeddingStore
from src.models import Document

DATA_DIR = Path('data')
ANALYSIS_DIR = Path('analysis')
ANALYSIS_DIR.mkdir(exist_ok=True)
OUTFILE = ANALYSIS_DIR / 'benchmark_results.md'

# Vietnamese benchmark queries (as prepared)
queries = [
    {
        'id': 'Q1',
        'query': 'Buýt số 07 (Nội Bài ↔ Cầu Giấy) chạy mấy giờ và giá vé là bao nhiêu?',
        'gold': 'Giờ hoạt động khoảng 05:00–21:35; giá vé ~8.000 VND',
        'filters': None,
    },
    {
        'id': 'Q2',
        'query': 'Tuyến Metro Cát Linh–Hà Đông có bao nhiêu ga và giờ hoạt động hàng ngày?',
        'gold': '12 ga; giờ hoạt động khoảng 05:30–22:30',
        'filters': {'topic': 'metro'},
    },
    {
        'id': 'Q3',
        'query': 'Quy định về việc ăn uống trên metro Hà Nội là gì và mức phạt như thế nào?',
        'gold': 'Nghiêm cấm ăn uống trên tàu và sân ga; mức phạt ghi trong văn bản',
        'filters': {'topic': 'law_traffic'},
    },
    {
        'id': 'Q4',
        'query': 'Từ Bến xe Giáp Bát muốn đi đến Nhổn phải đi bằng tuyến nào?',
        'gold': 'Tham khảo danh sách tuyến và lịch trình để xác định (ví dụ: tuyến 32)',
        'filters': None,
    },
    {
        'id': 'Q5',
        'query': 'Hướng dẫn mua vé online cho buýt/BRT ở Hà Nội như thế nào?',
        'gold': 'Truy cập trang mua vé online, chọn tuyến/khung giờ, thanh toán, nhận mã vé',
        'filters': None,
    },
]

# Load data files into Document list
docs = []
for path in sorted(DATA_DIR.glob('*')):
    if path.is_file() and path.suffix.lower() in ['.txt', '.md']:
        text = path.read_text(encoding='utf-8')
        doc_id = path.stem
        # simple metadata: source=file and topic if filename suggests
        metadata = {'source': str(path), 'extension': path.suffix}
        if 'metro' in path.stem.lower():
            metadata['topic'] = 'metro'
        if 'quy_dinh' in path.stem.lower() or 'phap' in path.stem.lower():
            metadata['topic'] = 'law_traffic'
        if 'online' in path.stem.lower():
            metadata['topic'] = 'online'
        docs.append(Document(id=doc_id, content=text, metadata=metadata))

# Run chunking comparator per document
comparator = ChunkingStrategyComparator()
chunking_results = {}
for doc in docs:
    res = comparator.compare(doc.content, chunk_size=200)
    chunking_results[doc.id] = res

# Build embedding store and add documents
store = EmbeddingStore()
store.add_documents(docs)

# Run queries
benchmark_results = []
for q in queries:
    if q['filters']:
        retrieved = store.search_with_filter(q['query'], top_k=3, metadata_filter=q['filters'])
    else:
        retrieved = store.search(q['query'], top_k=3)
    benchmark_results.append({'query': q, 'retrieved': retrieved})

# Write markdown analysis
with OUTFILE.open('w', encoding='utf-8') as f:
    f.write('# Benchmark Results\n\n')
    f.write('## Data files analyzed\n')
    for doc in docs:
        f.write(f"- {doc.id} ({doc.metadata.get('topic', 'no-topic')}) — {len(doc.content)} chars\n")
    f.write('\n## Chunking strategy summary per document\n')
    for doc_id, res in chunking_results.items():
        f.write(f"### {doc_id}\n")
        for key, stats in res.items():
            f.write(f"- **{key}**: count={stats['count']}, avg_length={stats['avg_length']:.1f}\n")
        f.write('\n')

    f.write('## Benchmark queries and top-3 results\n')
    for br in benchmark_results:
        q = br['query']
        f.write(f"### {q['id']}: {q['query']}\n")
        f.write(f"- Gold answer: {q['gold']}\n")
        f.write('- Retrieved top-3:\n')
        for idx, item in enumerate(br['retrieved'], start=1):
            content = item.get('content','').replace('\n',' ')[:300]
            metadata = item.get('metadata',{})
            score = item.get('score', 0.0)
            f.write(f"  - {idx}. score={score:.6f}, source={metadata.get('source')}, snippet='{content}'\n")
        f.write('\n')

    f.write('## Observations\n')
    f.write('- Chunking: compare counts and avg lengths to choose strategy.\n')
    f.write('- Retrieval: mock embeddings used; scores are relative.\n')
    f.write('\n')

print('Wrote', OUTFILE)
