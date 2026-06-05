# Phase 2 Benchmark Results - Optimized

## Dataset

Danh sach file da dung:
- bus_brt_hanoi.txt
- danh_sach_tuyen_buyt.txt
- lich_trinh_buyt.txt
- metro_hanoi.txt
- quy_dinh_phap_luat.txt
- tai_lieu_phap_ly.txt

File bi bo qua:
- .gitkeep
- benchmark_queries.md
- buyt_online_hanoi.txt
- chunking_experiment_report.md
- customer_support_playbook.txt
- python_intro.txt
- rag_system_design.md
- vector_store_notes.md
- vi_retrieval_notes.md

## Optimization Summary

- Domain-aware chunking theo tung tuyen buyt, tung section metro, tung section quy dinh, va tung dieu khoan phap ly.
- Metadata chi tiet hon: `route_no`, `line_name`, `section`, `article_no`, `chunk_type`, `transport_type`.
- Query routing/filter tu dong: dung `topic` benchmark khi co, ket hop soft preferences theo route, line, article, section.
- Hybrid reranking: `final_score = 0.4 * embedding_score_norm + 0.6 * lexical_score + metadata_bonus`.
- Lexical reranking su dung normalize tieng Viet don gian va overlap token/phrase, khong can dependency moi.

## Chunk Counts

- `fixed_size`: 372 chunks
- `sentence`: 132 chunks
- `recursive`: 405 chunks
- `domain_aware`: 365 chunks

## Strategy: fixed_size

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Hard filter: Khong
Soft preferences: {'preferred_terms': ['noi bai', 'cau giay', '05 00', '21 35', '8 000', '12 000'], 'route_no': '7', 'topic': None}

Top 1:
- Final score: 1.4227
- Embedding score: 0.2087
- Lexical score: 1.3350
- Metadata bonus: 0.0800
- Completeness bonus: 0.3000
- Source: danh_sach_tuyen_buyt.txt
- Metadata: {'doc_id': 'danh_sach_tuyen_buyt', 'source': 'danh_sach_tuyen_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '7', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 2}
- Preview: - Mã số: 7 | Tuyến xe buýt: Cầu Giấy – Nội Bài | Thời gian hoạt động: 5:00 - 21:35 | Giá vé tham khảo: 12.000 VNĐ - Mã số: 08A | Tuyến xe buýt: Long Biên – Đông Mỹ | Thời gian hoạt động: 5:05 - 22:30 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 9A | Tuyến xe buýt: Bờ Hồ – Bờ Hồ | Thời gian hoạt động: 5:00 - 21:00 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 10A | Tuyến xe buýt: Long Biên - Từ Sơn | Thời gian hoạt động: 5:05 -...

Top 2:
- Final score: 0.9871
- Embedding score: 0.3130
- Lexical score: 0.9075
- Metadata bonus: 0.0800
- Completeness bonus: 0.1000
- Source: bus_brt_hanoi.txt
- Metadata: {'doc_id': 'bus_brt_hanoi', 'source': 'bus_brt_hanoi.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '7', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 1}
- Preview: I BÀI === TUYẾN 07 (Nội Bài – Bến xe Mỹ Đình): - Lộ trình: Sân bay Nội Bài → QL2 → Cầu Thăng Long → Trần Duy Hưng → Bến xe Mỹ Đình - Giờ: 05:30 – 22:00 | Tần suất: 15–20 phút | Giá: 9.000 đồng - Thời gian: 45–50 phút | Đây là tuyến phổ biến nhất từ Nội Bài TUYẾN 17 (Nội Bài – Long Biên): - Lộ trình: Sân bay Nội Bài → QL5 → Cầu Đuống → Long Biên - Giờ: 05:30 – 22:00 | Tần suất: 20–30 phút | Giá: 9.000 đồng TUYẾN 86 (N...

Top 3:
- Final score: 0.8352
- Embedding score: 0.2136
- Lexical score: 0.9875
- Metadata bonus: 0.0000
- Completeness bonus: 0.0000
- Source: bus_brt_hanoi.txt
- Metadata: {'doc_id': 'bus_brt_hanoi', 'source': 'bus_brt_hanoi.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '3', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 7}
- Preview: oàn Kiếm): Cách 1 – Buýt 7: Nội Bài → Bến xe Mỹ Đình → Buýt 45/49 → Hoàn Kiếm | ~18.000đ | 70–90 phút Cách 2 – Buýt 86: Nội Bài → Bến xe Gia Lâm → Buýt 01 → Hoàn Kiếm | ~18.000đ | 80–100 phút Cách 1 – Metro 2A: Ga Cát Linh → Ga Yên Nghĩa (~23 phút, 15.000đ) TỪ NHỔN → TRUNG TÂM HÀ NỘI: Metro 3 (trên cao): Ga Nhổn → Ga Cầu Giấy (~15 phút) + chờ đoạn ngầm 2027 Q: Đi từ sân bay Nội Bài vào Hà Nội bằng gì? Q: Metro Cát Li...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Hard filter: topic=metro
Soft preferences: {'preferred_terms': ['cat linh', 'ha dong', '12 ga', '05 30', '22 30'], 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'transport_type': 'metro', 'topic': 'metro'}

Top 1:
- Final score: 1.5615
- Embedding score: -0.0280
- Lexical score: 1.6785
- Metadata bonus: 0.2800
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'fixed_size', 'chunk_index': 6}
- Preview: yến 2A (Cát Linh – Hà Đông) Ga 11 – Văn Miếu (S11): Quận Đống Đa | Gần Văn Miếu Quốc Tử Giám Ga 12 – Ga Hà Nội (S12): Quận Hoàn Kiếm | Kết nối ga đường sắt quốc gia Hà Nội GIỜ HOẠT ĐỘNG (Đoạn trên cao Nhổn – Cầu Giấy): - 05:30 – 22:00 hàng ngày - Cao điểm: theo biểu đồ thực tế - Thấp điểm & cuối tuần: 10 phút/chuyến - Tối (19:30–22:00): 15 phút/chuyến - Từ 01/02/2026: 100% soát vé điện tử sinh trắc học GIÁ VÉ METRO N...

Top 2:
- Final score: 1.4920
- Embedding score: 0.0355
- Lexical score: 1.5415
- Metadata bonus: 0.2800
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'fixed_size', 'chunk_index': 0}
- Preview: === METRO HÀ NỘI === METRO HÀ NỘI ================================================================================ === B1. TUYẾN 2A: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) === THÔNG TIN CHUNG: - Tên: Đường sắt đô thị Hà Nội tuyến 2A - Chiều dài: 13 km (toàn bộ trên cao) - Số ga: 12 ga - Khai thác chính thức: 06/11/2021 - Đơn vị vận hành: Công ty TNHH MTV Đường sắt Hà Nội (MRB) - Hotline: (024) 7307 0888 - Website: mrhan...

