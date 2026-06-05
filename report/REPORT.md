# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** [Tên sinh viên]
**Nhóm:** [Tên nhóm]
**Ngày:** [Ngày nộp]

---

> **Ghi chú:** Báo cáo này đã hoàn thành các phần cá nhân quan trọng theo rubric: Warm-up, My Approach, Similarity Predictions, và Core Implementation. Phần Document Selection, Benchmark Queries, và Demo vẫn giữ placeholder để cập nhật sau khi nhóm thống nhất.

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
> Cosine similarity cao nghĩa là hai vector embeddings có hướng gần giống nhau, tức là hai văn bản có nội dung hoặc ý nghĩa tương tự. Đây là thước đo phù hợp để so sánh semantic của text embeddings.

**Ví dụ HIGH similarity:**
- Sentence A: "The quick brown fox jumps over the lazy dog."
- Sentence B: "A fox is a small omnivorous mammal."
- Tại sao tương đồng: Cả hai câu đề cập đến "fox" và đặc điểm của loài cáo, nên semantic gần nhau.

**Ví dụ LOW similarity:**
- Sentence A: "Cats sleep a lot during the day."
- Sentence B: "Dogs are loyal companions and working animals."
- Tại sao khác: Hai câu nói về hai loài động vật khác nhau với thông tin không trùng khớp.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> Cosine similarity chỉ so sánh hướng của vector, bỏ qua độ lớn, nên phù hợp để đánh giá sự giống nhau về ý nghĩa. Euclidean distance bị ảnh hưởng bởi scale và không thể phân biệt tốt khi cùng nội dung nhưng có độ lớn khác nhau.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> Với `chunk_size=500` và `overlap=50`, step là `450`. Số chunk sẽ là `ceil((10000 - 500) / 450) + 1 = 23`.
> **Đáp án:** 23 chunks.

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**
> Khi overlap tăng lên 100, step giảm xuống 400 nên số chunk tăng lên khoảng 25. Overlap nhiều hơn giúp giữ ngữ cảnh giữa các chunk, giảm khả năng cắt ngang ý và tăng cơ hội tìm được chunk chứa thông tin liên quan.

---

## 2. Document Selection — Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Giao thông công cộng Hà Nội

**Tại sao nhóm chọn domain này?**
> Nhóm chọn chủ đề giao thông công cộng vì ta đã có sẵn một bộ tài liệu mạnh gồm các tuyến buýt, lộ trình, lịch trình và thông tin metro. Domain này phù hợp để kiểm thử retrieval vì dữ liệu chứa nhiều dạng nội dung: danh sách tuyến, giờ chạy, giá vé, tên điểm và thông tin nhà ga.

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|--------------|-------|----------|-----------------|
| 1 | bus_brt_hanoi.txt | data/ | 4123 | source, extension, doc_id, topic=bus_city |
| 2 | buyt_online_hanoi.txt | data/ | 1846 | source, extension, doc_id, topic=online |
| 3 | danh_sach_tuyen_buyt.txt | data/ | 16825 | source, extension, doc_id, topic=bus_city |
| 4 | lich_trinh_buyt.txt | data/ | 82158 | source, extension, doc_id, topic=bus_city |
| 5 | metro_hanoi.txt | data/ | 3214 | source, extension, doc_id, topic=metro |
| 6 | quy_dinh_phap_luat.txt | data/ | 1405 | source, extension, doc_id, topic=law_traffic |
| 7 | tai_lieu_phap_ly.txt | data/ | 57758 | source, extension, doc_id, topic=law_education |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| source | str | data/metro_hanoi.txt | Giúp biết file nguồn và trace kết quả |
| extension | str | .txt | Phân biệt tài liệu text/markdown trong store |
| doc_id | str | metro_hanoi | Dùng để xóa hoặc nhóm chunk theo tài liệu |
| topic | str | metro, law_traffic, bus_city, online | Hỗ trợ `search_with_filter()` tăng độ chính xác cho query nhóm |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Kết quả chạy `ChunkingStrategyComparator().compare()` trên bộ tài liệu nhóm cho thấy:

| Tài liệu | Strategy | Chunk Count | Avg Length | Nhận xét |
|-----------|----------|-------------|------------|----------|
| bus_brt_hanoi.txt | FixedSizeChunker | 21 | 196.3 | Cắt đều nhưng có thể cắt ngang danh sách tuyến |
| bus_brt_hanoi.txt | SentenceChunker | 5 | 823.2 | Chunk dài, ít phù hợp với nội dung bảng/routing |
| bus_brt_hanoi.txt | RecursiveChunker | 59 | 68.6 | Chia nhỏ tốt, giữ được ranh giới mục |
| buyt_online_hanoi.txt | FixedSizeChunker | 10 | 184.6 | Cắt ổn cho văn bản mô tả nhưng vẫn hơi thô |
| buyt_online_hanoi.txt | SentenceChunker | 6 | 303.3 | Chunk khá dài, khó retrieve chi tiết |
| buyt_online_hanoi.txt | RecursiveChunker | 188 | 8.8 | Quá nhiều chunk nhỏ, dễ trùng lặp với đoạn ngắn |
| lich_trinh_buyt.txt | FixedSizeChunker | 411 | 199.9 | Nhiều chunk ổn định nhưng dễ cắt ngang thông tin chi tiết |
| lich_trinh_buyt.txt | SentenceChunker | 104 | 786.0 | Chunk quá dài để truy vấn nhanh |
| lich_trinh_buyt.txt | RecursiveChunker | 15254 | 4.4 | Quá nhiều chunk siêu ngắn, không hiệu quả cho retrieval |
| metro_hanoi.txt | FixedSizeChunker | 17 | 189.1 | Tốt cho nội dung trung bình |
| metro_hanoi.txt | SentenceChunker | 1 | 3212.0 | Quá dài, mất tính granular |
| metro_hanoi.txt | RecursiveChunker | 61 | 51.5 | Giữ được ranh giới phần và câu hợp lý |

