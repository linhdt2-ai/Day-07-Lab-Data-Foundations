# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** 2A202600660-Nguyễn Hải Quân  
**Nhóm:** [Bổ sung tên nhóm nếu có]  
**Ngày:** 5/6/2026

---

## 1. Warm-up

### Cosine Similarity

**High cosine similarity nghĩa là gì?**

High cosine similarity nghĩa là hai vector embedding có hướng gần giống nhau trong không gian vector. Với text embeddings, điều này thường cho thấy hai đoạn văn/câu có ý nghĩa hoặc chủ đề tương tự nhau, dù chúng không nhất thiết dùng đúng cùng từ khóa.

**Ví dụ HIGH similarity:**

- Sentence A: Python is a high-level programming language.
- Sentence B: Python is used to build software applications.
- Tại sao tương đồng: Cả hai câu đều nói về Python trong ngữ cảnh lập trình/phát triển phần mềm.

**Ví dụ LOW similarity:**

- Sentence A: Vector databases store embeddings for similarity search.
- Sentence B: A recipe explains how to bake a chocolate cake.
- Tại sao khác: Một câu nói về vector database trong AI/retrieval, câu còn lại nói về nấu ăn.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**

Cosine similarity tập trung vào hướng của vector, tức là pattern ngữ nghĩa, thay vì chỉ đo khoảng cách tuyệt đối giữa hai điểm. Điều này phù hợp với text embeddings vì độ dài hoặc độ lớn vector không quan trọng bằng việc hai vector có biểu diễn cùng chủ đề hay không.

### Chunking Math

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**

```text
num_chunks = ceil((doc_length - overlap) / (chunk_size - overlap))
num_chunks = ceil((10000 - 50) / (500 - 50))
num_chunks = ceil(9950 / 450)
num_chunks = ceil(22.11)
num_chunks = 23
```

**Đáp án:** 23 chunks.

**Nếu overlap tăng lên 100 thì sao?**

```text
num_chunks = ceil((10000 - 100) / (500 - 100))
num_chunks = ceil(9900 / 400)
num_chunks = ceil(24.75)
num_chunks = 25
```

Khi overlap tăng từ 50 lên 100, số chunk tăng từ 23 lên 25 vì mỗi bước trượt ngắn hơn. Overlap nhiều hơn giúp giữ thêm ngữ cảnh giữa hai chunk liền kề, giảm rủi ro một ý quan trọng bị cắt ngang ở ranh giới chunk.

---

## 2. Document Selection - Nhóm

### Domain & Lý Do Chọn

**Domain:** Giao thông công cộng Hà Nội và tài liệu pháp lý liên quan.

Nhóm chọn domain này vì dữ liệu có nhiều dạng câu hỏi thực tế: tra cứu tuyến buýt, metro, quy định khi đi phương tiện công cộng, và chính sách pháp lý/học bổng trong tài liệu nghị định. Đây là domain phù hợp để đánh giá retrieval vì câu hỏi cần tìm đúng đoạn thông tin cụ thể, không chỉ tìm tài liệu cùng chủ đề.

### Data Inventory

Bộ dữ liệu nằm tại:

```text
D:\CongViec\AI\day 7\Day-07-Lab-Data-Foundations\data\hanoi
```

| # | Tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|----------|-------|----------|-----------------|
| 1 | bus_brt_hanoi.txt | data/hanoi/bus_brt_hanoi.txt | 5238 | doc_id, source, chunk_index, category |
| 2 | buyt_online_hanoi.txt | data/hanoi/buyt_online_hanoi.txt | 2397 | doc_id, source, chunk_index, category |
| 3 | danh_sach_tuyen_buyt.txt | data/hanoi/danh_sach_tuyen_buyt.txt | 20666 | doc_id, source, chunk_index, category |
| 4 | lich_trinh_buyt.txt | data/hanoi/lich_trinh_buyt.txt | 105527 | doc_id, source, chunk_index, category |
| 5 | metro_hanoi.txt | data/hanoi/metro_hanoi.txt | 4128 | doc_id, source, chunk_index, category |
| 6 | quy_dinh_phap_luat.txt | data/hanoi/quy_dinh_phap_luat.txt | 1758 | doc_id, source, chunk_index, category |
| 7 | tai_lieu_phap_ly.txt | data/hanoi/tai_lieu_phap_ly.txt | 77755 | doc_id, source, chunk_index, category |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| doc_id | string | metro_hanoi | Xác định tài liệu gốc và chấm top-k relevance. |
| source | string | data/hanoi/metro_hanoi.txt | Truy vết nguồn thông tin. |
| chunk_index | int | 0 | Biết đoạn nào trong tài liệu được retrieve. |
| category | string | hanoi_transport | Có thể mở rộng để filter theo bus, metro, legal, app. |