Top 3:
- Final score: 1.4569
- Embedding score: -0.1402
- Lexical score: 1.5415
- Metadata bonus: 0.2800
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'fixed_size', 'chunk_index': 3}
- Preview: uất cao điểm: 6 phút/chuyến - Tần suất thường: 10 phút/chuyến - Thời gian toàn tuyến: ~23 phút GIÁ VÉ METRO CÁT LINH – HÀ ĐÔNG: - 1–4 ga: 8.000 đồng - 5–8 ga: 10.000 đồng - 9–12 ga (toàn tuyến): 15.000 đồng - Vé ngày: 30.000 đồng - Vé tháng thường: 200.000 đồng - Vé tháng sinh viên: 100.000 đồng - Miễn phí: Trẻ dưới 6 tuổi, người ≥60 tuổi, người khuyết tật === B2. TUYẾN 3: NHỔN – GA HÀ NỘI (MỘT PHẦN ĐANG HOẠT ĐỘNG) =...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Danh gia: Da route dung vao metro nhung can uu tien manh hon tuyên 2A thay vi cac section cua tuyen 3.

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Hard filter: topic=law_traffic
Soft preferences: {'preferred_terms': ['an uong', '100 000', '300 000', 'san ga', 'trong tau'], 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'topic': 'law_traffic'}

Top 1:
- Final score: 1.3487
- Embedding score: -0.0263
- Lexical score: 1.3400
- Metadata bonus: 0.2000
- Completeness bonus: 0.1500
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'strategy': 'fixed_size', 'chunk_index': 1}
- Preview: METRO: - NGHIÊM CẤM ăn uống trong tàu và trên sân ga (phạt 100.000–300.000đ) - Không hút thuốc trong toàn bộ khu vực nhà ga - Không mang xe đạp, xe máy lên tàu (trừ xe đẩy em bé gấp gọn) - Không chụp ảnh tại khu vực vận hành, buồng lái - Không đứng sát cửa, không giữ cửa tàu - Vượt vạch vàng an toàn: có thể bị phạt - Mang theo vé/thẻ hợp lệ khi soát vé LUẬT GIAO THÔNG – NGHỊ ĐỊNH 100/2019/NĐ-CP (Mức phạt xe cơ giới):...

Top 2:
- Final score: 1.0794
- Embedding score: -0.2330
- Lexical score: 1.2100
- Metadata bonus: 0.2000
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'strategy': 'fixed_size', 'chunk_index': 0}
- Preview: === QUY ĐỊNH PHÁP LUẬT === QUY ĐỊNH & LUẬT PHÁP ================================================================================ QUY ĐỊNH ĐI XE BUÝT: - Không hút thuốc, không xả rác, giữ trật tự, không ăn uống mạnh - Nhường ghế cho người cao tuổi, khuyết tật, phụ nữ mang thai, trẻ em - Hành lý tay: không quá 20 kg - Không mang chất dễ cháy, nổ, chất độc, vật sắc nhọn nguy hiểm - Thanh toán tiền mặt hoặc thẻ điện tử t...

Top 3:
- Final score: 0.3521
- Embedding score: 0.1403
- Lexical score: 0.1400
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'strategy': 'fixed_size', 'chunk_index': 3}
- Preview: y): 300.000 – 400.000đ | ô tô: 3.000.000 – 5.000.000đ

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['giap bat', 'nhon', 'kim ma', 'cau giay', '32'], 'route_no': '32', 'transport_type': 'bus', 'topic': 'bus_city'}

Top 1:
- Final score: 1.3969
- Embedding score: 0.1947
- Lexical score: 1.4300
- Metadata bonus: 0.2000
- Completeness bonus: 0.1000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '32', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 45}
- Preview: <> Lê Thanh Nghị <> Tạ Quang Bửu <> Đại Cồ Việt <> Phố Huế <> Hàng Bài <> Lý Thường Kiệt <> Phan Chu Trinh <> Lý Thái Tổ <> Ngô Quyền <> Hàng Vôi <> Hàng Tre <> Hàng Muối <> Trần Nhật Duật <> Điểm trung chuyển Long Biên <> Yên Phụ <> Nghi Tàm <> Âu Cơ <> Nhật Tân <> An Dương Vương <> Phú Thượng <> Dốc Chèm <> Đông Ngạc <> Chèm (Đại học Mỏ). Thời gian hoạt động: 5:05 – 21:00. Giá vé: 7.000 VNĐ. Tần suất: 10 – 25 phút/...

Top 2:
- Final score: 0.7820
- Embedding score: 0.2098
- Lexical score: 0.7000
- Metadata bonus: 0.1200
- Completeness bonus: 0.0000
- Source: danh_sach_tuyen_buyt.txt
- Metadata: {'doc_id': 'danh_sach_tuyen_buyt', 'source': 'danh_sach_tuyen_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '26', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 7}
- Preview: : 5:09 - 21:00 | Giá vé tham khảo: 12.000 VNĐ - Mã số: 26 | Tuyến xe buýt: Mai Động – SVĐ Quốc gia | Thời gian hoạt động: 5:00 - 22:30 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 27 | Tuyến xe buýt: BX.Nam Thăng Long – BX.Yên Nghĩa | Thời gian hoạt động: 5:00 - 21:35 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 28 | Tuyến xe buýt: BX Giáp Bát – ĐH Mỏ | Thời gian hoạt động: 5:01 - 21:02 | Giá vé tham khảo: 10.000 VNĐ - Mã số:...

Top 3:
- Final score: 0.7625
- Embedding score: 0.2325
- Lexical score: 0.6600
- Metadata bonus: 0.1200
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 151}
- Preview: Xuyên). Tuyến buýt số 92 : Nhổn ⇄ Tây Đằng Nhổn - đường Cầu Diễn - đường Cầu Diễn - Phố Nhổn - Quốc lộ 32 - thị trấn Tây Đằng (Ba Vì) - Đường 411 - Tây Đằng. Tuyến buýt số 93 : Nam Thăng Long ⇄ Bắc Sơn Nam Thăng Long (điểm đỗ xe buýt trên đường đỗ Nhuận, cạnh cổng công viên Hòa Bình) - Đỗ Nhuận - quay đầu tại điểm mở - Đỗ Nhuận - Phạm Văn Đồng - cầu Thăng Long - Võ Văn Kiệt - Quốc lộ 2 - Quốc lộ 3 - Tỉnh lộ 35 - đườn...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Hard filter: topic=law_education
Soft preferences: {'preferred_terms': ['hoc bong', 'loai kha', 'muc tran hoc phi', 'dieu 7'], 'article_no': '7', 'topic': 'law_education'}

Top 1:
- Final score: 0.6497
- Embedding score: 0.2485
- Lexical score: 0.6000
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'fixed_size', 'chunk_index': 57}
- Preview: ng; b) Đối với học sinh trường dự bị đại học, trường phổ thông dân tộc nội trú: Trong thời hạn 10 ngày làm việc kể từ ngày nhập học, học sinh nộp 01 bộ hồ sơ theo quy định cho nhà trường nơi học sinh đang theo học để xét, cấp học bổng chính sách. Mỗi học sinh chỉ nộp một bộ hồ sơ một lần để đề nghị cấp học bổng trong cả thời gian học tại cơ sở giáo dục. Trong thời hạn 10 ngày làm việc kể từ ngày kết thúc nhận hồ sơ ,...

Top 2:
- Final score: 0.6491
- Embedding score: 0.2454
- Lexical score: 0.6000
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'fixed_size', 'chunk_index': 47}
- Preview: h, người khuyết tật được hưởng mức học bổng bằng 80% mức lương cơ sở/tháng; b) Học viên thuộc diện hộ nghèo học trong các cơ sở giáo dục nghề nghiệp dành cho thương binh, người khuyết tật: mức học bổng bằng 100% mức lương cơ sở/tháng. 2. Nguyên tắc hưởng: a) Học bổng chính sách chỉ được hưởng một lần trong cả quá trình đi học của sinh viên, học viên quy định tại khoản 1 Điều này. Học bổng chính sách được chi trả hai...