### Strategy Của Tôi

**Loại:** RecursiveChunker

**Mô tả cách hoạt động:**
> `RecursiveChunker` cố gắng chia văn bản theo các separator ngữ nghĩa `\n\n`, `\n`, `. ` rồi ` ` trước khi fallback về chunk size. Điều này giúp giữ ranh giới đoạn và mục, đặc biệt phù hợp với tài liệu dạng danh sách và lộ trình.

**Tại sao chọn strategy này cho domain nhóm?**
> Tài liệu buýt và metro chứa cả đoạn mô tả và danh sách tuyến. RecursiveChunker giúp tách mỗi phần nhỏ hơn mà vẫn giữ ý nghĩa, nên cấp nguồn dữ liệu tốt hơn cho retrieval khi query cần chi tiết.

### So sánh hiệu quả

| Tài liệu | Strategy tốt nhất | Vì sao |
|-----------|------------------|--------|
| bus_brt_hanoi.txt | RecursiveChunker | Giữ được cấu trúc mục nhỏ, phù hợp tìm thông tin cụ thể |
| buyt_online_hanoi.txt | FixedSizeChunker | Vừa đủ chi tiết và không quá phân mảnh |
| lich_trinh_buyt.txt | FixedSizeChunker | Tránh tạo quá nhiều chunk siêu ngắn |
| metro_hanoi.txt | RecursiveChunker | Giữ ranh giới trạm và đoạn giới thiệu |

---

## 4. My Approach — Cá nhân (10 điểm)

### Chunking Functions

**`SentenceChunker.chunk`** — approach:
> Tôi dùng regex để split các câu theo dấu kết thúc như `. `, `! `, `? ` và `.
`. Mỗi câu được strip whitespace trước khi gom vào chunk. Điều này giảm lỗi tạo chunk trống và giữ nguyên ranh giới câu.

**`RecursiveChunker.chunk` / `_split`** — approach:
> Thuật toán đệ quy ưu tiên separator ngữ nghĩa và chỉ xuống separator thô khi cần. Base case là khi đoạn nhỏ hơn `chunk_size` hoặc khi không còn separator, lúc đó trả về đoạn hiện tại.

### EmbeddingStore

**`add_documents` + `search`** — approach:
> Tôi xây store in-memory bằng dict chứa `id`, `content`, `metadata`, `embedding`. Search dùng `query_embedding` và dot product để tính score. Nếu `chromadb` có sẵn, tôi cũng chuẩn bị đường chuyển sang collection thực.

**`search_with_filter` + `delete_document`** — approach:
> `search_with_filter` lọc metadata trước rồi search trên tập kết quả lọc. `delete_document` loại bỏ mọi record có `metadata['doc_id']` trùng với doc_id cần xóa.

### KnowledgeBaseAgent

**`answer`** — approach:
> Agent lấy top-k chunk từ store, tạo prompt với context từng chunk và câu hỏi, rồi gọi `llm_fn(prompt)`. Cách này giúp LLM có grounding vào nội dung đã retrieved.

### Test Results

