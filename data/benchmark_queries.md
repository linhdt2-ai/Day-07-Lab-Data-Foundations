# Benchmark Queries — Phase 2

Bộ benchmark này dùng cho **Lab 7 — Phase 2: So sánh Retrieval Strategy**.

Chủ đề dữ liệu: giao thông công cộng Hà Nội và quy định/pháp lý liên quan.

## Danh sách benchmark queries

| Query ID | Query | Gold Answer | File chứa | Filter |
|---|---|---|---|---|
| Q1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ? | Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long. | `lich_trinh_buyt.txt`; `bus_brt_hanoi.txt` | Không |
| Q2 | Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ? | 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút. | `metro_hanoi.txt` | `topic=metro` |
| Q3 | Quy định về việc ăn uống trên metro Hà Nội? | Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga. | `quy_dinh_phap_luat.txt` | `topic=law_traffic` |
| Q4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn. | `lich_trinh_buyt.txt`; `danh_sach_tuyen_buyt.txt` | `topic=bus_city` |
| Q5 | Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu? | Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026. | `tai_lieu_phap_ly.txt` | `topic=law_education` |

---

## Chi tiết từng query

### Q1 — Xe buýt số 7 Nội Bài – Cầu Giấy

**Question:**  
Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?

**Gold Answer:**  
Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.

**Expected relevant files:**  
- `lich_trinh_buyt.txt`
- `bus_brt_hanoi.txt`

**Filter:**  
Không

---

### Q2 — Metro Cát Linh – Hà Đông

**Question:**  
Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?

**Gold Answer:**  
12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.

**Expected relevant files:**  
- `metro_hanoi.txt`

**Filter:**  
`topic=metro`

---

### Q3 — Quy định ăn uống trên metro Hà Nội

**Question:**  
Quy định về việc ăn uống trên metro Hà Nội?

**Gold Answer:**  
Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.

**Expected relevant files:**  
- `quy_dinh_phap_luat.txt`

**Filter:**  
`topic=law_traffic`

---

### Q4 — Tuyến từ Bến xe Giáp Bát đến Nhổn

**Question:**  
Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?

**Gold Answer:**  
Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.

**Expected relevant files:**  
- `lich_trinh_buyt.txt`
- `danh_sach_tuyen_buyt.txt`

**Filter:**  
`topic=bus_city`

---

### Q5 — Học bổng khuyến khích học tập loại Khá

**Question:**  
Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?

**Gold Answer:**  
Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.

**Expected relevant files:**  
- `tai_lieu_phap_ly.txt`

**Filter:**  
`topic=law_education`

---

## Bảng ghi kết quả benchmark

| Query ID | Strategy | Top-1 đúng? | Top-3 có chunk liên quan? | Score Top-1 | Source Top-1 | Nhận xét |
|---|---|---:|---:|---:|---|---|
| Q1 | FixedSizeChunker |  |  |  |  |  |
| Q1 | SentenceChunker |  |  |  |  |  |
| Q1 | RecursiveChunker |  |  |  |  |  |
| Q2 | FixedSizeChunker |  |  |  |  |  |
| Q2 | SentenceChunker |  |  |  |  |  |
| Q2 | RecursiveChunker |  |  |  |  |  |
| Q3 | FixedSizeChunker |  |  |  |  |  |
| Q3 | SentenceChunker |  |  |  |  |  |
| Q3 | RecursiveChunker |  |  |  |  |  |
| Q4 | FixedSizeChunker |  |  |  |  |  |
| Q4 | SentenceChunker |  |  |  |  |  |
| Q4 | RecursiveChunker |  |  |  |  |  |
| Q5 | FixedSizeChunker |  |  |  |  |  |
| Q5 | SentenceChunker |  |  |  |  |  |
| Q5 | RecursiveChunker |  |  |  |  |  |

---

## Gợi ý metadata filter

Khi tạo `Document`, có thể gắn metadata theo file như sau:

| File | Metadata gợi ý |
|---|---|
| `lich_trinh_buyt.txt` | `topic=bus_city`, `transport_type=bus`, `city=hanoi` |
| `danh_sach_tuyen_buyt.txt` | `topic=bus_city`, `transport_type=bus`, `city=hanoi` |
| `bus_brt_hanoi.txt` | `topic=bus_city`, `transport_type=bus`, `city=hanoi` |
| `metro_hanoi.txt` | `topic=metro`, `transport_type=metro`, `city=hanoi` |
| `quy_dinh_phap_luat.txt` | `topic=law_traffic`, `category=regulation` |
| `tai_lieu_phap_ly.txt` | `topic=law_education`, `category=legal_document` |