Top 3:
- Final score: 0.6312
- Embedding score: 0.1560
- Lexical score: 0.6000
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'fixed_size', 'chunk_index': 59}
- Preview: sở giáo dục đang theo học theo định k ỳ xét, cấp học bổng chính sách theo quy định; c) Đối với học viên cơ sở giáo dục nghề nghiệp dành cho thương binh, người khuyết tật: Trong thời hạn 10 ngày làm việc kể từ ngày nhập học, cơ sở giáo dục nghề nghiệp thông báo cho học viên về chế độ học bổng chính sách, thời gian nộp hồ sơ và hướng dẫn học viên nộp 01 bộ hồ sơ theo quy định. Mỗi học viên chỉ phải nộp một bộ hồ sơ một...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Danh gia: Tai lieu phap ly dai va OCR khien retrieval van co xu huong roi vao dieu/khoan khac trong cung van ban.

## Strategy: sentence

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Hard filter: Khong
Soft preferences: {'preferred_terms': ['noi bai', 'cau giay', '05 00', '21 35', '8 000', '12 000'], 'route_no': '7', 'topic': None}

Top 1:
- Final score: 0.9480
- Embedding score: 0.1926
- Lexical score: 1.1825
- Metadata bonus: 0.0000
- Completeness bonus: 0.0000
- Source: danh_sach_tuyen_buyt.txt
- Metadata: {'doc_id': 'danh_sach_tuyen_buyt', 'source': 'danh_sach_tuyen_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '1', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === DANH SÁCH TUYẾN XE BUÝT HÀ NỘI (TỪ EXCEL) === - Mã số: 1 | Tuyến xe buýt: BX Gia Lâm - BX Yên Nghĩa | Thời gian hoạt động: 5:00 – 21:00 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 2 | Tuyến xe buýt: Bác Cổ – BX Yên Nghĩa | Thời gian hoạt động: 5:00 – 22:30 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 03A | Tuyến xe buýt: BX Giáp Bát – BX Gia Lâm | Thời gian hoạt động: 5:00 – 21:00 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 0...

Top 2:
- Final score: 0.6668
- Embedding score: 0.2715
- Lexical score: 0.6875
- Metadata bonus: 0.0000
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 59}
- Preview: Tuyến buýt số 93 : Nam Thăng Long ⇄ Bắc Sơn Nam Thăng Long (điểm đỗ xe buýt trên đường đỗ Nhuận, cạnh cổng công viên Hòa Bình) - Đỗ Nhuận - quay đầu tại điểm mở - Đỗ Nhuận - Phạm Văn Đồng - cầu Thăng Long - Võ Văn Kiệt - Quốc lộ 2 - Quốc lộ 3 - Tỉnh lộ 35 - đường nối xã Bắc Sơn, Hồng Kỳ - Bắc Sơn (Bãi đỗ xe buýt thôn Đa Hội, xã Bắc Sơn, huyện Sóc Sơn) Tuyến buýt số 94 : Bến xe Giáp Bát ⇄ Kim Bài Bến xe Giáp Bát - Giả...

Top 3:
- Final score: 0.6172
- Embedding score: 0.2259
- Lexical score: 0.6200
- Metadata bonus: 0.0000
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '51', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 48}
- Preview: Thời gian hoạt động: 5:00 – 21:09. Giá vé: 7.000 VNĐ. Tần suất: 17 – 23 phút/chuyến. Tuyến xe buýt số 51: Trần Khánh Dư <> Công viên Cầu Giấy Lộ trình: Bãi đỗ xe Trần Khánh Dư <> Nguyễn Khoái <> Lạc Trung <> Thanh Nhàn <> Võ Thị Sáu <> Trần Khát Chân <> Đại Cồ Việt <> Xã Đàn <> Phạm Ngọc Thạch <> Chùa Bộc <> Tây Sơn <> Thái Thịnh <> Láng Hạ <> Quay đầu tại gầm cầu vượt Láng Hạ <> Láng Hạ <> Lê Văn Lương <> Hoàng Đạo...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Danh gia: Van con nhieu tuyen san bay va tuyen qua Cau Giay/Noi Bai gan nhau, nen can lexical route match manh hon nua.

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Hard filter: topic=metro
Soft preferences: {'preferred_terms': ['cat linh', 'ha dong', '12 ga', '05 30', '22 30'], 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'transport_type': 'metro', 'topic': 'metro'}

Top 1:
- Final score: 1.7313
- Embedding score: -0.0397
- Lexical score: 1.7654
- Metadata bonus: 0.2800
- Completeness bonus: 0.2000
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === METRO HÀ NỘI === METRO HÀ NỘI ================================================================================ === B1. TUYẾN 2A: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) === THÔNG TIN CHUNG: - Tên: Đường sắt đô thị Hà Nội tuyến 2A - Chiều dài: 13 km (toàn bộ trên cao) - Số ga: 12 ga - Khai thác chính thức: 06/11/2021 - Đơn vị vận hành: Công ty TNHH MTV Đường sắt Hà Nội (MRB) - Hotline: (024) 7307 0888 - Website: mrhan...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Hard filter: topic=law_traffic
Soft preferences: {'preferred_terms': ['an uong', '100 000', '300 000', 'san ga', 'trong tau'], 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'topic': 'law_traffic'}

Top 1:
- Final score: 1.4388
- Embedding score: 0.1239
- Lexical score: 1.4400
- Metadata bonus: 0.2000
- Completeness bonus: 0.1500
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === QUY ĐỊNH PHÁP LUẬT === QUY ĐỊNH & LUẬT PHÁP ================================================================================ QUY ĐỊNH ĐI XE BUÝT: - Không hút thuốc, không xả rác, giữ trật tự, không ăn uống mạnh - Nhường ghế cho người cao tuổi, khuyết tật, phụ nữ mang thai, trẻ em - Hành lý tay: không quá 20 kg - Không mang chất dễ cháy, nổ, chất độc, vật sắc nhọn nguy hiểm - Thanh toán tiền mặt hoặc thẻ điện tử t...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['giap bat', 'nhon', 'kim ma', 'cau giay', '32'], 'route_no': '32', 'transport_type': 'bus', 'topic': 'bus_city'}

Top 1:
- Final score: 1.5006
- Embedding score: 0.1032
- Lexical score: 1.5000
- Metadata bonus: 0.2000
- Completeness bonus: 0.1800
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '32', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 31}
- Preview: Tuyến xe buýt số 32: Bến xe Giáp Bát <> Nhổn Lộ trình: Bến xe Giáp Bát <> Giải Phóng <> Lê Duẩn <> Trần Nhân Tông <> Trần Bình Trọng <> Trần Hưng Đạo <> Quán Sứ <> Hai Bà Trưng <> Thợ Nhuộm <> Tràng Thị <> Điện Biên Phủ <> Trần Phú <> Kim Mã <> Càu Giấy <> Điểm trung chuyển Cầu Giấy <> Cầu Giấy <> Xuân Thuỷ <> Hồ Tùng Mậu <> Diễn <> Đường 3/2 <> Phố Nhổn <> Nhổn. Thời gian hoạt động: 5:00 – 22:30. Giá vé: 7.000 VNĐ....

