# Báo Cáo Kết Quả Nhóm (Group Report) - Phase 2
**Môn học:** Lab 7 - Embedding & Vector Store (Day 07)  
**Nhóm:** D5  
**Thành viên:** Đỗ Đức Tuệ, Nguyễn Thái Dương, Nguyễn Hải Quân, Trần Quang Thanh, Dương Thế Linh ,Hoàng Trọng Vĩnh
**Ngày thực hiện:** 05/06/2026  

---

## 1. Warm-up: Khái Niệm Cơ Bản (Embedding & Chunking)

### Cosine Similarity (Độ tương đồng Cosine)
* **Khái niệm:** Cosine similarity đo góc giữa hai vector trong không gian nhiều chiều, có giá trị trong khoảng từ -1 đến 1. Điểm càng gần 1 thể hiện hai vector có cùng hướng (tương đồng cao về ngữ nghĩa).
* **Ưu điểm so với Euclidean Distance:** Cosine similarity chỉ tập trung vào hướng của vector thay vì độ lớn (magnitude). Trong xử lý văn bản, điều này cực kỳ quan trọng vì hai đoạn văn bản có độ dài rất khác nhau (ví dụ: một câu ngắn và một đoạn văn dài) nhưng cùng nói về một chủ đề vẫn có vector chỉ cùng hướng, giúp tránh lỗi do độ dài văn bản gây ra như khi dùng Euclidean distance.
* **Ví dụ tương đồng cao (High similarity):**
  * *Câu A:* "Xe buýt số 7 đi từ Cầu Giấy đến Nội Bài."
  * *Câu B:* "Tuyến buýt 7 kết nối Cầu Giấy với sân bay Nội Bài."
  * *Giải thích:* Cả hai câu đều chia sẻ cùng thực thể (tuyến 7, Cầu Giấy, Nội Bài) và mục đích di chuyển.
* **Ví dụ tương đồng thấp (Low similarity):**
  * *Câu A:* "Metro Cát Linh - Hà Đông có 12 ga tàu điện."
  * *Câu B:* "Sinh viên đại học được nhận học bổng nếu xếp loại Khá."
  * *Giải thích:* Hai câu thuộc hai lĩnh vực hoàn toàn độc lập (giao thông đô thị và chính sách giáo dục).

### Chunking Math (Toán học phân đoạn)
Với một tài liệu dài $10.000$ ký tự:
1. **Cấu hình 1:** `chunk_size = 500`, `overlap = 50`.
   * Kích thước bước dịch (step) = $500 - 50 = 450$ ký tự.
   * Số lượng chunk = $\lceil \frac{10000 - 50}{450} \rceil = \lceil 22.11 \rceil = \mathbf{23}$ chunks.
2. **Cấu hình 2:** `chunk_size = 500`, `overlap = 100`.
   * Kích thước bước dịch (step) = $500 - 100 = 400$ ký tự.
   * Số lượng chunk = $\lceil \frac{10000 - 100}{400} \rceil = \lceil 24.75 \rceil = \mathbf{25}$ chunks.
   * *Ý nghĩa của việc tăng overlap:* Giúp giữ ngữ cảnh ở ranh giới giữa các chunk. Nếu một thông tin quan trọng bị cắt đôi, phần trùng lặp lớn hơn sẽ giúp cả hai chunk liền kề đều chứa thông tin hoàn chỉnh, từ đó tăng độ chính xác khi truy vấn.

---

## 2. Thiết Kế Bộ Dữ Liệu Nhóm (Document Selection)

### Lựa chọn Domain & Lý do
Nhóm thống nhất chọn domain: **Hệ thống Giao thông công cộng Hà Nội và Quy định Pháp lý liên quan**.
* *Lý do chọn:* Đây là một domain mang tính thực tế cao, chứa cả dữ liệu có cấu trúc dạng bảng/danh sách (lịch trình, các nhà ga) và dữ liệu văn bản hành chính dài (các điều khoản nghị định, quy định xử phạt). Cấu trúc hỗn hợp này rất thích hợp để thử nghiệm giới hạn của các chiến lược chunking khác nhau.

### Data Inventory (Danh mục tài liệu)

Nhóm sử dụng bộ dữ liệu gồm 7 tài liệu chính:

| # | Tên tài liệu | Nguồn gốc | Số ký tự ≈ | Metadata đã gán | Mục tiêu kiểm thử |
|---|--------------|-----------|------------|-----------------|-------------------|
| 1 | `bus_brt_hanoi.txt` | Transerco/timbus.vn | 5.238 | `source: bus_brt`, `type: route_info`, `topic: bus_airport_brt` | Tuyến sân bay Nội Bài & BRT |
| 2 | `buyt_online_hanoi.txt` | Internet | 2.397 | `source: buyt_online`, `type: route_info`, `topic: bus_city` | Các tuyến buýt nội đô phổ biến |
| 3 | `danh_sach_tuyen_buyt.txt` | Excel export | 20.666 | `source: danh_sach_tuyen`, `type: route_list`, `topic: bus_city` | Danh sách tóm tắt mã tuyến và giá vé |
| 4 | `lich_trinh_buyt.txt` | Transerco | 105.527 | `source: lich_trinh_buyt`, `type: route_detail`, `topic: bus_city` | Dữ liệu cực lớn, lộ trình chi tiết từng tuyến |
| 5 | `metro_hanoi.txt` | metrohanoi.com.vn | 4.128 | `source: metro_hanoi`, `type: route_info`, `topic: metro` | Thông tin ga tàu điện Nhổn & Cát Linh |
| 6 | `quy_dinh_phap_luat.txt` | Nghị định 100/2019 | 1.758 | `source: quy_dinh`, `type: regulation`, `topic: law_traffic` | Quy định cấm ăn uống, xử phạt |
| 7 | `tai_lieu_phap_ly.txt` | Nghị định 66/2026 | 77,755 | `source: tai_lieu_phap_ly`, `type: legal_doc`, `topic: law_education` | Văn bản luật giáo dục dài, phức tạp |

### Metadata Schema
* `source` (string): Tên file nguồn dùng để truy vết dữ liệu (grounding).
* `type` (string): Định dạng tài liệu (`route_info`, `route_list`, `route_detail`, `regulation`, `legal_doc`).
* `topic` (string): Nhãn phân loại miền tri thức (`bus_airport_brt`, `bus_city`, `metro`, `law_traffic`, `law_education`) dùng để lọc dữ liệu trước khi search (`search_with_filter`), tránh hiện tượng nhiễu chéo domain.

---

## 3. So Sánh Các Chiến Lược Chunking (Strategy Analysis)

### Số lượng chunk được tạo ra thực tế
Khi áp dụng các chiến lược chunking của các thành viên lên 7 file dữ liệu:

| Tài liệu | SentenceChunck (Linh) | Recursive 500 (Dương/Tuệ) | FixedSize 400, ol=80 (Baseline) | Recursive 2500 (Quân) | Custom HanoiTransit (Thanh) |
|---|:---:|:---:|:---:|:---:|:---:|
| `bus_brt_hanoi.txt` | 22 | 30 | 13 | 3 | 11 |
| `buyt_online_hanoi.txt` | 10 | 7 | 6 | 1 | 4 |
| `danh_sach_tuyen_buyt.txt` | 161 | 136 | 53 | 9 | 22 |
| `lich_trinh_buyt.txt` | 855 | **3.397** ⚠️ | 257 | 43 | 95 |
| `metro_hanoi.txt` | 22 | 33 | 10 | 2 | 8 |
| `quy_dinh_phap_luat.txt` | 16 | 11 | 5 | 1 | 3 |
| `tai_lieu_phap_ly.txt` | 77 | **1.024** ⚠️ | 181 | 32 | 48 |
| **Tổng số Chunks** | **1.163** | **4.638** | **525** | **91** | **191** |

---

## 4. Kết Quả Benchmark Trên 5 Queries Nhóm Thống Nhất

Nhóm đã sử dụng bộ 5 queries chuẩn kèm câu trả lời mẫu (Gold Answer) để kiểm thử hiệu năng retrieval của từng thành viên:

* **Q1:** "Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?" (Gold: Giá 8.000đ, chạy 05:00-21:35, Cầu Giấy-Nội Bài)
* **Q2:** "Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?" (Gold: 12 ga, chạy 05:30-22:30, cao điểm 6 phút/chuyến)
* **Q3:** "Quy định về việc ăn uống trên metro Hà Nội?" (Gold: Nghiêm cấm, phạt 100.000-300.000đ trong tàu/ga)
* **Q4:** "Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?" (Gold: Tuyến 32: Giáp Bát -> Kim Mã -> Cầu Giấy -> Nhổn)
* **Q5:** "Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?" (Gold: >= mức trần học phí hiện hành của ngành)

### Kết quả so sánh điểm số retrieval (Top-3)

| Query ID | Filter áp dụng | SentenceChunck (Linh) | Recursive 500 (Tuệ/Dương) | FixedSize 400, ol=80 | Recursive 2500 + Gemini (Quân) | Custom HanoiTransit (Thanh) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Q1** | Không | 2/2 (Đúng) | 0/2 (Sai) | 2/2 (Đúng) | 2/2 (Đúng) | 0/2 (Sai) |
| **Q2** | `topic=metro` | 2/2 (Đúng) | 2/2 (Đúng) | 2/2 (Đúng) | 2/2 (Đúng) | 2/2 (Đúng) |
| **Q3** | `topic=law_traffic` | 2/2 (Đúng) | 0/2 (Sai) | 2/2 (Đúng) | 2/2 (Đúng) | 2/2 (Đúng) |
| **Q4** | `topic=bus_city` | 2/2 (Đúng) | 0/2 (Sai) | 2/2 (Đúng) | 2/2 (Đúng) | 2/2 (Đúng) |
| **Q5** | `topic=law_education` | 0/2 (Sai) | 2/2 (Đúng) | 2/2 (Đúng) | 2/2 (Đúng) | 2/2 (Đúng) |
| **Tổng** | | **8 / 10** | **4 / 10** | **10 / 10** | **10 / 10** | **8 / 10** |