---

## 3. Chunking Strategy

### Baseline Analysis

Tôi so sánh ba chiến lược chunking có sẵn trong package:

| Strategy | Cách hoạt động | Điểm mạnh | Điểm yếu |
|----------|----------------|-----------|----------|
| FixedSizeChunker | Cắt theo số ký tự cố định, có overlap. | Dễ kiểm soát kích thước, đơn giản. | Dễ cắt ngang câu hoặc đoạn luật/tuyến xe. |
| SentenceChunker | Tách theo câu rồi gom nhiều câu thành chunk. | Dễ đọc, giữ ranh giới câu. | Không tối ưu với bảng tuyến xe hoặc tài liệu pháp lý dài. |
| RecursiveChunker | Ưu tiên tách theo đoạn, dòng, câu, từ, rồi ký tự. | Giữ cấu trúc tài liệu tốt nhất, phù hợp markdown/text dài. | Cần chọn `chunk_size` hợp lý. |

### Strategy Của Tôi

**Loại:** `RecursiveChunker(chunk_size=2500)` kết hợp Gemini embedding thật.

Tôi chọn recursive chunking vì bộ dữ liệu có nhiều cấu trúc khác nhau: danh sách tuyến, lịch trình dài, quy định pháp luật, và phần mô tả metro/bus. Recursive chunking cố giữ đoạn lớn trước, chỉ tách nhỏ khi cần, nên phù hợp hơn fixed-size thuần túy. Với `chunk_size=2500`, 7 tài liệu được chia thành 74 chunks, đủ nhỏ để retrieve chính xác hơn nhưng vẫn giữ được ngữ cảnh tuyến/điều khoản.

### So Sánh Với Baseline

| Cấu hình | Embedding | Stored chunks | Retrieval top-3 trên 5 query nhóm | Nhận xét |
|----------|-----------|---------------|------------------------------------|----------|
| Baseline | `_mock_embed` + RecursiveChunker | 74 chunks | 2 / 5 relevant in top-3 | Đủ để test code, nhưng không hiểu ngữ nghĩa thật nên retrieval nhiễu. |
| Strategy của tôi | Gemini `gemini-embedding-2` + RecursiveChunker | 74 chunks | 5 / 5 relevant in top-3 | Kết quả tốt hơn rõ rệt, tìm đúng tài liệu/đoạn liên quan. |

**So sánh với thành viên khác:** hiện chưa có bảng score/tên chiến lược cụ thể từ từng thành viên khác. Nếu nhóm bổ sung kết quả của các thành viên, bảng này nên thêm strategy, top-3 score và điểm mạnh/yếu của từng người. Trong phạm vi hiện tại, phần benchmark chung của nhóm đã được chạy trên implementation cá nhân của tôi.

---

## 4. My Approach - Cá Nhân

### Chunking Functions

**`SentenceChunker.chunk`**

Tôi dùng regex `(?<=[.!?])(?:\s+|\n+)` để tách câu sau các dấu `.`, `!`, `?` khi phía sau là khoảng trắng hoặc xuống dòng. Sau đó tôi strip whitespace, bỏ câu rỗng, và gom mỗi `max_sentences_per_chunk` câu thành một chunk.

**`RecursiveChunker.chunk` / `_split`**

Thuật toán kiểm tra base case trước: nếu text đã nhỏ hơn hoặc bằng `chunk_size` thì trả về luôn. Nếu text quá dài, `_split` lần lượt thử separator ưu tiên từ lớn đến nhỏ: đoạn văn, dòng, câu, từ, rồi ký tự. Các mảnh vẫn quá dài sẽ được gọi đệ quy với separator tiếp theo; khi hết separator thì fallback sang cắt fixed-size theo ký tự.

**`compute_similarity`**

Tôi tính cosine similarity bằng công thức:

```text
dot(a, b) / (norm(a) * norm(b))
```

Nếu một trong hai vector có norm bằng 0 thì trả về `0.0` để tránh lỗi chia cho 0.

**`ChunkingStrategyComparator.compare`**

Comparator chạy ba strategy có sẵn: `FixedSizeChunker`, `SentenceChunker`, và `RecursiveChunker`. Với mỗi strategy, kết quả trả về gồm `count`, `avg_length`, và danh sách `chunks`.

### EmbeddingStore