Top 2:
- Final score: 1.2268
- Embedding score: 0.1838
- Lexical score: 1.4500
- Metadata bonus: 0.1200
- Completeness bonus: 0.0000
- Source: bus_brt_hanoi.txt
- Metadata: {'doc_id': 'bus_brt_hanoi', 'source': 'bus_brt_hanoi.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '7', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === XE BUÝT HÀ NỘI === XE BUÝT HÀ NỘI (CHI TIẾT CÁC TUYẾN QUAN TRỌNG) ================================================================================ TỔNG QUAN: - Đơn vị quản lý chính: Tổng công ty Vận tải Hà Nội (Transerco) - Website: transerco.com.vn | timbus.vn - App: Tìm Buýt (iOS & Android) | Hotline: 1900 1296 - Giá vé từ 01/11/2024: 8.000đ (<15km) đến 20.000đ (>40km) - Thẻ vé điện tử liên thông đang thí điểm...

Top 3:
- Final score: 1.0533
- Embedding score: 0.1267
- Lexical score: 1.1800
- Metadata bonus: 0.1200
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 19}
- Preview: Tuyến xe buýt 20C: Nhổn <> Võng Xuyên Lộ trình: Nhổn (Điểm trung chuyển xe buýt Nhổn) <> Nhổn <> Quay đầu tại Cumj Công nghiệp vừa và nhỏ Từ Liêm <> Quốc lộ 32 <> Ngã tư Nhổn <> Tây Tựu <> Thượng Cát <> Đê Liên Trì <> Đê Hữu Hồng <> Tiên Tân <> Trung Châu <> Hát Môn <> Ngã tư huyện (Cụm 11, Võng Xuyên). Thời gian hoạt động: 5:23 – 18:08. Giá vé: 9.000 VNĐ. Tần suất: 30 phút/chuyến. Tuyến xe buýt 21A: Bến xe Giáp Bát...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Hard filter: topic=law_education
Soft preferences: {'preferred_terms': ['hoc bong', 'loai kha', 'muc tran hoc phi', 'dieu 7'], 'article_no': '7', 'topic': 'law_education'}

Top 1:
- Final score: 0.7931
- Embedding score: 0.1653
- Lexical score: 0.8667
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'article_no': '8', 'article_title': 'Học bổng khuyến khích học tập', 'strategy': 'sentence', 'chunk_index': 11}
- Preview: Việc xét, cấp học bổng đối với đối tượng quy định tại điểm c khoản 1 Điều này: a) Hiệu trưởng căn cứ vào nguồn học bổng khuyến khích học tập xác định số lượng suất học bổng cho từng khóa học, ngành học. Trong trường hợp số lượng người học thuộc diện được xét, cấp học bổng nhiều hơn số suất học bổng thì việc xét, cấp học bổng do hiệu trưởng quyết định; b) Hiệu trưởng căn cứ vào kết quả học tập và rèn luyện của người h...

Top 2:
- Final score: 0.7525
- Embedding score: 0.1625
- Lexical score: 0.8000
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'sentence', 'chunk_index': 17}
- Preview: Trong thời hạn 10 ngày làm việc kể từ ngày nhận đủ hồ sơ hợp lệ , Ủy ban nhân dân cấp xã tổ chức thẩm định, phê duyệt danh sách đối tượng được hưởng chính sách và xây dựng dự toán kinh phí thực hiện ( Mẫu số 05 tại Phụ lục kèm theo Nghị định này ) gửi cơ quan tài chính có thẩm quyền, trình cấp có thẩm quyền phê duyệt (Mẫu số 06 tại Phụ lục kèm theo Nghị định này) . Trường hợp hồ sơ không bảo đảm đúng quy định, Ủy ban...

Top 3:
- Final score: 0.7094
- Embedding score: 0.1468
- Lexical score: 0.7333
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'article_title': 'Học bổng khuyến khích học tập', 'strategy': 'sentence', 'chunk_index': 31}
- Preview: Các hồ sơ phong tặng Tiến sĩ danh dự, Giáo sư danh dự đã nộp cho Hội đồng trường của cơ sở giáo dục đại học công lập xem xét trước ngày 01 tháng 01 năm 2026 được chuyển giao cho Giám đốc hoặc hiệu trưởng cơ sở giáo dục đại học công lập xem xét, quyết định theo thẩm quyền quy định tại Nghị định này. 2. Các hồ sơ đề nghị chuyển đổi nhà trẻ, trường mẫu giáo, trường mầm non, cơ sở giáo dục phổ thông, cơ sở giáo dục nghề...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Danh gia: Tai lieu phap ly dai va OCR khien retrieval van co xu huong roi vao dieu/khoan khac trong cung van ban.

## Strategy: recursive

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Hard filter: Khong
Soft preferences: {'preferred_terms': ['noi bai', 'cau giay', '05 00', '21 35', '8 000', '12 000'], 'route_no': '7', 'topic': None}

Top 1:
- Final score: 0.7613
- Embedding score: 0.2265
- Lexical score: 0.8600
- Metadata bonus: 0.0000
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '8', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 19}
- Preview: Lộ trình: Bãi đỗ xe Cầu Giấy <> Điểm trung chuyển Cầu Giấy <> Nguyễn Văn Huyên <> Hoàng Quốc Việt <> Phạm Văn Đồng <> Cầu Thăng Long <> Võ Văn Kiệt <> Đường dưới cầu vượt Kim Chung <> Võ Văn Kiệt <> Sân bay Nội Bài. Thời gian hoạt động: 5:00 – 21:35. Giá vé: 8.000 VNĐ. Tuyến xe buýt số 8: Long Biên <> Đông Mỹ

Top 2:
- Final score: 0.5969
- Embedding score: 0.3047
- Lexical score: 0.5600
- Metadata bonus: 0.0000
- Completeness bonus: 0.0000
- Source: danh_sach_tuyen_buyt.txt
- Metadata: {'doc_id': 'danh_sach_tuyen_buyt', 'source': 'danh_sach_tuyen_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 35}
- Preview: - Mã số: Phủ Tây Hồ | Tuyến xe buýt: 31, 55, 57, 58, 90 | Thời gian hoạt động: Đền thờ thánh Mẫu, nổi tiếng với kiến trúc đẹp và không gian linh thiêng. - Mã số: Cầu Long Biên | Tuyến xe buýt: 14, 21, 35, 50, 55 | Thời gian hoạt động: Cây cầu lịch sử bắc qua sông Hồng, từng chứng kiến nhiều biến cố lịch sử của thủ đô. - Mã số: Chợ Đồng Xuân | Tuyến xe buýt: 01, 14, 36, 52, 55 | Thời gian hoạt động: Chợ truyền thống l...

Top 3:
- Final score: 0.5524
- Embedding score: 0.2770
- Lexical score: 0.4950
- Metadata bonus: 0.0000
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 21}
- Preview: Lộ trình: Bãi đỗ xe Bờ Hồ <> Đình Tiên Hoàng <> Lê Thái Tổ <> Bà Triệu <> Hồ Xuân Hương <> Nguyễn Bỉnh Khiêm <> Trần Nhân Tông <> Lê Duẩn <> Khâm Thiên <> Đường mới (Vành đai 1) <> Quay đầu tại điểm mở dải phân cách <> Đường mới (Vành đai 1) <> Nguyễn Lương Bằng <> Tây Sơn <> Ngã tư Sở <> Láng <> Láng Hạ <> Huỳnh Thúc Kháng <> Nguyễn Chí Thanh <> Quay đầu tại đối diện 56 Nguyễn Chí Thanh <> Chùa Láng <> Láng <> Điểm...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Danh gia: Van con nhieu tuyen san bay va tuyen qua Cau Giay/Noi Bai gan nhau, nen can lexical route match manh hon nua.

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Hard filter: topic=metro
Soft preferences: {'preferred_terms': ['cat linh', 'ha dong', '12 ga', '05 30', '22 30'], 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'transport_type': 'metro', 'topic': 'metro'}

