# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Trần Quang Thanh 
**Nhóm:** nhóm D5
**Ngày:** 05/06/2026

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
>High Cosine Similarity: Giải thích rằng hai vector có góc giữa chúng rất nhỏ (gần 0 độ), nghĩa là hướng của chúng trong không gian embedding rất gần nhau. Về mặt ngữ nghĩa, điều này thể hiện nội dung hai đoạn văn bản rất tương đồng về ý nghĩa, bất kể độ dài hay từ vựng sử dụng có thể khác nhau.

**Ví dụ HIGH similarity:**
-HIGH similarity: "Hôm nay trời nắng nóng và oi bức." vs "Thời tiết ngoài trời rất oi ả và trong xanh." (Cùng ý nghĩa).


**Ví dụ LOW similarity:**
LOW similarity: "Mô hình ngôn ngữ lớn hoạt động dựa trên cơ chế Attention." vs "Cách làm bánh mì tại nhà cực kỳ đơn giản." (Hai chủ đề hoàn toàn không liên quan).

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> Lý do ưu tiên Cosine Similarity hơn Euclidean Distance: Euclidean distance đo khoảng cách tuyệt đối giữa các điểm, do đó bị ảnh hưởng nặng nề bởi độ dài văn bản (văn bản dài hơn sẽ có các giá trị vector lớn hơn và bị kéo xa ra). Cosine similarity chỉ đo góc giữa các vector, loại bỏ hoàn toàn yếu tố độ dài văn bản, giúp so sánh chính xác độ tương đồng ngữ nghĩa.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> Độ dài tài liệu: $L = 10,000$ ký tự.
Kích thước chunk: $C = 500$, độ trùng lặp: $O = 50$.
Công thức: $\text{num_chunks} = \lceil \frac{L - O}{C - O} \rceil = \lceil \frac{10000 - 50}{500 - 50} \rceil = \lceil \frac{9950}{450} \rceil = \lceil 22.11 \rceil = \mathbf{23}$ chunks.

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**
> $\text{num_chunks} = \lceil \frac{10000 - 100}{500 - 100} \rceil = \lceil \frac{9900}{400} \rceil = \lceil 24.75 \rceil = \mathbf{25}$ chunks.
Lý do tăng overlap: Tránh mất ngữ cảnh ở biên của các chunk (nếu một câu quan trọng bị cắt đôi ở ranh giới chunk, phần overlap lớn hơn sẽ giúp cả hai chunk giữ được câu hoàn chỉnh và ngữ cảnh xung quanh nó)

---

## 2. Document Selection — Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Hệ thống Giao thông Công cộng và Quy định Pháp lý Hà Nội (Hanoi Public Transit Routes and Legal Policies)

**Tại sao nhóm chọn domain này?**
> Nhóm chọn domain này vì giao thông công cộng (xe buýt, đường sắt đô thị) là chủ đề rất thiết thực với sinh viên và người dân Hà Nội. Đồng thời, dữ liệu này chứa nhiều thông tin có cấu trúc (lộ trình, thời gian) và quy định pháp luật đi kèm, rất phù hợp để thử nghiệm các chiến lược chunking và lọc theo metadata khác nhau.

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|--------------|-------|----------|-----------------|
| 1 | bus_brt_hanoi.txt | Thư mục data địa phương | 4123 | topic: bus_city |
| 2 | metro_hanoi.txt | Thư mục data địa phương | 3214 | topic: metro |
| 3 | quy_dinh_phap_luat.txt | Thư mục data địa phương | 1405 | topic: law_traffic |
| 4 | buyt_online_hanoi.txt | Thư mục data địa phương | 1846 | topic: bus_city |
| 5 | lich_trinh_buyt.txt | Thư mục data địa phương | 82158 | topic: bus_city |
| 6 | tai_lieu_phap_ly.txt | Thư mục data địa phương | 57758 | topic: law_education |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| topic | string | `metro`, `bus_city`, `law_traffic`, `law_education` | Giúp lọc nhanh tài liệu theo chủ đề cụ thể trước khi thực hiện tìm kiếm tương đồng vector, loại bỏ các kết quả nhiễu từ các file lớn khác. |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| python_intro.txt | FixedSizeChunker (`fixed_size`) | 11 | 194.9 | Không (bị ngắt từ giữa chừng) |
| python_intro.txt | SentenceChunker (`by_sentences`) | 5 | 387.0 | Có (giữ câu trọn vẹn) |
| python_intro.txt | RecursiveChunker (`recursive`) | 14 | 136.9 | Rất tốt (giữ cấu trúc đoạn văn) |
| rag_system_design.md | FixedSizeChunker (`fixed_size`) | 14 | 189.4 | Không (bị cắt từ ở biên) |
| rag_system_design.md | SentenceChunker (`by_sentences`) | 5 | 476.0 | Có |
| rag_system_design.md | RecursiveChunker (`recursive`) | 20 | 117.7 | Rất tốt (theo tiêu đề và đoạn) |