**`add_documents` + `search`**

Mỗi `Document` được chuẩn hóa thành một record gồm `id`, `doc_id`, `content`, `metadata`, và `embedding`. Embedding được tạo bằng `embedding_fn`, mặc định là `_mock_embed`. Khi search, query cũng được embed rồi tính dot product với từng record embedding, sau đó sort giảm dần theo `score` và trả về top-k.

**Embedding backend**

Tôi giữ `_mock_embed` làm backend mặc định cho test tự động vì mock embedding deterministic, không cần API key và giúp kết quả unit test ổn định. Khi đánh giá retrieval thực tế trên data Hà Nội, tôi bổ sung `GeminiEmbedder` để dùng embedding thật qua Gemini API với model `gemini-embedding-2`. API key được đặt trong `.env` local, không ghi vào report và không commit lên git.

**`search_with_filter` + `delete_document`**

`search_with_filter` lọc metadata trước để thu hẹp candidates, rồi mới chạy similarity search trên tập đã lọc. `delete_document` xóa tất cả records có `metadata["doc_id"]` hoặc `record["doc_id"]` trùng với `doc_id` cần xóa và trả về `True` nếu có record bị xóa.

### KnowledgeBaseAgent

**`answer`**

Agent nhận câu hỏi, gọi `store.search(question, top_k)` để lấy các chunk liên quan, rồi build prompt gồm context, source, score và câu hỏi. Prompt yêu cầu LLM chỉ trả lời dựa trên context đã retrieve; nếu context không đủ thì phải nói rõ knowledge base không có đủ thông tin.

### Test Results

Tôi cài Python 3.12, tạo `.venv`, cài dependencies và chạy:

```bash
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

Kết quả:

```text
platform win32 -- Python 3.12.10, pytest-9.0.3
collected 42 items
42 passed in 0.08s
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions - Cá Nhân

Các score dưới đây được tính bằng logic tương đương `_mock_embed` trong repo. Lưu ý: mock embedding deterministic nhưng không phải semantic embedding thật, nên điểm số có thể không phản ánh đúng trực giác ngữ nghĩa.

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Python is a high-level programming language. | Python is used to build software applications. | high | -0.0008 | Không |
| 2 | Vector databases store embeddings for similarity search. | A vector store helps retrieve semantically similar text chunks. | high | -0.2151 | Không |
| 3 | Recursive chunking preserves paragraph context. | The weather is sunny at the beach today. | low | -0.0362 | Có |
| 4 | Customer support agents follow escalation playbooks. | Support teams use procedures to handle customer issues. | high | -0.0695 | Không |
| 5 | Machine learning learns patterns from data. | A recipe explains how to bake a chocolate cake. | low | 0.0622 | Gần đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**

Kết quả bất ngờ nhất là các cặp có nghĩa gần nhau như Python/programming hoặc vector store/retrieval lại không có score cao. Điều này xảy ra vì `_mock_embed` chỉ tạo vector deterministic từ hash của text, không học ngữ nghĩa thật như model embedding. Khi dùng Gemini embedding thật ở phần benchmark, retrieval phản ánh ngữ nghĩa tốt hơn nhiều.

---

## 6. Results - Benchmark Queries Nhóm

### Benchmark Queries & Gold Answers

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ? | Giá 8.000đ, giờ hoạt động 05:00-21:35, tuyến Cầu Giấy - Nội Bài qua Cầu Thăng Long |
| 2 | Metro Cát Linh-Hà Đông có bao nhiêu ga và chạy mấy giờ? | 12 ga, hoạt động 05:30-22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút |
| 3 | Quy định về việc ăn uống trên metro Hà Nội? | Nghiêm cấm ăn uống; mức phạt từ 100.000-300.000đ trong tàu và sân ga |
| 4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | Tuyến 32: Giáp Bát -> Mã -> Cầu Giấy -> Nhổn |
| 5 | Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu? | Mức học bổng >= mức trần học phí hiện hành của ngành (Điều 7, Nghị định 66/2026) |

### Cấu Hình Chạy Benchmark

```text
Embedding backend: gemini-embedding-2
Chunker: RecursiveChunker
Chunk size: 2500
Stored chunks: 74
Script: scripts/evaluate_hanoi_gemini.py
```

Do Gemini API có quota requests/phút, script có delay 1.1 giây/request để tránh lỗi `429 RESOURCE_EXHAUSTED`.

Tôi cũng chạy baseline bằng `_mock_embed` trên đúng 5 query nhóm để so sánh với embedding thật:

