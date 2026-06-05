# Báo Cáo Lab 7: Data Foundations

**Họ tên:** Hoàng Trọng Vĩnh  
**Nhóm:** Bàn D5  
**Ngày:** 05/06/2026

---

## 1. Warm-up

### 1.1. Cosine similarity

**High cosine similarity nghĩa là gì?**  
High cosine similarity nghĩa là hai vector embedding có hướng gần nhau trong không gian vector. Với dữ liệu văn bản, điều đó thường tương ứng với việc hai câu hoặc hai đoạn nói về nội dung giống nhau hoặc rất gần nhau về mặt ngữ nghĩa.

**Ví dụ high similarity**
- Câu A: `Metro Cát Linh - Hà Đông có 12 ga.`
- Câu B: `Tuyến 2A Cát Linh - Hà Đông gồm 12 nhà ga.`

Hai câu này cùng nói về một tuyến metro và cùng nhấn mạnh thông tin chính là số lượng ga, nên kỳ vọng similarity sẽ cao.

**Ví dụ low similarity**
- Câu A: `Xe buýt số 7 đi từ Cầu Giấy đến Nội Bài.`
- Câu B: `Học bổng loại Khá được tính theo mức trần học phí.`

Hai câu thuộc hai chủ đề khác nhau hoàn toàn: một câu về giao thông công cộng, một câu về chính sách học bổng. Vì vậy similarity kỳ vọng sẽ thấp.

**Vì sao cosine similarity phù hợp hơn Euclidean distance cho text embeddings?**  
Cosine similarity tập trung vào hướng của vector, tức là mức độ giống nhau về ý nghĩa, thay vì độ lớn tuyệt đối của vector. Với embedding văn bản, đây thường là thước đo phù hợp hơn vì hai đoạn có cùng ý nghĩa vẫn có thể có độ lớn vector khác nhau.

### 1.2. Chunking math

Với tài liệu dài `10.000` ký tự, `chunk_size=500`, `overlap=50`:

- `step = 500 - 50 = 450`
- `num_chunks = ceil((10000 - 500) / 450) + 1`
- `= ceil(9500 / 450) + 1`
- `= 22 + 1`
- `= 23`

**Kết quả:** `23 chunks`

Nếu tăng `overlap` lên `100`:

- `step = 500 - 100 = 400`
- `num_chunks = ceil((10000 - 500) / 400) + 1`
- `= ceil(9500 / 400) + 1`
- `= 24 + 1`
- `= 25`

Overlap lớn hơn giúp giữ ngữ cảnh tốt hơn giữa hai chunk liền kề, nhưng đồng thời làm tăng số chunk và chi phí retrieval.

---

## 2. Document Selection

### 2.1. Domain được chọn

Nhóm chọn domain **giao thông công cộng Hà Nội** kết hợp với **quy định/pháp lý liên quan**.

### 2.2. Lý do chọn

Mình thấy domain này phù hợp cho một bài lab về RAG vì:

- Có nhiều kiểu dữ liệu khác nhau: lịch trình xe buýt, danh sách tuyến, metro, BRT, quy định đi metro và văn bản pháp lý.
- Có thể tạo được các câu hỏi retrieval rất đa dạng: giá vé, giờ hoạt động, tuyến đường, quy định cấm, điều khoản học bổng.
- Metadata khá rõ ràng, thuận lợi cho filtering theo `topic`, `transport_type`, `route_no`, `article_no`, `section`.

### 2.3. Data inventory

