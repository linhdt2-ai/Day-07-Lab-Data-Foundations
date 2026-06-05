# Group Benchmark Results

## Domain

Domain nhóm chọn là hệ thống tra cứu giao thông công cộng Hà Nội, mở rộng thêm một phần pháp lý giáo dục/pháp luật giao thông để kiểm tra metadata filter.

Các file dùng trong benchmark:

| # | File | Topic metadata | Vai trò |
|---|---|---|---|
| 1 | `lich_trinh_buyt.txt` | `bus_city` | Lịch trình và lộ trình các tuyến xe buýt |
| 2 | `bus_brt_hanoi.txt` | `bus_city` | Thông tin xe buýt/BRT Hà Nội |
| 3 | `metro_hanoi.txt` | `metro` | Thông tin Metro Hà Nội |
| 4 | `quy_dinh_phap_luat.txt` | `law_traffic` | Quy định pháp luật giao thông/metro |
| 5 | `danh_sach_tuyen_buyt.txt` | `bus_city` | Danh sách tuyến xe buýt |
| 6 | `tai_lieu_phap_ly.txt` | `law_education` | Tài liệu pháp lý giáo dục, học bổng |

## Strategy Của Tôi

Strategy: `RecursiveChunker(chunk_size=300)`

Metadata schema:

| Field | Type | Example | Lý do hữu ích |
|---|---|---|---|
| `source` | string | `metro_hanoi.txt` | Biết kết quả lấy từ file nào |
| `topic` | string | `metro` | Dùng để filter theo domain |
| `chunk_index` | int | `9` | Biết vị trí chunk trong file gốc |
| `strategy` | string | `recursive_300` | Ghi lại strategy dùng khi benchmark |

Tôi chọn `RecursiveChunker` vì dữ liệu có cấu trúc theo tuyến, mục, giá vé và quy định. Strategy này ưu tiên tách theo đoạn, dòng, câu rồi mới tách theo từ, nên có khả năng giữ các thông tin cùng một tuyến trong cùng một chunk tốt hơn `FixedSizeChunker`.

## Benchmark Queries

| Query ID | Query | Gold Answer | File chứa | Filter |
|---|---|---|---|---|
| Q1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ? | Giá 8.000đ, giờ hoạt động 05:00-21:35, tuyến Cầu Giấy - Nội Bài qua cầu Thăng Long. | `lich_trinh_buyt.txt`, `bus_brt_hanoi.txt` | Không |
| Q2 | Metro Cát Linh - Hà Đông có bao nhiêu ga và chạy mấy giờ? | 12 ga, hoạt động 05:30-22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút. | `metro_hanoi.txt` | `topic=metro` |
| Q3 | Quy định về việc ăn uống trên metro Hà Nội? | Nghiêm cấm ăn uống; mức phạt từ 100.000-300.000đ trong tàu và sân ga. | `quy_dinh_phap_luat.txt` | `topic=law_traffic` |
| Q4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | Tuyến 32: Giáp Bát -> Kim Mã -> Cầu Giấy -> Nhổn. | `lich_trinh_buyt.txt`, `danh_sach_tuyen_buyt.txt` | `topic=bus_city` |
| Q5 | Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu? | Mức học bổng bằng hoặc cao hơn mức trần học phí hiện hành của ngành. | `tai_lieu_phap_ly.txt` | `topic=law_education` |

## Kết Quả Chạy Benchmark



Kết quả:

```text
Loaded chunks: 776
Strategy: RecursiveChunker(chunk_size=300)
```

| # | Query | Top-1 Retrieved Chunk | Score | Relevant? | Nhận xét |
|---|---|---|---:|---|---|
| 1 | Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ? | `lich_trinh_buyt.txt`, chunk 111 | 0.406 | Partly | Top-1 có nhắc Cầu Giấy nhưng không trả đúng tuyến số 7, giá và giờ. |
| 2 | Metro Cát Linh - Hà Đông có bao nhiêu ga và chạy mấy giờ? | `metro_hanoi.txt`, chunk 15 | 0.341 | Partly | Filter giúp giới hạn đúng file metro, nhưng top-1 là giá vé Nhổn - Cầu Giấy, chưa đúng tuyến 2A. |
| 3 | Quy định về việc ăn uống trên metro Hà Nội? | `quy_dinh_phap_luat.txt`, chunk 0 | 0.195 | Partly | Filter đúng domain pháp luật, nhưng top-1 là tiêu đề chung. Đáp án thật nằm trong file ở phần quy định đi metro. |
| 4 | Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào? | `lich_trinh_buyt.txt`, chunk 263 | 0.434 | No | Top-1 trả tuyến số 30, chưa đúng gold answer. Top-3 có một chunk về Nhổn nhưng là tuyến 34, vẫn chưa đúng tuyến 32. |
| 5 | Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu? | `tai_lieu_phap_ly.txt`, chunk 98 | 0.310 | Partly | Filter đúng file pháp lý giáo dục, nhưng top-1 chưa chứa trực tiếp mức học bổng loại Khá. |

Relevant trong top-3: khoảng 2/5 nếu tính đúng domain, nhưng 0-1/5 nếu yêu cầu chunk chứa đúng đáp án chi tiết.

## Phân Tích

Metadata filter có ích vì nó giảm kết quả lạc domain. Ví dụ Q2 chỉ tìm trong `topic=metro`, Q3 chỉ tìm trong `topic=law_traffic`, Q5 chỉ tìm trong `topic=law_education`. Nếu không filter, kết quả rất dễ lẫn giữa xe buýt, metro và pháp lý giáo dục.

Tuy nhiên, kết quả retrieval chưa tốt vì benchmark đang dùng `MockEmbedder`. Mock embedder tạo vector giả bằng hash, không hiểu nghĩa tiếng Việt, nên điểm similarity không phản ánh đúng độ liên quan ngữ nghĩa. Vì vậy nhiều câu hỏi tìm đúng file nhưng chưa tìm đúng chunk chứa câu trả lời.

`RecursiveChunker(chunk_size=300)` vẫn phù hợp với domain này vì chunk tương đối ngắn và giữ được cấu trúc theo đoạn/tuyến. Nếu dùng embedding thật như `LocalEmbedder` hoặc `OpenAIEmbedder`, strategy này có khả năng cho kết quả tốt hơn vì từng chunk giữ được ngữ cảnh đủ rõ để trả lời.

## Kết Luận

Strategy cá nhân của tôi là `RecursiveChunker(chunk_size=300)` kết hợp metadata filter theo `topic`. Strategy này phù hợp với dữ liệu có cấu trúc như tuyến xe buýt, metro, giá vé và quy định pháp luật. Kết quả benchmark cho thấy filter hữu ích, nhưng chất lượng retrieval phụ thuộc mạnh vào embedding backend; với `MockEmbedder`, hệ thống chạy đúng pipeline nhưng retrieval chưa thật sự hiểu nghĩa.