| # | Query | Mock Top-1 Document | Mock Top-3 Relevant? | Nhận xét |
|---|-------|---------------------|----------------------|----------|
| 1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ? | `lich_trinh_buyt` chunk 20 | Yes | Đúng nhóm tài liệu, nhưng chunk chưa phải tuyến 07 cụ thể. |
| 2 | Metro Cát Linh-Hà Đông có bao nhiêu ga và chạy mấy giờ? | `tai_lieu_phap_ly` chunk 9 | No | Mock retrieve sai sang tài liệu pháp lý. |
| 3 | Quy định về việc ăn uống trên metro Hà Nội? | `tai_lieu_phap_ly` chunk 10 | Yes | Có liên quan theo expected doc, nhưng preview chưa đúng đoạn ăn uống. |
| 4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | `tai_lieu_phap_ly` chunk 13 | No | Sai domain. |
| 5 | Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu? | `metro_hanoi` chunk 1 | No | Sai domain. |

**Mock baseline relevant trong top-3:** 2 / 5.

### Kết Quả Của Tôi

| # | Query | Top-1 Retrieved Chunk | Score | Relevant Top-3? | Agent Answer / Gold Summary |
|---|-------|----------------------|-------|-----------------|-----------------------------|
| 1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ? | `lich_trinh_buyt` chunk 0 | 0.7766 | Yes | Giá 8.000đ, 05:00-21:35, tuyến Cầu Giấy - Nội Bài qua Cầu Thăng Long |
| 2 | Metro Cát Linh-Hà Đông có bao nhiêu ga và chạy mấy giờ? | `metro_hanoi` chunk 1 | 0.7545 | Yes | 12 ga, 05:30-22:30, cao điểm 6 phút/chuyến, toàn tuyến 23 phút |
| 3 | Quy định về việc ăn uống trên metro Hà Nội? | `quy_dinh_phap_luat` chunk 0 | 0.6817 | Yes | Nghiêm cấm ăn uống; phạt 100.000-300.000đ trong tàu và sân ga |
| 4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | `lich_trinh_buyt` chunk 22 | 0.7565 | Yes | Tuyến 32: Giáp Bát -> Mã/Cầu Giấy -> Nhổn |
| 5 | Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu? | `tai_lieu_phap_ly` chunk 7 | 0.7109 | Yes | Mức học bổng loại Khá >= mức trần học phí hiện hành của ngành |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 5 / 5.

### Failure Analysis

Không có query nào fail theo tiêu chí top-3 relevance trong lần chạy Gemini chính thức. Tuy nhiên vẫn có một rủi ro chất lượng ở query số 2: top-1 là `metro_hanoi` chunk 1, nhưng đoạn preview nghiêng về tuyến Nhổn - Ga Hà Nội; top-2 mới chứa phần Cát Linh - Hà Đông rõ hơn. Điều này cho thấy top-3 relevance tốt, nhưng top-1 precision chưa luôn hoàn hảo. Cách cải thiện là chunk nhỏ hơn theo từng tuyến metro hoặc thêm metadata `line=2A` và `line=3` để filter theo tuyến.

---

## 7. What I Learned

**Điều hay nhất tôi học được từ strategy này:**

Mock embedding rất hữu ích để test code vì ổn định và không cần API key, nhưng không nên dùng để đánh giá retrieval thực tế. Khi chuyển sang Gemini embedding thật, kết quả trên data Hà Nội cải thiện rõ rệt và đạt 5/5 query có chunk relevant trong top-3.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**

Tôi sẽ thêm metadata chi tiết hơn cho từng chunk, ví dụ `transport_type=bus/metro/legal`, `route_number=07/32`, `metro_line=2A`, hoặc `document_type=policy/schedule/list`. Với metadata tốt hơn, `search_with_filter()` có thể giúp tăng precision, đặc biệt khi câu hỏi có tuyến cụ thể hoặc loại tài liệu cụ thể.

**Bài học về failure/risk:**

Retrieval không chỉ cần đúng tài liệu trong top-3 mà còn cần đúng chunk ở top-1. Nếu tài liệu chứa nhiều tuyến hoặc nhiều quy định trong cùng một chunk lớn, embedding có thể retrieve đúng file nhưng chưa đúng đoạn nhất. Vì vậy chunking strategy và metadata schema quan trọng gần như ngang với embedding model.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 9 / 10 |
| Chunking strategy | Nhóm | 13 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 5 / 5 |
| Results | Cá nhân | 10 / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | 4 / 5 |
| **Tổng** | | **86 / 100** |