| # | Tài liệu | Vai trò | Số ký tự | Metadata chính |
|---|---|---|---:|---|
| 1 | `lich_trinh_buyt.txt` | Lộ trình xe buýt chi tiết | 82158 | `topic=bus_city`, `category=route_schedule`, `city=hanoi`, `transport_type=bus` |
| 2 | `danh_sach_tuyen_buyt.txt` | Danh sách tuyến và giờ hoạt động | 16825 | `topic=bus_city`, `category=route_schedule`, `city=hanoi`, `transport_type=bus` |
| 3 | `bus_brt_hanoi.txt` | Một số tuyến buýt/BRT quan trọng | 4123 | `topic=bus_city`, `category=route_schedule`, `city=hanoi`, `transport_type=bus` |
| 4 | `metro_hanoi.txt` | Thông tin metro Hà Nội | 3214 | `topic=metro`, `category=route_schedule`, `city=hanoi`, `transport_type=metro` |
| 5 | `quy_dinh_phap_luat.txt` | Quy định đi xe buýt/metro | 1405 | `topic=law_traffic`, `category=regulation`, `city=hanoi` |
| 6 | `tai_lieu_phap_ly.txt` | Văn bản pháp lý giáo dục | 57758 | `topic=law_education`, `category=legal_document`, `city=hanoi` |

Trong benchmark, script chỉ dùng 6 file này và bỏ qua `benchmark_queries.md` cùng các file ngoài tập benchmark chính.

### 2.4. Metadata schema

| Trường | Kiểu | Ví dụ | Ý nghĩa |
|---|---|---|---|
| `doc_id` | `str` | `lich_trinh_buyt` | Xác định tài liệu gốc |
| `source` | `str` | `metro_hanoi.txt` | Truy vết kết quả về đúng file |
| `topic` | `str` | `metro` | Hỗ trợ filter theo nhóm chủ đề |
| `category` | `str` | `route_schedule` | Phân biệt lịch trình, quy định, pháp lý |
| `city` | `str` | `hanoi` | Có ích nếu mở rộng đa thành phố |
| `transport_type` | `str` | `bus` | Tách xe buýt với metro |
| `route_no` | `str` | `32` | Hỗ trợ query theo số tuyến |
| `route_no_norm` | `str` | `7` | Chuẩn hóa `7` và `07` |
| `section` | `str` | `quy_dinh_di_metro` | Hữu ích cho tài liệu dạng quy định |
| `article_no` | `str` | `7` | Hữu ích cho văn bản pháp lý |
| `clause_no` | `str` | `3` | Tăng độ chính xác khi hỏi theo điều/khoản |

---

## 3. Chunking Strategy

### 3.1. Ba chiến lược đã so sánh

Mình benchmark 4 hướng:

| Strategy | Cấu hình / ý tưởng | Số chunk |
|---|---|---:|
| `fixed_size` | `chunk_size=500`, `overlap=50` | 372 |
| `sentence` | `max_sentences_per_chunk=5` | 132 |
| `recursive` | `chunk_size=500`, tách đệ quy theo separator | 405 |
| `domain_aware` | chunk theo cấu trúc domain + reranking lai | 249 |

Trong đó, `domain_aware` là phiên bản tối ưu thêm ở Phase 2:

- Gom các mẩu thông tin cùng tuyến thành `bus_route_aggregate`
- Tách tài liệu pháp lý theo `Điều`, `Khoản`, và với Điều 7 còn tách sâu tới `điểm a/b/c`
- Dùng hybrid reranking dựa trên embedding score, lexical overlap, metadata bonus và completeness bonus

### 3.2. Kết quả benchmark content-level

Theo `report/phase2_benchmark_results_optimized_v2.md`:

| Strategy | Top-1 Content Correct | Top-3 Content Correct |
|---|---:|---:|
| `fixed_size` | 4 / 5 | 4 / 5 |
| `sentence` | 4 / 5 | 4 / 5 |
| `recursive` | 2 / 5 | 2 / 5 |
| `domain_aware` | 4 / 5 | 4 / 5 |

### 3.3. Strategy mình chọn

Mình chọn **`domain_aware`** là hướng phù hợp nhất để trình bày trong báo cáo, dù điểm content-level đang **đồng hạng cao nhất** với `fixed_size` và `sentence`.

Lý do:

- Nó phản ánh đúng tinh thần RAG hơn: không chỉ cắt theo độ dài mà còn tận dụng cấu trúc của dữ liệu.
- Nó cải thiện rõ Q5 nhờ tách đúng `Điều 7`, `Khoản 3`, và các điểm con.
- Nó cho kết quả dễ giải thích hơn vì metadata bám sát domain thật như `route_no_norm`, `article_no`, `clause_no`, `section`.