Top 1:
- Final score: 1.6901
- Embedding score: -0.0149
- Lexical score: 1.6885
- Metadata bonus: 0.2800
- Completeness bonus: 0.2000
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'recursive', 'chunk_index': 3}
- Preview: GIỜ HOẠT ĐỘNG: - Chuyến đầu: 05:30 - Chuyến cuối: 22:30 - Tần suất cao điểm: 6 phút/chuyến - Tần suất thường: 10 phút/chuyến - Thời gian toàn tuyến: ~23 phút GIÁ VÉ METRO CÁT LINH – HÀ ĐÔNG: - 1–4 ga: 8.000 đồng - 5–8 ga: 10.000 đồng - 9–12 ga (toàn tuyến): 15.000 đồng - Vé ngày: 30.000 đồng - Vé tháng thường: 200.000 đồng - Vé tháng sinh viên: 100.000 đồng - Miễn phí: Trẻ dưới 6 tuổi, người ≥60 tuổi, người khuyết tậ...

Top 2:
- Final score: 1.4889
- Embedding score: 0.0200
- Lexical score: 1.5415
- Metadata bonus: 0.2800
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'recursive', 'chunk_index': 0}
- Preview: === METRO HÀ NỘI === METRO HÀ NỘI ================================================================================ === B1. TUYẾN 2A: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) === THÔNG TIN CHUNG: - Tên: Đường sắt đô thị Hà Nội tuyến 2A - Chiều dài: 13 km (toàn bộ trên cao) - Số ga: 12 ga - Khai thác chính thức: 06/11/2021 - Đơn vị vận hành: Công ty TNHH MTV Đường sắt Hà Nội (MRB) - Hotline: (024) 7307 0888 - Website: mrhan...

Top 3:
- Final score: 1.4733
- Embedding score: -0.0580
- Lexical score: 1.5415
- Metadata bonus: 0.2800
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'recursive', 'chunk_index': 1}
- Preview: LỘ TRÌNH 12 GA (Cát Linh → Hà Đông): Ga 01 – Cát Linh: Quận Đống Đa | Điểm đầu, gần Đại học Kiến trúc, kết nối nhiều tuyến buýt Ga 02 – La Thành: Quận Đống Đa | Gần Văn Miếu Quốc Tử Giám (đi bộ ~800m) Ga 03 – Thái Hà: Quận Đống Đa | Khu thương mại Thái Hà, nhiều quán ăn Ga 04 – Láng: Quận Đống Đa | Gần ĐH Quốc gia Hà Nội, bệnh viện Nhi Ga 05 – Thượng Đình: Quận Thanh Xuân | Khu công nghiệp cao su Thượng Đình Ga 06 –...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Hard filter: topic=law_traffic
Soft preferences: {'preferred_terms': ['an uong', '100 000', '300 000', 'san ga', 'trong tau'], 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'topic': 'law_traffic'}

Top 1:
- Final score: 1.4362
- Embedding score: 0.1111
- Lexical score: 1.4400
- Metadata bonus: 0.2000
- Completeness bonus: 0.1500
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'strategy': 'recursive', 'chunk_index': 1}
- Preview: QUY ĐỊNH ĐI METRO: - NGHIÊM CẤM ăn uống trong tàu và trên sân ga (phạt 100.000–300.000đ) - Không hút thuốc trong toàn bộ khu vực nhà ga - Không mang xe đạp, xe máy lên tàu (trừ xe đẩy em bé gấp gọn) - Không chụp ảnh tại khu vực vận hành, buồng lái - Không đứng sát cửa, không giữ cửa tàu - Vượt vạch vàng an toàn: có thể bị phạt - Mang theo vé/thẻ hợp lệ khi soát vé

Top 2:
- Final score: 0.5962
- Embedding score: -0.0188
- Lexical score: 0.6000
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'quy_dinh_di_xe_buyt', 'transport_type': 'bus', 'strategy': 'recursive', 'chunk_index': 0}
- Preview: === QUY ĐỊNH PHÁP LUẬT === QUY ĐỊNH & LUẬT PHÁP ================================================================================ QUY ĐỊNH ĐI XE BUÝT: - Không hút thuốc, không xả rác, giữ trật tự, không ăn uống mạnh - Nhường ghế cho người cao tuổi, khuyết tật, phụ nữ mang thai, trẻ em - Hành lý tay: không quá 20 kg - Không mang chất dễ cháy, nổ, chất độc, vật sắc nhọn nguy hiểm - Thanh toán tiền mặt hoặc thẻ điện tử t...

Top 3:
- Final score: 0.3421
- Embedding score: -0.0296
- Lexical score: 0.1800
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'luat_giao_thong', 'strategy': 'recursive', 'chunk_index': 2}
- Preview: LUẬT GIAO THÔNG – NGHỊ ĐỊNH 100/2019/NĐ-CP (Mức phạt xe cơ giới): - Không có GPLX: 800.000 – 1.200.000đ (xe máy) | 4.000.000 – 6.000.000đ (ô tô) - Vượt đèn đỏ: 4.000.000 – 6.000.000đ (xe máy) | 6.000.000 – 8.000.000đ (ô tô) - Nồng độ cồn 0,25–0,4 mg/l khí thở: 6.000.000 – 8.000.000đ + tước GPLX 10–12 tháng - Nồng độ cồn >0,4 mg/l (xe máy): 30.000.000 – 40.000.000đ + tước GPLX 22–24 tháng - Không đội mũ bảo hiểm: 200....

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['giap bat', 'nhon', 'kim ma', 'cau giay', '32'], 'route_no': '32', 'transport_type': 'bus', 'topic': 'bus_city'}

Top 1:
- Final score: 0.8366
- Embedding score: 0.1830
- Lexical score: 0.8000
- Metadata bonus: 0.1200
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 93}
- Preview: Bến xe Nước Ngầm - Ngọc Hồi - Giải Phóng - Bến xe Giáp Bát (Quảng trường Bến xe Giáp Bát) - Giải Phóng - Đại La - Minh Khai - Cầu Vĩnh Tuy - Đàm Quang Trung - Chu Huy Mân - Hội Xá - Vũ Xuân Thiều - Đường Phúc Lợi - Ngõ 193 Phúc lợi - Ngách 195/9 Phúc Lợi - Ngõ 195 Phúc Lợi - Phúc Lợi (đối diện trường THPT Phúc Lợi). Tuyến buýt số 04 : Long Biên ⇄ Bến xe Nước Ngầm

Top 2:
- Final score: 0.8162
- Embedding score: 0.2012
- Lexical score: 0.7600
- Metadata bonus: 0.1200
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 215}
- Preview: Tuyến buýt số CNG05 : Cầu Giấy ⇄ Tam Hiệp Cầu Giấy (Bãi đỗ xe Cầu Giấy) - Cầu Giấy (đường trên) - Điểm trung chuyển Cầu Giấy (hè trước tường rào vườn thú Hà Nội) - Cầu Giấy - Đường Láng - Ngã Tư Sở - Nguyễn Trãi - Nguyễn Xiển - Nghiêm Xuân Yêm - Thanh Liệt - Cầu Bươu - Phan Trọng Tuệ - ngõ 190 Phan Trọng Tuệ - đường vào UBND xã Tam Hiệp - Tam Hiệp (trước sân bóng Đình Cung, xã Tam Hiệp, Thanh Trì). Tuyến buýt số CNG0...