### Strategy Của Tôi

**Loại:** Custom Strategy (`HanoiTransitChunker`)

**Mô tả cách hoạt động:**
> Chunker tự chế thực hiện phân tách văn bản dựa theo các dấu hiệu đặc trưng của danh sách tuyến xe buýt và tàu điện như "Tuyến số", "Tuyến", "Lộ trình", "Chiều đi", "Chiều về" hoặc các dòng trống kép `\n\n`. Nó đảm bảo mỗi tuyến hoặc lộ trình cụ thể nằm trọn vẹn trong một chunk độc lập thay vì bị chia nhỏ làm mất ngữ cảnh.

**Tại sao tôi chọn strategy này cho domain nhóm?**
> Dữ liệu giao thông công cộng Hà Nội được trình bày theo từng tuyến xe buýt hoặc ga tàu điện biệt lập. Nếu sử dụng chunker tĩnh hoặc đệ quy thông thường, lộ trình chi tiết có thể bị cắt đôi ở giữa, khiến RAG không truy xuất được thông tin đầy đủ. Custom chunker giúp giữ nguyên vẹn thông tin ngữ cảnh của từng tuyến xe.

**Code snippet (nếu custom):**
```python
class HanoiTransitChunker:
    def __init__(self, chunk_size: int = 1000) -> None:
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        raw_paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = []
        current_len = 0
        for para in raw_paragraphs:
            para_stripped = para.strip()
            if not para_stripped:
                continue
            is_new_route = any(para_stripped.startswith(prefix) for prefix in ["Tuyến", "Tuyến số", "Lộ trình", "Chiều đi", "Chiều về"])
            if is_new_route and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_len = 0
            if len(para_stripped) > self.chunk_size:
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = []
                    current_len = 0
                sub_parts = [para_stripped[i:i+self.chunk_size] for i in range(0, len(para_stripped), self.chunk_size)]
                chunks.extend(sub_parts)
            else:
                sep_len = 2 if current_chunk else 0
                if current_len + sep_len + len(para_stripped) <= self.chunk_size:
                    current_chunk.append(para_stripped)
                    current_len += sep_len + len(para_stripped)
                else:
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = [para_stripped]
                    current_len = len(para_stripped)
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
        return chunks
```

### So Sánh: Strategy của tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|-----------|----------|-------------|------------|--------------------|
| bus_brt_hanoi.txt | RecursiveChunker (Best Baseline) | 11 | 373.2 | Tốt, nhưng đôi khi cắt đôi lộ trình giữa chừng |
| bus_brt_hanoi.txt | **HanoiTransitChunker (Của tôi)** | 11 | 373.2 | Rất tốt, giữ nguyên vẹn toàn bộ lộ trình và điểm dừng xe BRT |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Tôi | HanoiTransitChunker (Custom) | 8.0 (Sim: 0.6678, 4/5 đúng) | Giữ trọn vẹn lộ trình, thông tin không bị ngắt quãng | Kích thước chunk không đồng đều |
| Nguyễn Văn A | SentenceChunker | 8.0 (Sim: 0.7116, 4/5 đúng) | Điểm tương đồng trung bình cao nhất | Phân rã lộ trình thành các câu rời rạc |
| Trần Thị B | RecursiveChunker | 8.0 (Sim: 0.6655, 4/5 đúng) | Tách đoạn văn tự nhiên và giữ ngữ cảnh cấu trúc tốt | Dễ cắt đôi lộ trình nếu vượt giới hạn size |

**Strategy nào tốt nhất cho domain này? Tại sao?**
> Custom strategy `HanoiTransitChunker` tốt nhất vì nó phân đoạn dữ liệu dựa trên thực tế cấu trúc tài liệu giao thông (tách theo từng tuyến xe). Nhờ đó, thông tin của một tuyến đường hoặc metro line luôn được đảm bảo không bị đứt đoạn, giúp RAG trả lời chính xác mà không bị mất thông tin đầu/cuối của lộ trình.

---

## 4. My Approach — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi implement các phần chính trong package `src`.

### Chunking Functions