---

## 5. Phân Tích Các Failure Cases & Bài Học Kinh Nghiệm

### Failure Case 1: Lỗi bùng nổ số lượng chunk gây nhiễu (Recursive 500)
* *Nguyên nhân:* Việc đặt `chunk_size` quá nhỏ (500) đối với các file dữ liệu lớn như `lich_trinh_buyt.txt` (103KB) tạo ra tới gần 3.400 chunks. Khi dùng MockEmbedder (MD5), các vector được sinh ra ngẫu nhiên và không mang tính ngữ nghĩa. Với số lượng chunk quá lớn, xác suất xuất hiện các chunk sai (false positive) có điểm số mock cao hơn chunk đúng tăng vọt, lấn át kết quả ở Q1, Q3, Q4.
* *Bài học:* Khi lượng dữ liệu lớn, cần tăng kích thước chunk (`chunk_size=800+` hoặc `2500`) hoặc phải áp dụng filter metadata một cách triệt để nhằm thu hẹp không gian tìm kiếm trước khi tính độ tương đồng.

### Failure Case 2: Regex của Chunker theo câu bị lỗi trước dấu chấm viết tắt (SentenceChunker)
* *Nguyên nhân:* `SentenceChunker` tách câu dựa trên dấu chấm kết câu `.`. Tuy nhiên, văn bản pháp luật thường xuyên sử dụng các dấu chấm viết tắt dạng mục lục như `a.`, `b.`, `khoản 1.`.
* *Hậu quả:* Một điều khoản luật hoàn chỉnh (Q5) bị băm nhỏ thành các dòng rác như "a.", "b.", làm biến dạng ngữ nghĩa của đoạn văn bản và khiến retrieval thất bại.
* *Bài học:* Đối với văn bản luật và hành chính, chiến lược chunking dựa trên dòng mới `\n` hoặc từ khóa bắt đầu điều khoản (`Điều 1`, `Điều 2`) hiệu quả hơn nhiều so với việc tách câu theo dấu chấm đơn thuần.

### Failure Case 3: Tài liệu dạng danh sách không có dấu kết thúc câu
* *Nguyên nhân:* Dữ liệu lịch trình và nhà ga BRT/Metro thường được liệt kê dạng danh sách gạch đầu dòng, kết thúc bằng dấu xuống dòng hoặc ký tự đặc biệt (`<>`, `→`), không có dấu chấm câu.
* *Hậu quả:* `SentenceChunker` không tìm thấy ranh giới câu và coi cả file là một chunk khổng lồ, làm mất đi khả năng tìm kiếm chi tiết (granularity).
* *Bài học:* Cần xây dựng custom chunker (như `HanoiTransitChunker`) có thể tự phát hiện các ký tự đặc biệt của domain (như "Tuyến", "Lộ trình", "Chiều đi") để cắt chunk chính xác.

### Failure Case 4: Sự khác biệt giữa Mock Embedding và Semantic Embedding thật
* *Nguyên nhân:* `MockEmbedder` chỉ tạo vector từ mã hash của text. Các cặp câu có nghĩa rất gần nhau lại bị chấm điểm rất thấp (thậm chí âm).
* *Minh chứng vượt trội:* Khi thành viên Nguyễn Hải Quân chạy thử nghiệm với Gemini Embedding thật (`gemini-embedding-2`), toàn bộ 5 queries đều đạt điểm số tương đồng rất cao (0.68 - 0.77) và trả về chính xác 100% chunk liên quan trong top-1.
* *Bài học:* Mock embedding chỉ dùng để kiểm thử tính đúng đắn của code (unit test), bắt buộc phải có mô hình embedding ngữ nghĩa thực tế để đánh giá chất lượng hệ thống RAG.

---

## 6. Đề Xuất Cải Tiến Cho Hệ Thống RAG

1. **Ứng dụng Metadata Filtering sớm:** Phải luôn thiết kế metadata phân loại rõ ràng và thực hiện lọc dữ liệu trước khi chạy thuật toán tìm kiếm tương đồng vector (`search_with_filter`).
2. **Chọn Chunker phù hợp cho từng loại tài liệu (Hybrid Chunking):**
   * Đối với danh sách tuyến xe buýt: Sử dụng custom chunker (`HanoiTransitChunker`) để giữ trọn vẹn thông tin từng tuyến.
   * Đối với văn bản quy định pháp luật: Dùng `RecursiveChunker` với cấu hình separator ưu tiên ngắt dòng `\n` để tránh lỗi dấu chấm viết tắt.
   * Đối với tài liệu thông thường: `FixedSizeChunker(400, overlap=80)` là lựa chọn an toàn và cân bằng nhất.
3. **Chuyển đổi sang Embedding ngữ nghĩa thực tế:** Sử dụng các mô hình local (như `sentence-transformers`) hoặc API (như Gemini) thay thế cho mock embedder để đảm bảo khả năng tìm kiếm thông tin theo ngữ nghĩa thực tế.