Top 3:
- Final score: 0.7819
- Embedding score: 0.2695
- Lexical score: 0.6800
- Metadata bonus: 0.1200
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '48', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 78}
- Preview: Lộ trình: Điểm trung chuyển Long Biên <> Yên Phụ <> Trần Nhật Duật <> Cầu Chương Dương <> Đê Long Biên <> Bồ Đề <> Tư Đình <> Cự Khối <> Đông Dư <> Qua ngã ba đi Bát Tràng <> Đường liên xã Kim Lan <> Bãi đỗ xe Kim Lan. Thời gian hoạt động: 5:14 – 19:42. Giá vé: 7.000 VNĐ. Tần suất: 28 – 33 phút/chuyến. Tuyến xe buýt số 48: Trần Khánh Dư <> Vạn Phúc

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Danh gia: Van de chinh la nhieu tuyen buyt cung chia se diem Giap Bat/Cau Giay/Nhon, nen Top-1 van de lech sang tuyen khac.

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Hard filter: topic=law_education
Soft preferences: {'preferred_terms': ['hoc bong', 'loai kha', 'muc tran hoc phi', 'dieu 7'], 'article_no': '7', 'topic': 'law_education'}

Top 1:
- Final score: 1.0907
- Embedding score: 0.2237
- Lexical score: 1.2100
- Metadata bonus: 0.1200
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'article_no': '7', 'article_title': 'Học bổng khuyến khích học tập', 'strategy': 'recursive', 'chunk_index': 31}
- Preview: Điều 7. Học bổng khuyến khích học tập 1. Đối tượng xét, cấp học bổng khuyến khích học tập: a) Học sinh trường trung học phổ thông chuyên (sau đây gọi chung là trường chuyên), học sinh trung học phổ thông chuyên trong cơ sở giáo dục đại học có kết quả rèn luyện và kết quả học tập đạt mức cao nhất trong các mức đánh giá kết quả rèn luyện, kết quả học tập của học sinh trung học phổ thông thuộc kỳ xét, cấp học bổng và có...

Top 2:
- Final score: 0.7018
- Embedding score: 0.1492
- Lexical score: 0.7200
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'recursive', 'chunk_index': 36}
- Preview: Khá trở lên. Đối với các trường tư thục mức học bổng tối thiểu do hiệu trưởng quy định. Đối với những ngành nghề đào tạo không thu học phí thì áp dụng theo đơn giá được Nhà nước đặt hàng, giao nhiệm vụ cho nhóm ngành đào tạo của trường; b) Học bổng loại Giỏi: Mức học bổng cao hơn loại khá do hiệu trưởng quy định đối với người học có điểm trung bình chung học tập đạt loại Giỏi trở lên và điểm rèn luyện đạt loại tốt tr...

Top 3:
- Final score: 0.6767
- Embedding score: 0.1835
- Lexical score: 0.6667
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'recursive', 'chunk_index': 45}
- Preview: dành cho thương binh, người khuyết tật: mức học bổng bằng 100% mức lương cơ sở/tháng. 2. Nguyên tắc hưởng: a) Học bổng chính sách chỉ được hưởng một lần trong cả quá trình đi học của sinh viên, học viên quy định tại khoản 1 Điều này. Học bổng chính sách được chi trả hai lần trong năm học, mỗi lần 06 tháng, lần thứ nhất cấp vào tháng 10, lần thứ hai cấp vào tháng 3. Trường hợp học sinh, sinh viên, học viên (sau đây gọ...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Danh gia: Tai lieu phap ly dai va OCR khien retrieval van co xu huong roi vao dieu/khoan khac trong cung van ban.

## Strategy: domain_aware

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Hard filter: Khong
Soft preferences: {'preferred_terms': ['noi bai', 'cau giay', '05 00', '21 35', '8 000', '12 000'], 'route_no': '7', 'topic': None}

Top 1:
- Final score: 1.0253
- Embedding score: 0.2442
- Lexical score: 1.0275
- Metadata bonus: 0.0800
- Completeness bonus: 0.0800
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 70, 'chunk_type': 'bus_route', 'route_no': '7'}
- Preview: Tuyến buýt số 07 : Cầu Giấy ⇄ Nội Bài Bãi đỗ xe Cầu Giấy - Cầu Giấy - Điểm trung chuyển Cầu Giấy (hè trước tường rào Vườn thú Hà Nội) - Cầu Giấy - Nguyễn Văn Huyên - Hoàng Quốc Việt - Phạm Văn Đồng - Cầu Thăng Long - Võ Văn Kiệt - Đường dưới cầu vượt Kim Chung - Võ Văn Kiệt - Quay đầu tại điểm mở (đối diện công ty dịch vụ hàng hóa hàng không - ACS) - Võ Văn Kiệt - Sân bay Nội Bài (Sân đỗ P2, nhà ga T1)

Top 2:
- Final score: 0.6102
- Embedding score: 0.1912
- Lexical score: 0.6200
- Metadata bonus: 0.0000
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 42, 'chunk_type': 'bus_route', 'route_no': '38'}
- Preview: Tuyến xe buýt số 38: Bến xe Nam Thăng Long <> Mai Động Lộ trình: Bãi đỗ xe buýt Nam Thăng Long <> Phạm Văn Đồng <> Hoàng Quốc Việt <> Nguyễn Văn Huyên <> Nguyễn Khánh Toàn <> Bưởi <> Cầu Giấy <> Điểm trung chuyển Cầu Giấy <> Kim Mã <> Nguyễn Thái Học <> Lê Duẩn <> Trần Hưng Đạo <> Bà Triệu <> Lê Đại Hành <> Bạch mai <> Minh Khai <> Tam Trinh <> Cầu Voi <> Nguyễn Tam Trinh <> Mai Động. Thời gian hoạt động: 5:05 – 21:0...