```
42 passed
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Ghi chú |
|------|-----------|-----------|---------|--------------|--------|
| 1 | The bus departs at 6:00 AM. | Buses start service at six in the morning. | High | -0.141786 | Cặp cùng ý nghĩa nhưng mock score âm nhỏ |
| 2 | The metro is closed on Sunday. | The train operates daily. | Low | -0.013112 | Chủ đề liên quan nhưng không trùng ý chính |
| 3 | This document lists bus routes. | The recipe requires eggs and flour. | Low | -0.041125 | Hoàn toàn khác chủ đề |
| 4 | Station A is near the museum. | The museum is next to Station A. | High | -0.115539 | Cùng nội dung, đảo trật tự câu |
| 5 | Fare increases from next month. | Tickets cost 2 USD per ride. | Medium | -0.171365 | Cùng chủ đề vé/giá nhưng không cùng thông tin cụ thể |

**Nhận xét:**
> Tất cả điểm similarity trả về bởi `MockEmbedder` là giá trị nhỏ và một số là âm — điều này là do embedder giả định mang tính determinisitic và không phản ánh hoàn hảo semantic như embedding thực tế. Kết luận: để có đánh giá similarity chính xác cho retrieval, nên dùng backend embedding chất lượng (local `sentence-transformers` hoặc OpenAI) thay vì mock.

---

## 6. Results — Phase 2 Benchmark

### Benchmark Queries & Gold Answers

| Query ID | Query | Gold Answer | File chứa | Filter |
|----------|-------|-------------|-----------|--------|
| Q1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ? | Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long | `lich_trinh_buyt.txt`; `bus_brt_hanoi.txt` | Không |
| Q2 | Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ? | 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút | `metro_hanoi.txt` | `topic=metro` |
| Q3 | Quy định về việc ăn uống trên metro Hà Nội? | Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga | `quy_dinh_phap_luat.txt` | `topic=law_traffic` |
| Q4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn | `lich_trinh_buyt.txt`; `danh_sach_tuyen_buyt.txt` | `topic=bus_city` |
| Q5 | Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu? | Mức học bổng ≥ mức trần học phí hiện hành của ngành (Điều 7, Nghị định 66/2026) | `tai_lieu_phap_ly.txt` | `topic=law_education` |

### Kết quả benchmark top-3

| Query | Top-1 file | Score | Ghi chú |
|------|------------|-------|---------|
| Q1 | `customer_support_playbook.txt` | 0.188556 | Nhiễu, do mock embedding chưa tập trung vào nội dung bus |
| Q2 | `metro_hanoi.txt` | 0.153006 | Đúng file, filter topic hữu ích |
| Q3 | `quy_dinh_phap_luat.txt` | 0.150617 | Đúng file, filter topic hữu ích |
| Q4 | `lich_trinh_buyt.txt` | 0.018771 | File liên quan, nhưng top-1 vẫn chỉ sơ bộ vì query cụm từ chưa đủ mạnh |
| Q5 | `tai_lieu_phap_ly.txt` | 0.162131 | Đúng file, filter law_education hoạt động tốt |

### Detail retrieval results

- Q1: top-3 gồm `customer_support_playbook.txt`, `chunking_experiment_report.md`, `lich_trinh_buyt.txt`; chỉ vị trí 3 là đúng tài liệu nhóm cần.
- Q2: top-1 là `metro_hanoi.txt`, đúng file chứa thông tin tuyến và giờ hoạt động.
- Q3: top-1 là `quy_dinh_phap_luat.txt`, đúng file về quy định pháp luật và hạn chế ăn uống.
- Q4: top-1 là `lich_trinh_buyt.txt`, đúng file mục bus nhưng cần query chi tiết hơn để lọc đúng tuyến 32.
- Q5: top-1 là `tai_lieu_phap_ly.txt`, đúng file pháp lý; filter topic giúp tập trung.

### Quan sát bổ sung

- `search_with_filter()` rất hữu ích với `topic=metro`, `topic=law_traffic` và `topic=law_education`.
- Với query chung như Q1, `mock_embed` trả top-k nhiễu vì embeddings không đủ semantic. Điều này cho thấy cần dùng embedder chất lượng hoặc dữ liệu metadata cụ thể hơn.
- File nhóm cần thiết nên có metadata rõ ràng hơn (ví dụ `query_tags` hoặc `document_type`) để tránh retrieve nhầm tài liệu chung.

> Chi tiết kết quả benchmark được lưu tại `analysis/phase2_results.md`.

---

## 7. What I Learned — Failure Analysis & Insights

### Failure cases

- **Q1**: Top-2 retrieved không phải tài liệu lộ trình bus, vì query chứa nhiều thông tin định danh mà `mock_embed` lại ưu tiên nội dung chung. Đây là failure case do embedding quá generic và chưa đủ metadata chuyên dụng.
- **Q4**: Mặc dù trả về tài liệu bus, top-1 vẫn là một chunk chung từ `lich_trinh_buyt.txt` thay vì tuyến 32 cụ thể. Nguyên nhân là query không đủ chi tiết về đường đi hoặc metadata chưa phân biệt tuyến cụ thể.

### Đề xuất cải thiện

- Sử dụng `LocalEmbedder` hoặc OpenAI embedder để tăng chất lượng semantic khi truy vấn.
- Thêm metadata chi tiết hơn cho tài liệu bus, ví dụ `route_number`, `source_region`, `document_type`.
- Với `RecursiveChunker`, cân nhắc điều chỉnh `chunk_size` để tránh quá nhiều chunk siêu ngắn trong tài liệu dài như `lich_trinh_buyt.txt`.

### Bài học nhóm

- `search_with_filter()` giúp tăng precision khi metadata topic rõ ràng.
- Chunking strategy quan trọng: `FixedSizeChunker` vẫn tốt với dữ liệu dài có cấu trúc lặp, nhưng `RecursiveChunker` phù hợp với tài liệu đặt nặng về tiêu đề và danh sách.
- Phase 2 cần kết hợp cả chunking và metadata, không thể chỉ dựa vào embedding nếu dùng backend giả lập.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | / 10 |
| Chunking strategy | Nhóm | / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 4 / 5 |
| Results | Cá nhân | / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | / 5 |
| **Tổng** | | **/ 100** |