### 3.4. So sánh ngắn với các strategy khác

**So với `fixed_size`**  
`fixed_size` rất ổn định và đơn giản, nhưng vẫn có xu hướng đưa về chunk đúng file mà chưa chắc đúng đúng đoạn cần trả lời. Nó mạnh ở baseline, nhưng kém “giải thích được” hơn khi phân tích theo domain.

**So với `sentence`**  
`sentence` giữ câu tốt, và ở benchmark này cho kết quả khá đẹp. Tuy nhiên, khi dữ liệu có nhiều bullet, OCR dài hoặc format không đều, strategy này vẫn phụ thuộc mạnh vào cách xuống dòng/cấu trúc câu trong file gốc.

**So với `recursive`**  
`recursive` có ý tưởng tốt nhưng trong dữ liệu thực tế của nhóm chưa tận dụng hết được lợi thế. Đặc biệt với các query cần đúng route hoặc đúng điều khoản pháp lý, nó vẫn thua khá rõ.

---

## 4. My Approach

### 4.1. Chunking

Trong `src/chunking.py`, mình implement:

- `SentenceChunker.chunk`: tách câu bằng regex, giữ dấu câu, gom theo số câu tối đa mỗi chunk.
- `RecursiveChunker.chunk` và `_split`: tách đệ quy theo thứ tự `\n\n`, `\n`, `. `, `" "`, rồi fallback cắt cứng.
- `compute_similarity`: cosine similarity với xử lý an toàn cho vector rỗng hoặc norm bằng 0.
- `ChunkingStrategyComparator.compare`: so sánh các strategy built-in và trả về thống kê theo format test yêu cầu.

### 4.2. Store

Trong `src/store.py`, mình hoàn thiện:

- Lưu record in-memory gồm `content`, `text`, `metadata`, `embedding`, `document`
- `add_documents`
- `search`
- `search_with_filter`
- `get_collection_size`
- `delete_document`

Điểm chính là search có thể hoạt động ổn định với mock embedding và metadata filter đơn giản, đủ cho bài lab.

### 4.3. Agent

Trong `src/agent.py`, mình implement `KnowledgeBaseAgent` theo hướng RAG tối giản:

- Retrieve từ store bằng `search(question, top_k=top_k)`
- Gom context từ `content`, `text`, hoặc `document.content`
- Tạo prompt dạng context + question
- Gọi `llm_fn(prompt)`
- Có fallback để luôn trả về chuỗi không rỗng

### 4.4. Kết quả test

```bash
python -m pytest tests/ -v
```

**Kết quả:** `42 passed`

Điều này cho thấy phần core implementation trong `src/` đã đạt yêu cầu của bộ test cung cấp.

---

## 5. Similarity Predictions

Mình dùng `_mock_embed` kết hợp với `compute_similarity()` để tính điểm thật cho 5 cặp câu.

| Pair | Sentence A | Sentence B | Dự đoán | Actual score | Đúng? |
|---|---|---|---|---:|---|
| 1 | Metro Cát Linh - Hà Đông có 12 ga. | Tuyến 2A có tổng cộng 12 nhà ga. | High | -0.2011 | Không |
| 2 | Xe buýt số 7 đi từ Cầu Giấy đến Nội Bài. | Tuyến 07 kết nối Cầu Giấy với sân bay Nội Bài. | High | -0.0541 | Không |
| 3 | Không được ăn uống trên metro. | Hành khách bị cấm ăn uống trong tàu và sân ga. | High | 0.1375 | Có |
| 4 | Tuyến 32 đi Nhổn. | Học bổng loại Khá căn cứ mức trần học phí. | Low | -0.0406 | Có |
| 5 | BRT Kim Mã - Yên Nghĩa có làn đường riêng. | Danh hiệu Tiến sĩ danh dự không thay thế học vị. | Low | -0.0514 | Có |