Top 3:
- Final score: 0.5385
- Embedding score: 0.1924
- Lexical score: 0.5000
- Metadata bonus: 0.0000
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 12, 'chunk_type': 'bus_route', 'route_no': '10A'}
- Preview: Tuyến xe buýt số 10A: Long Biên <> Từ Sơn Lộ trình: Long Biên (Đối diện Đội Cảnh sát Giao thông số 1 Hà nôi – 3 Trần Nhật Duật) <> Trần Nhật Duật <> Yên Phụ <> Quay đầu tại 92 Yên Phụ <> Điểm trung chuyển Long Biên <> Trần Nhật Duật <> Cầu Chương Dương <> Nguyễn Văn Cừ <> Ngô Gia Tự <> Cầu Đuống <> Hà Huy Tập <> Quốc lộ 1A <> Dốc Lã <> Đình Bảng <> Trần Phú (Từ Sơn) <> Minh Khai (Từ Sơn) <> Từ Sơn (Cổng Bệnh viện Đa...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Danh gia: Van con nhieu tuyen san bay va tuyen qua Cau Giay/Noi Bai gan nhau, nen can lexical route match manh hon nua.

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Hard filter: topic=metro
Soft preferences: {'preferred_terms': ['cat linh', 'ha dong', '12 ga', '05 30', '22 30'], 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'transport_type': 'metro', 'topic': 'metro'}

Top 1:
- Final score: 1.7049
- Embedding score: -0.1715
- Lexical score: 1.7654
- Metadata bonus: 0.2800
- Completeness bonus: 0.2000
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'domain_aware', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_section', 'chunk_index': 0, 'section': 'full_route'}
- Preview: === B1. TUYẾN 2A: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) === THÔNG TIN CHUNG: - Tên: Đường sắt đô thị Hà Nội tuyến 2A - Chiều dài: 13 km (toàn bộ trên cao) - Số ga: 12 ga - Khai thác chính thức: 06/11/2021 - Đơn vị vận hành: Công ty TNHH MTV Đường sắt Hà Nội (MRB) - Hotline: (024) 7307 0888 - Website: mrhanoi.gov.vn LỘ TRÌNH 12 GA (Cát Linh → Hà Đông): Ga 01 – Cát Linh: Quận Đống Đa | Điểm đầu, gần Đại học Kiến trúc, kế...

Top 2:
- Final score: 1.5326
- Embedding score: 0.0891
- Lexical score: 1.5246
- Metadata bonus: 0.2800
- Completeness bonus: 0.1200
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'domain_aware', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_section', 'chunk_index': 3, 'section': 'gio_hoat_dong'}
- Preview: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) GIỜ HOẠT ĐỘNG : - Chuyến đầu: 05:30 - Chuyến cuối: 22:30 - Tần suất cao điểm: 6 phút/chuyến - Tần suất thường: 10 phút/chuyến - Thời gian toàn tuyến: ~23 phút

Top 3:
- Final score: 1.4758
- Embedding score: -0.0459
- Lexical score: 1.5415
- Metadata bonus: 0.2800
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'domain_aware', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_section', 'chunk_index': 2, 'section': 'lo_trinh_va_ga'}
- Preview: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) LỘ TRÌNH 12 GA (Cát Linh → Hà Đông): Ga 01 – Cát Linh: Quận Đống Đa | Điểm đầu, gần Đại học Kiến trúc, kết nối nhiều tuyến buýt Ga 02 – La Thành: Quận Đống Đa | Gần Văn Miếu Quốc Tử Giám (đi bộ ~800m) Ga 03 – Thái Hà: Quận Đống Đa | Khu thương mại Thái Hà, nhiều quán ăn Ga 04 – Láng: Quận Đống Đa | Gần ĐH Quốc gia Hà Nội, bệnh viện Nhi Ga 05 – Thượng Đình: Quận Thanh Xuân | Khu côn...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Hard filter: topic=law_traffic
Soft preferences: {'preferred_terms': ['an uong', '100 000', '300 000', 'san ga', 'trong tau'], 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'topic': 'law_traffic'}

Top 1:
- Final score: 1.4362
- Embedding score: 0.1111
- Lexical score: 1.4400
- Metadata bonus: 0.2000
- Completeness bonus: 0.1500
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 1, 'chunk_type': 'regulation_section', 'section': 'quy_dinh_di_metro', 'transport_type': 'metro'}
- Preview: QUY ĐỊNH ĐI METRO: - NGHIÊM CẤM ăn uống trong tàu và trên sân ga (phạt 100.000–300.000đ) - Không hút thuốc trong toàn bộ khu vực nhà ga - Không mang xe đạp, xe máy lên tàu (trừ xe đẩy em bé gấp gọn) - Không chụp ảnh tại khu vực vận hành, buồng lái - Không đứng sát cửa, không giữ cửa tàu - Vượt vạch vàng an toàn: có thể bị phạt - Mang theo vé/thẻ hợp lệ khi soát vé

Top 2:
- Final score: 0.5798
- Embedding score: -0.1009
- Lexical score: 0.6000
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 0, 'chunk_type': 'regulation_section', 'section': 'quy_dinh_di_xe_buyt', 'transport_type': 'bus'}
- Preview: QUY ĐỊNH ĐI XE BUÝT: - Không hút thuốc, không xả rác, giữ trật tự, không ăn uống mạnh - Nhường ghế cho người cao tuổi, khuyết tật, phụ nữ mang thai, trẻ em - Hành lý tay: không quá 20 kg - Không mang chất dễ cháy, nổ, chất độc, vật sắc nhọn nguy hiểm - Thanh toán tiền mặt hoặc thẻ điện tử trước/khi lên xe

Top 3:
- Final score: 0.4325
- Embedding score: 0.2427
- Lexical score: 0.2400
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 2, 'chunk_type': 'regulation_section', 'section': 'luat_giao_thong'}
- Preview: LUẬT GIAO THÔNG – NGHỊ ĐỊNH 100/2019/NĐ-CP (Mức phạt xe cơ giới): - Không có GPLX: 800.000 – 1.200.000đ (xe máy) | 4.000.000 – 6.000.000đ (ô tô) - Vượt đèn đỏ: 4.000.000 – 6.000.000đ (xe máy) | 6.000.000 – 8.000.000đ (ô tô) - Nồng độ cồn 0,25–0,4 mg/l khí thở: 6.000.000 – 8.000.000đ + tước GPLX 10–12 tháng - Nồng độ cồn >0,4 mg/l (xe máy): 30.000.000 – 40.000.000đ + tước GPLX 22–24 tháng - Không đội mũ bảo hiểm: 200....

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['giap bat', 'nhon', 'kim ma', 'cau giay', '32'], 'route_no': '32', 'transport_type': 'bus', 'topic': 'bus_city'}

Top 1:
- Final score: 1.3405
- Embedding score: 0.2123
- Lexical score: 1.3300
- Metadata bonus: 0.2000
- Completeness bonus: 0.1000
- Source: danh_sach_tuyen_buyt.txt
- Metadata: {'doc_id': 'danh_sach_tuyen_buyt', 'source': 'danh_sach_tuyen_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 32, 'chunk_type': 'bus_route', 'route_no': '32'}
- Preview: - Mã số: 32 | Tuyến xe buýt: BX Giáp Bát – Nhổn | Thời gian hoạt động: 5:00 - 22:30 | Giá vé tham khảo: 10.000 VNĐ

Top 2:
- Final score: 0.8677
- Embedding score: 0.3387
- Lexical score: 0.8000
- Metadata bonus: 0.1200
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 156, 'chunk_type': 'bus_route', 'route_no': '94'}
- Preview: Tuyến buýt số 94 : Bến xe Giáp Bát ⇄ Kim Bài Bến xe Giáp Bát - Giải Phóng - Kim Đồng - Trương Định - Giải Phóng - Ngọc Hồi - Cầu Quán Gánh (Quốc lộ 1A) - Thị trấn Thường Tín - Tỉnh lộ 427B - Quốc lộ 21B - Thị trấn Kim Bài