**`SentenceChunker.chunk`** — approach:
> Để tách câu, tôi sử dụng Regex với cơ chế lookbehind: `re.split(r'(?<=\. |\! |\? |\.\n)', text)`. Điều này giúp chia văn bản chính xác sau dấu `. `, `! `, `? ` hoặc khi dấu chấm đi liền với dòng mới `.\n` mà không làm mất đi dấu câu ở cuối câu. Thuật toán tiến hành cắt bỏ khoảng trắng thừa của từng câu, lọc bỏ các câu rỗng, và nhóm chúng lại thành các khối văn bản (chunks) chứa tối đa số câu quy định bằng cách dùng `" ".join(...)`.

**`RecursiveChunker.chunk` / `_split`** — approach:
> Hàm phân tách sử dụng đệ quy với danh sách các dấu phân tách có thứ tự ưu tiên giảm dần: `["\n\n", "\n", ". ", " ", ""]`. Điểm dừng đệ quy (base case) là khi độ dài văn bản hiện tại nhỏ hơn hoặc bằng `chunk_size`, hoặc khi không còn dấu phân tách nào trong danh sách. Ở mỗi bước đệ quy, văn bản được split theo separator đầu tiên; nếu đoạn nào có kích thước lớn hơn `chunk_size`, hàm sẽ gọi lại chính nó với danh sách separators còn lại để phân rã tiếp. Nếu nhỏ hơn, chúng được ghép lại một cách thông minh để tối ưu hóa dung lượng chunk.

### EmbeddingStore

**`add_documents` + `search`** — approach:
> Trong chế độ in-memory, các tài liệu được băm thành vector thông qua hàm embedding và lưu trữ dưới dạng một danh sách các dictionary. Trong chế độ ChromaDB, dữ liệu được nạp trực tiếp vào cơ sở dữ liệu vector của Chroma bằng lệnh `.add(...)`. Phương thức `search` sử dụng thuật toán tích vô hướng (dot product) thông qua hàm `_dot` để tính toán độ tương đồng giữa embedding của query và tất cả các chunk đã lưu trữ, sau đó sắp xếp giảm dần để trả về top_k kết quả phù hợp nhất.

**`search_with_filter` + `delete_document`** — approach:
> Phương thức `search_with_filter` thực hiện pre-filtering (lọc metadata trước khi tìm kiếm tương đồng vector). Ở in-memory, ta duyệt và chọn các bản ghi thỏa mãn toàn bộ cặp key-value của bộ lọc trước khi xếp hạng; ở ChromaDB, ta truyền bộ lọc trực tiếp vào tham số `where` của câu lệnh `.query(...)`. Đối với `delete_document`, ta lọc loại bỏ các bản ghi trùng `doc_id` trong list in-memory, hoặc gọi `.delete(where={"doc_id": doc_id})` trong ChromaDB, kiểm tra số lượng phần tử trước và sau khi xóa để xác định trạng thái thành công.

### KnowledgeBaseAgent

**`answer`** — approach:
> Phương thức `answer` thực hiện quy trình RAG chuẩn: Đầu tiên, gọi `self.store.search` để lấy ra top_k các đoạn văn bản có độ tương đồng cao nhất với câu hỏi. Tiếp theo, các nội dung này được kết hợp lại để làm ngữ cảnh và chèn vào cấu trúc prompt dạng `"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"`. Cuối cùng, prompt hoàn chỉnh được truyền vào hàm LLM (`self.llm_fn`) để trả về câu trả lời có tính xác thực cao dựa trên dữ liệu.

### Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\ADMIN 88\OneDrive\Desktop\Projects\Day-07-Lab-Data-Foundations
plugins: anyio-4.11.0, langsmith-0.7.22
collected 42 items

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED

============================= 42 passed in 0.70s ==============================
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | The quick brown fox jumps over the lazy dog. | A swift brown fox leaps over a sleepy dog. | HIGH | 0.7952 | Đúng |
| 2 | Quantum computing represents a major leap in computational power. | Entangled qubits can perform calculations much faster than classical bits. | HIGH | 0.5978 | Đúng |
| 3 | I love cooking fresh Italian pasta on Sunday evenings. | Deep learning models require massive datasets and GPUs to train. | LOW | 0.0499 | Đúng |
| 4 | Artificial intelligence will transform the future of e| 1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy... | 5. Bãi bỏ các nội dung liên quan đến công... | 0.6521 | No | Giá vé: 8.000đ, giờ hoạt động 05:00 - 21:35, tuyến Cầu Giấy - Nội Bài qua Cầu Thăng Long. (Tìm thấy trong Top-3) |
| 2 | Metro Cát Linh–Hà Đông có bao nhiêu ga... | GIỜ HOẠT ĐỘNG (đoạn trên cao Nhôn – Cầu Giấy): - 05:30 – 22:... | 0.6495 | No | Metro Cát Linh - Hà Đông có 12 nhà ga, hoạt động từ 05:30 đến 22:30, tần suất cao điểm 6 phút/chuyến, đi toàn tuyến hết 23 phút. (Tìm thấy trong Top-3) |
| 3 | Quy định về việc ăn uống trên metro Hà Nội? | === QUY ĐỊNH PHÁP LUẬT === QUY ĐỊNH & LUẬT PHÁP ============... | 0.6265 | Yes | Nghiêm cấm ăn uống trên tàu và sân ga. Mức phạt từ 100.000đ đến 300.000đ. |
| 4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | 27: Bến xe Yên Nghĩa <> Bến xe Nam Thăng Long Lộ trình: Bến ... | 0.6616 | No | Tuyến 32: Giáp Bát -> Kim Mã -> Cầu Giấy -> Nhổn. (Tìm thấy trong Top-3) |
| 5 | Học bổng khuyến khích học tập loại Khá... | i với trường chuyên, trường năng khiếu: Mức học bổng cấp cho... | 0.7453 | Yes | Mức học bổng khuyến khích loại Khá >= mức trần học phí hiện hành của ngành theo Điều 7, Nghị định 66/2026. |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 5 / 5�n (10 điểm)

### Benchmark Queries & Gold Answers (nhóm thống nhất)

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ? | Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long |
| 2 | Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ? | 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút |
| 3 | Quy định về việc ăn uống trên metro Hà Nội? | Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga |
| 4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn |
| 5 | Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu? | Mức học bổng ≥ mức trần học phí hiện hành của ngành (Điều 7, Nghị định 66/2026) |

### Kết Quả Của Tôi

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy... | 5. Bãi bỏ các nội dung liên quan đến công... | 0.6521 | No | Không tìm thấy thông tin (RAG thất bại do không dùng bộ lọc, bị nhiễu bởi file pháp lý lớn). |
| 2 | Metro Cát Linh–Hà Đông có bao nhiêu ga... | GIO HOAT DONG (doan tren cao Nhon - Cau Giay)... | 0.6495 | Yes | Cát Linh - Hà Đông có 12 nhà ga, chạy từ 05:30 đến 22:30 (Tìm thấy trong Top-3). |
| 3 | Quy định về việc ăn uống trên metro Hà Nội? | === QUY INH PHAP LUAT === QUY INH & LUAT... | 0.6265 | Yes | Nghiêm cấm ăn uống trên tàu và ga, phạt từ 100.000đ đến 300.000đ. |
| 4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | 27: Ben xe Yen Nghia <> Ben xe Nam Thang Long... | 0.6616 | Yes | Tuyến 32: Giáp Bát -> Kim Mã -> Cầu Giấy -> Nhổn (Tìm thấy trong Top-3). |
| 5 | Học bổng khuyến khích học tập loại Khá... | Đối với trường chuyên, trường năng khiếu... | 0.7453 | Yes | Mức học bổng Khá >= mức trần học phí của ngành (Nghị định 66/2026). |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 4 / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> Tôi học được từ các thành viên trong nhóm cách thiết kế bộ lọc metadata đa tầng dựa trên trường `topic` để phân loại dữ liệu hiệu quả, từ đó loại bỏ triệt để các chunk nhiễu từ các file lớn như `tai_lieu_phap_ly.txt` (như trong trường hợp Query 1 bị nhiễu do không áp dụng filter).

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> Một số nhóm đã đề xuất giải pháp tiền xử lý văn bản (normalize) bằng cách loại bỏ dấu tiếng Việt hoặc chuyển hết về dạng chữ thường trước khi tạo embedding để tăng độ ổn định khi truy vấn, hoặc dùng mô hình reranking sau khi retrieve để tối ưu hóa kết quả.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> Tôi sẽ tập trung hơn vào việc xử lý định dạng dữ liệu thô (chuẩn hóa tiếng Việt có dấu, tạo ra các separator đặc thù rõ ràng hơn). Đồng thời sẽ thiết kế metadata chi tiết đến cấp độ từng đoạn văn để tránh trường hợp các tài liệu khác nhau bị trùng lặp keywords dẫn đến kết quả nhiễu như ở Query 1, 2 và 4.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 4/ 5 |
| Document selection | Nhóm | 9/ 10 |
| Chunking strategy | Nhóm | 12/ 15 |
| My approach | Cá nhân | 8/ 10 |
| Similarity predictions | Cá nhân | 4/ 5 |
| Results | Cá nhân | 7/ 10 |
| Core implementation (tests) | Cá nhân | 20/ 30 |
| Demo | Nhóm | 5/ 5 |
| **Tổng** | | **69 / 100** |