Điều bất ngờ nhất là hai cặp mình dự đoán “high” ở Pair 1 và Pair 2 lại ra điểm âm. Điều này cho thấy `_mock_embed` chỉ phù hợp để test pipeline và API, chứ chưa đủ mạnh để phản ánh quan hệ ngữ nghĩa thật như một embedding model thực tế.

---

## 6. Results

### 6.1. Bộ benchmark của nhóm

| ID | Query | Gold answer |
|---|---|---|
| Q1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ? | Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long. |
| Q2 | Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ? | 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút. |
| Q3 | Quy định về việc ăn uống trên metro Hà Nội? | Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga. |
| Q4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn. |
| Q5 | Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu? | Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026. |

### 6.2. Kết quả strategy mình chọn: `domain_aware`

| ID | Top-1 source | Top-1 Content Correct? | Top-3 Content Correct? | Ghi chú |
|---|---|---|---|---|
| Q1 | `lich_trinh_buyt.txt` | Yes | Yes | Route 7 đã được kéo đúng lên Top-1 sau khi tăng ưu tiên exact route |
| Q2 | `metro_hanoi.txt` | Yes | Yes | Chunk metro section trả lời được cả số ga và giờ hoạt động |
| Q3 | `quy_dinh_phap_luat.txt` | Yes | Yes | Chunk đúng section `quy_dinh_di_metro` |
| Q4 | `lich_trinh_buyt.txt` | No | No | Vẫn còn bị nhiễu giữa các tuyến buýt có lộ trình gần nhau |
| Q5 | `tai_lieu_phap_ly.txt` | Yes | Yes | Chunk pháp lý tách theo Điều 7/Khoản 3 hoạt động tốt |

### 6.3. Tổng kết benchmark v2

- `domain_aware`: `Top-1 Content Correct = 4/5`
- `domain_aware`: `Top-3 Content Correct = 4/5`
- `Expected file hit in Top-3 = 5/5`

Mình xem đây là một kết quả khá tốt cho một pipeline không dùng API thật và không dùng embedding model ngoài. Điểm còn yếu nhất hiện tại là Q4, vì dữ liệu xe buýt có nhiều tuyến chia sẻ một phần hành trình giống nhau nên rất dễ gây nhiễu.

### 6.4. So sánh trước và sau tối ưu

Sau khi thêm `domain_aware` chunking và hybrid reranking:

- Q1 được cải thiện rõ nhờ `bus_route_aggregate` và ưu tiên exact `route_no_norm=7`
- Q5 được cải thiện rõ nhờ tách theo `article_no=7`, `clause_no=3` và các điểm con
- Q4 vẫn là truy vấn khó nhất vì nhiều tuyến xe buýt có bối cảnh gần giống nhau

Điểm mình rút ra là: **đúng file chưa đủ**, mà cần **đúng chunk và đúng đoạn thông tin** để trả lời tốt ở mức RAG.

---

## 7. What I Learned

Điều quan trọng nhất mình học được từ lab này là retrieval quality phụ thuộc rất mạnh vào cách chia chunk và cách biểu diễn metadata. Cùng một bộ dữ liệu, chỉ cần đổi chiến lược chunking và reranking là chất lượng content-level có thể thay đổi đáng kể, dù source-level trông có vẻ vẫn “đúng”.

Nếu làm lại từ đầu, mình sẽ:

- Chuẩn hóa dữ liệu xe buýt theo từng tuyến ngay từ bước ingest
- Tách văn bản pháp lý theo điều/khoản/điểm sớm hơn
- Dùng embedding model thật thay cho `_mock_embed`
- Bổ sung thêm metric như `MRR`, `Top-1 exact answer hit`, hoặc `answer faithfulness`

---

## 8. Tự Đánh Giá

| Hạng mục | Điểm |
|---|---:|
| Cá nhân | 57 / 60 |
| Nhóm | 35 / 40 |
| **Tổng** | **92 / 100** |

Ghi chú: Điểm tự đánh giá cuối cùng được chốt trực tiếp theo thang 100, trong đó phần cá nhân là `57/60`, phần nhóm là `35/40`, và tổng là `92/100`.