Top 3:
- Final score: 0.8380
- Embedding score: 0.2500
- Lexical score: 0.7800
- Metadata bonus: 0.1200
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 51, 'chunk_type': 'bus_route', 'route_no': '47A'}
- Preview: Tuyến xe buýt số 47A: Bến xe Long Biên <> Bát Tràng Lộ trình: Điểm trung chuyển Long Biên <> Yên Phụ <> Trần Nhật Duật <> Cầu Chương Dương <> Đê Long Biên <> Bồ Đề <> Tư Đình <> Cự Khối <> Đông Dư <> Phố Trúc <> Đường phía Tây Phố Trúc <> Rừng Cọ <> Quay đầu tại bùng binh <> Phố Trúc <> Đê Long Biên <> Bát Tràng. Thời gian hoạt động: 5:00 – 19:28. Giá vé: 7.000 VNĐ. Tần suất: 30 phút/chuyến. Tuyến xe buýt 47B: Long B...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Hard filter: topic=law_education
Soft preferences: {'preferred_terms': ['hoc bong', 'loai kha', 'muc tran hoc phi', 'dieu 7'], 'article_no': '7', 'topic': 'law_education'}

Top 1:
- Final score: 1.5853
- Embedding score: -0.0934
- Lexical score: 1.7233
- Metadata bonus: 0.1200
- Completeness bonus: 0.2500
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 6, 'chunk_type': 'legal_article', 'article_no': '7', 'article_title': 'Học bổng khuyến khích học tập'}
- Preview: Điều 7. Học bổng khuyến khích học tập 1. Đối tượng xét, cấp học bổng khuyến khích học tập: a) Học sinh trường trung học phổ thông chuyên (sau đây gọi chung là trường chuyên), học sinh trung học phổ thông chuyên trong cơ sở giáo dục đại học có kết quả rèn luyện và kết quả học tập đạt mức cao nhất trong các mức đánh giá kết quả rèn luyện, kết quả học tập của học sinh trung học phổ thông thuộc kỳ xét, cấp học bổng và có...

Top 2:
- Final score: 1.3614
- Embedding score: -0.2130
- Lexical score: 1.3900
- Metadata bonus: 0.1200
- Completeness bonus: 0.2500
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 9, 'chunk_type': 'legal_article', 'article_no': '7', 'article_title': 'Học bổng khuyến khích học tập', 'clause_no': '3'}
- Preview: Điều 7. Học bổng khuyến khích học tập 3. Mức học bổng đối với đối tượng quy định tại điểm c khoản 1 Điều này: a) Học bổng loại Khá: Mức học bổng bằng hoặc cao hơn mức trần học phí hiện hành của ngành, chuyên ngành, nghề mà người học đó phải đóng tại trường do hiệu trưởng hoặc giám đốc quy định (sau đây gọi chung là hiệu trưởng) đối với người học có điểm trung bình chung học tập và điểm rèn luyện đều đạt loại Khá trở...

Top 3:
- Final score: 1.3094
- Embedding score: 0.0570
- Lexical score: 1.4633
- Metadata bonus: 0.1200
- Completeness bonus: 0.1000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 7, 'chunk_type': 'legal_article', 'article_no': '7', 'article_title': 'Học bổng khuyến khích học tập', 'clause_no': '1'}
- Preview: Điều 7. Học bổng khuyến khích học tập 1. Đối tượng xét, cấp học bổng khuyến khích học tập: a) Học sinh trường trung học phổ thông chuyên (sau đây gọi chung là trường chuyên), học sinh trung học phổ thông chuyên trong cơ sở giáo dục đại học có kết quả rèn luyện và kết quả học tập đạt mức cao nhất trong các mức đánh giá kết quả rèn luyện, kết quả học tập của học sinh trung học phổ thông thuộc kỳ xét, cấp học bổng và có...

Nhan xet:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Danh gia: Top-1 chunk da cham dung noi dung tra loi.

# Summary Table

| Query ID | Strategy | Top-1 Source | Top-1 Score | Top-1 Content Correct? | Expected file hit in Top-3? | Nhan xet |
|---|---|---|---:|---|---|---|
| Q1 | fixed_size | danh_sach_tuyen_buyt.txt | 1.4227 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q2 | fixed_size | metro_hanoi.txt | 1.5615 | No | Yes | Da route dung vao metro nhung can uu tien manh hon tuyên 2A thay vi cac section cua tuyen 3. |
| Q3 | fixed_size | quy_dinh_phap_luat.txt | 1.3487 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q4 | fixed_size | lich_trinh_buyt.txt | 1.3969 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q5 | fixed_size | tai_lieu_phap_ly.txt | 0.6497 | No | Yes | Tai lieu phap ly dai va OCR khien retrieval van co xu huong roi vao dieu/khoan khac trong cung van ban. |
| Q1 | sentence | danh_sach_tuyen_buyt.txt | 0.9480 | No | Yes | Van con nhieu tuyen san bay va tuyen qua Cau Giay/Noi Bai gan nhau, nen can lexical route match manh hon nua. |
| Q2 | sentence | metro_hanoi.txt | 1.7313 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q3 | sentence | quy_dinh_phap_luat.txt | 1.4388 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q4 | sentence | lich_trinh_buyt.txt | 1.5006 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q5 | sentence | tai_lieu_phap_ly.txt | 0.7931 | No | Yes | Tai lieu phap ly dai va OCR khien retrieval van co xu huong roi vao dieu/khoan khac trong cung van ban. |
| Q1 | recursive | lich_trinh_buyt.txt | 0.7613 | No | Yes | Van con nhieu tuyen san bay va tuyen qua Cau Giay/Noi Bai gan nhau, nen can lexical route match manh hon nua. |
| Q2 | recursive | metro_hanoi.txt | 1.6901 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q3 | recursive | quy_dinh_phap_luat.txt | 1.4362 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q4 | recursive | lich_trinh_buyt.txt | 0.8366 | No | Yes | Van de chinh la nhieu tuyen buyt cung chia se diem Giap Bat/Cau Giay/Nhon, nen Top-1 van de lech sang tuyen khac. |
| Q5 | recursive | tai_lieu_phap_ly.txt | 1.0907 | No | Yes | Tai lieu phap ly dai va OCR khien retrieval van co xu huong roi vao dieu/khoan khac trong cung van ban. |
| Q1 | domain_aware | lich_trinh_buyt.txt | 1.0253 | No | Yes | Van con nhieu tuyen san bay va tuyen qua Cau Giay/Noi Bai gan nhau, nen can lexical route match manh hon nua. |
| Q2 | domain_aware | metro_hanoi.txt | 1.7049 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q3 | domain_aware | quy_dinh_phap_luat.txt | 1.4362 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q4 | domain_aware | danh_sach_tuyen_buyt.txt | 1.3405 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |
| Q5 | domain_aware | tai_lieu_phap_ly.txt | 1.5853 | Yes | Yes | Top-1 chunk da cham dung noi dung tra loi. |

# Comparison With Previous Benchmark

- Benchmark cu cho thay source-level Top-3 hit da tot, nhung content-level yeu: nhieu query dung file nhung sai chunk.
- Trong report cu, `fixed_size` on dinh nhat o source-level, `sentence` noi bat o Q2, va `recursive` noi bat o Q3. Tuy nhien khong co strategy nao giai quyet dong deu Q1-Q5 o muc Top-1 content.
- Benchmark toi uu nay them chunking theo domain, metadata chi tiet, query routing va hybrid reranking nen ky vong tang so query co Top-1 content dung, dac biet la Q3, Q4 va Q5.
- Q3 thuong la query cai thien ro nhat vi section `QUY DINH DI METRO` la mot don vi noi dung rat ro rang.
- Neu Q4 hoac Q5 van sai, nguyen nhan thuong den tu du lieu goc qua dai/nhieu mau giong nhau, can tach theo route/article chi tiet hon nua hoac dung embedding that.
