# Phase 2 Benchmark Results - Optimized V2

## Dataset

Danh sách file đã dùng:
- bus_brt_hanoi.txt
- danh_sach_tuyen_buyt.txt
- lich_trinh_buyt.txt
- metro_hanoi.txt
- quy_dinh_phap_luat.txt
- tai_lieu_phap_ly.txt

File bị bỏ qua:
- .gitkeep
- benchmark_queries.md
- buyt_online_hanoi.txt
- chunking_experiment_report.md
- customer_support_playbook.txt
- python_intro.txt
- rag_system_design.md
- vector_store_notes.md
- vi_retrieval_notes.md

## Các cải tiến ở vòng tối ưu 2

- Tiếp tục dùng mock embedding, chưa dùng Gemini Embedding.
- Tạo `bus_route_aggregate` để gom thông tin cùng một tuyến từ nhiều file buýt khác nhau.
- Chuẩn hóa `route_no_raw` và `route_no_norm` để query `7` và `07` match ổn định hơn.
- Tách Điều 7 tốt hơn theo khoản, và thêm chunk chi tiết cho khoản 3 cùng các điểm a/b/c.
- Tăng bonus metadata cho `route_no_norm=7`, `article_no=7`, `clause_no=3`, `chunk_type=legal_clause` và `legal_clause_point`.
- Thêm `Top-3 Content Correct?` để phân biệt rõ source-level với content-level.

## Số chunk theo strategy

- `fixed_size`: 372 chunks
- `sentence`: 132 chunks
- `recursive`: 405 chunks
- `domain_aware`: 249 chunks

## Strategy: fixed_size

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['noi bai', 'cau giay', 'cau thang long', '5 00', '21 35', '8 000', 'gia ve', 'thoi gian hoat dong'], 'route_no': '7', 'route_no_norm': '7', 'transport_type': 'bus', 'topic': 'bus_city'}

Top 1:
- Final score: 3.0303
- Embedding score: 0.2087
- Lexical score: 2.0750
- Metadata bonus: 1.1700
- Completeness bonus: 0.3000
- Source: danh_sach_tuyen_buyt.txt
- Metadata: {'doc_id': 'danh_sach_tuyen_buyt', 'source': 'danh_sach_tuyen_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '7', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 2}
- Preview: - Mã số: 7 | Tuyến xe buýt: Cầu Giấy – Nội Bài | Thời gian hoạt động: 5:00 - 21:35 | Giá vé tham khảo: 12.000 VNĐ - Mã số: 08A | Tuyến xe buýt: Long Biên – Đông Mỹ | Thời gian hoạt động: 5:05 - 22:30 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 9A | Tuyến xe buýt: Bờ Hồ – Bờ Hồ | Thời gian hoạt động: 5:00 - 21:00 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 10A | Tuyến xe buýt: Long Biên - Từ Sơn | Thời gian hoạt động: 5:05 -...

Top 2:
- Final score: 2.8416
- Embedding score: 0.0486
- Lexical score: 2.0125
- Metadata bonus: 1.1700
- Completeness bonus: 0.1800
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '7', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 11}
- Preview: ộ trình: Bến xe Giáp Bát <> Giải Phóng <> Kim Đồng <> Quay đầu tại điểm mở <> Kim Đồng <> Giải Phóng <> Ngọc Hồi <> Thường Tín <> Đường 429 <> Đường trục huyện Phú Túc, Hoàng Long <> Phúc Túc (Nhà văn hoá thôn Lưu Đông). Thời gian hoạt động: 5:45 – 18:15. Giá vé: 9.000 VNĐ. Tuyến xe buýt số 7: Cầu Giấy <> Nội Bài Lộ trình: Bãi đỗ xe Cầu Giấy <> Điểm trung chuyển Cầu Giấy <> Nguyễn Văn Huyên <> Hoàng Quốc Việt <> Phạm...

Top 3:
- Final score: 2.6228
- Embedding score: 0.2026
- Lexical score: 1.7575
- Metadata bonus: 1.1700
- Completeness bonus: 0.1000
- Source: bus_brt_hanoi.txt
- Metadata: {'doc_id': 'bus_brt_hanoi', 'source': 'bus_brt_hanoi.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '7', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 0}
- Preview: === XE BUÝT HÀ NỘI === XE BUÝT HÀ NỘI (CHI TIẾT CÁC TUYẾN QUAN TRỌNG) ================================================================================ TỔNG QUAN: - Đơn vị quản lý chính: Tổng công ty Vận tải Hà Nội (Transerco) - Website: transerco.com.vn | timbus.vn - App: Tìm Buýt (iOS & Android) | Hotline: 1900 1296 - Giá vé từ 01/11/2024: 8.000đ (<15km) đến 20.000đ (>40km) - Thẻ vé điện tử liên thông đang thí điểm...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Hard filter: topic=metro
Soft preferences: {'preferred_terms': ['cat linh', 'ha dong', '12 ga', '05 30', '22 30'], 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'transport_type': 'metro'}

Top 1:
- Final score: 1.7891
- Embedding score: -0.0280
- Lexical score: 1.5985
- Metadata bonus: 0.5000
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'fixed_size', 'chunk_index': 6}
- Preview: yến 2A (Cát Linh – Hà Đông) Ga 11 – Văn Miếu (S11): Quận Đống Đa | Gần Văn Miếu Quốc Tử Giám Ga 12 – Ga Hà Nội (S12): Quận Hoàn Kiếm | Kết nối ga đường sắt quốc gia Hà Nội GIỜ HOẠT ĐỘNG (Đoạn trên cao Nhổn – Cầu Giấy): - 05:30 – 22:00 hàng ngày - Cao điểm: theo biểu đồ thực tế - Thấp điểm & cuối tuần: 10 phút/chuyến - Tối (19:30–22:00): 15 phút/chuyến - Từ 01/02/2026: 100% soát vé điện tử sinh trắc học GIÁ VÉ METRO N...

Top 2:
- Final score: 1.7112
- Embedding score: 0.0355
- Lexical score: 1.4615
- Metadata bonus: 0.5000
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'fixed_size', 'chunk_index': 0}
- Preview: === METRO HÀ NỘI === METRO HÀ NỘI ================================================================================ === B1. TUYẾN 2A: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) === THÔNG TIN CHUNG: - Tên: Đường sắt đô thị Hà Nội tuyến 2A - Chiều dài: 13 km (toàn bộ trên cao) - Số ga: 12 ga - Khai thác chính thức: 06/11/2021 - Đơn vị vận hành: Công ty TNHH MTV Đường sắt Hà Nội (MRB) - Hotline: (024) 7307 0888 - Website: mrhan...

Top 3:
- Final score: 1.6805
- Embedding score: -0.1402
- Lexical score: 1.4615
- Metadata bonus: 0.5000
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'fixed_size', 'chunk_index': 3}
- Preview: uất cao điểm: 6 phút/chuyến - Tần suất thường: 10 phút/chuyến - Thời gian toàn tuyến: ~23 phút GIÁ VÉ METRO CÁT LINH – HÀ ĐÔNG: - 1–4 ga: 8.000 đồng - 5–8 ga: 10.000 đồng - 9–12 ga (toàn tuyến): 15.000 đồng - Vé ngày: 30.000 đồng - Vé tháng thường: 200.000 đồng - Vé tháng sinh viên: 100.000 đồng - Miễn phí: Trẻ dưới 6 tuổi, người ≥60 tuổi, người khuyết tật === B2. TUYẾN 3: NHỔN – GA HÀ NỘI (MỘT PHẦN ĐANG HOẠT ĐỘNG) =...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Hard filter: topic=law_traffic
Soft preferences: {'preferred_terms': ['an uong', '100 000', '300 000', 'san ga', 'trong tau'], 'section': 'quy_dinh_di_metro', 'transport_type': 'metro'}

Top 1:
- Final score: 1.5594
- Embedding score: -0.0263
- Lexical score: 1.2600
- Metadata bonus: 0.4200
- Completeness bonus: 0.1500
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'strategy': 'fixed_size', 'chunk_index': 1}
- Preview: METRO: - NGHIÊM CẤM ăn uống trong tàu và trên sân ga (phạt 100.000–300.000đ) - Không hút thuốc trong toàn bộ khu vực nhà ga - Không mang xe đạp, xe máy lên tàu (trừ xe đẩy em bé gấp gọn) - Không chụp ảnh tại khu vực vận hành, buồng lái - Không đứng sát cửa, không giữ cửa tàu - Vượt vạch vàng an toàn: có thể bị phạt - Mang theo vé/thẻ hợp lệ khi soát vé LUẬT GIAO THÔNG – NGHỊ ĐỊNH 100/2019/NĐ-CP (Mức phạt xe cơ giới):...

Top 2:
- Final score: 1.2887
- Embedding score: -0.2330
- Lexical score: 1.1300
- Metadata bonus: 0.4200
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'strategy': 'fixed_size', 'chunk_index': 0}
- Preview: === QUY ĐỊNH PHÁP LUẬT === QUY ĐỊNH & LUẬT PHÁP ================================================================================ QUY ĐỊNH ĐI XE BUÝT: - Không hút thuốc, không xả rác, giữ trật tự, không ăn uống mạnh - Nhường ghế cho người cao tuổi, khuyết tật, phụ nữ mang thai, trẻ em - Hành lý tay: không quá 20 kg - Không mang chất dễ cháy, nổ, chất độc, vật sắc nhọn nguy hiểm - Thanh toán tiền mặt hoặc thẻ điện tử t...

Top 3:
- Final score: 0.4986
- Embedding score: 0.1403
- Lexical score: 0.0600
- Metadata bonus: 0.2600
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'strategy': 'fixed_size', 'chunk_index': 3}
- Preview: y): 300.000 – 400.000đ | ô tô: 3.000.000 – 5.000.000đ

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['giap bat', 'nhon', 'kim ma', 'cau giay', '32'], 'route_no': '32', 'transport_type': 'bus'}

Top 1:
- Final score: 1.6066
- Embedding score: 0.1947
- Lexical score: 1.3500
- Metadata bonus: 0.4200
- Completeness bonus: 0.1000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '32', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 45}
- Preview: <> Lê Thanh Nghị <> Tạ Quang Bửu <> Đại Cồ Việt <> Phố Huế <> Hàng Bài <> Lý Thường Kiệt <> Phan Chu Trinh <> Lý Thái Tổ <> Ngô Quyền <> Hàng Vôi <> Hàng Tre <> Hàng Muối <> Trần Nhật Duật <> Điểm trung chuyển Long Biên <> Yên Phụ <> Nghi Tàm <> Âu Cơ <> Nhật Tân <> An Dương Vương <> Phú Thượng <> Dốc Chèm <> Đông Ngạc <> Chèm (Đại học Mỏ). Thời gian hoạt động: 5:05 – 21:00. Giá vé: 7.000 VNĐ. Tần suất: 10 – 25 phút/...

Top 2:
- Final score: 1.2301
- Embedding score: 0.1492
- Lexical score: 1.0600
- Metadata bonus: 0.3400
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 111}
- Preview: Giáp Bát - Giải Phóng - Lê Duẩn - Trần Nhân Tông - Trần Bình Trọng - Trần Hưng Đạo - Quán Sứ - Hai Bà Trưng - Thợ Nhuộm - Tràng Thi - Điện Biên Phủ - Trần Phú - Kim Mã – Kim Mã( đường dưới)-Đào Tấn- Đường Bưởi( đường dưới)-Cầu Giấy( đường dưới)-Điểm trung chuyển Cầu Giấy(hè trước tường rào vườn thú Hà Nội)-Cầu Giấy - Xuân Thuỷ - Hồ Tùng Mậu - đường Cầu Diễn - Quay đầu tại ngã 3 đường Cầu Diễn, Tỉnh lộ 70A mới - Nhổn...

Top 3:
- Final score: 0.9547
- Embedding score: 0.2098
- Lexical score: 0.6200
- Metadata bonus: 0.3400
- Completeness bonus: 0.0000
- Source: danh_sach_tuyen_buyt.txt
- Metadata: {'doc_id': 'danh_sach_tuyen_buyt', 'source': 'danh_sach_tuyen_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '26', 'chunk_type': 'bus_route_fragment', 'strategy': 'fixed_size', 'chunk_index': 7}
- Preview: : 5:09 - 21:00 | Giá vé tham khảo: 12.000 VNĐ - Mã số: 26 | Tuyến xe buýt: Mai Động – SVĐ Quốc gia | Thời gian hoạt động: 5:00 - 22:30 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 27 | Tuyến xe buýt: BX.Nam Thăng Long – BX.Yên Nghĩa | Thời gian hoạt động: 5:00 - 21:35 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 28 | Tuyến xe buýt: BX Giáp Bát – ĐH Mỏ | Thời gian hoạt động: 5:01 - 21:02 | Giá vé tham khảo: 10.000 VNĐ - Mã số:...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Hard filter: topic=law_education
Soft preferences: {'preferred_terms': ['hoc bong loai kha', 'muc tran hoc phi', 'diem c khoan 1', 'ket qua hoc tap', 'diem ren luyen'], 'article_no': '7', 'topic': 'law_education', 'clause_no': '3'}

Top 1:
- Final score: 0.7534
- Embedding score: 0.1302
- Lexical score: 0.7933
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'fixed_size', 'chunk_index': 35}
- Preview: giáo dục nghề nghiệp, cơ sở giáo dục đại học có kết quả học tập, rèn luyện từ loại Khá trở lên, không bị kỷ luật từ mức khiển trách trở lên trong kỳ xét cấp học bổng. 2. Mức học bổng đối với đối tượng quy định tại điểm a và điểm b khoản 1 Điều này: a) Đối với trường chuyên, trường năng khiếu: Mức học bổng cấp cho một học sinh do H ội đồng nhân dân c ấp tỉnh quy ết định nhưng không thấp hơn ba lần mức học phí làm căn...

Top 2:
- Final score: 0.7139
- Embedding score: 0.1270
- Lexical score: 0.7333
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'fixed_size', 'chunk_index': 33}
- Preview: ng học phổ thông chuyên trong cơ sở giáo dục đại học có kết quả rèn luyện và kết quả học tập đạt mức cao nhất trong các mức đánh giá kết quả rèn luyện, kết quả học tập của học sinh trung học phổ thông thuộc kỳ xét, cấp học bổng và có điểm trung bình môn chuyên của học kỳ xét , cấp từ 8,5 trở lên hoặc đạt một trong các giải từ khuyến khích trở lên trong kỳ thi học sinh giỏi cấp quốc gia do Bộ Giáo dục và Đào tạo tổ ch...

Top 3:
- Final score: 0.6095
- Embedding score: 0.2485
- Lexical score: 0.5400
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'fixed_size', 'chunk_index': 57}
- Preview: ng; b) Đối với học sinh trường dự bị đại học, trường phổ thông dân tộc nội trú: Trong thời hạn 10 ngày làm việc kể từ ngày nhập học, học sinh nộp 01 bộ hồ sơ theo quy định cho nhà trường nơi học sinh đang theo học để xét, cấp học bổng chính sách. Mỗi học sinh chỉ nộp một bộ hồ sơ một lần để đề nghị cấp học bổng trong cả thời gian học tại cơ sở giáo dục. Trong thời hạn 10 ngày làm việc kể từ ngày kết thúc nhận hồ sơ ,...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Top-3 Content Correct?: No
- Đánh giá: Cần đẩy mạnh hơn clause 3 Điều 7 hoặc point a của clause 3 lên Top-1.

## Strategy: sentence

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['noi bai', 'cau giay', 'cau thang long', '5 00', '21 35', '8 000', 'gia ve', 'thoi gian hoat dong'], 'route_no': '7', 'route_no_norm': '7', 'transport_type': 'bus', 'topic': 'bus_city'}

Top 1:
- Final score: 3.1296
- Embedding score: -0.1520
- Lexical score: 2.3250
- Metadata bonus: 1.1700
- Completeness bonus: 0.3000
- Source: bus_brt_hanoi.txt
- Metadata: {'doc_id': 'bus_brt_hanoi', 'source': 'bus_brt_hanoi.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '7', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === XE BUÝT HÀ NỘI === XE BUÝT HÀ NỘI (CHI TIẾT CÁC TUYẾN QUAN TRỌNG) ================================================================================ TỔNG QUAN: - Đơn vị quản lý chính: Tổng công ty Vận tải Hà Nội (Transerco) - Website: transerco.com.vn | timbus.vn - App: Tìm Buýt (iOS & Android) | Hotline: 1900 1296 - Giá vé từ 01/11/2024: 8.000đ (<15km) đến 20.000đ (>40km) - Thẻ vé điện tử liên thông đang thí điểm...

Top 2:
- Final score: 1.4343
- Embedding score: 0.1926
- Lexical score: 1.3625
- Metadata bonus: 0.3400
- Completeness bonus: 0.0000
- Source: danh_sach_tuyen_buyt.txt
- Metadata: {'doc_id': 'danh_sach_tuyen_buyt', 'source': 'danh_sach_tuyen_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '1', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === DANH SÁCH TUYẾN XE BUÝT HÀ NỘI (TỪ EXCEL) === - Mã số: 1 | Tuyến xe buýt: BX Gia Lâm - BX Yên Nghĩa | Thời gian hoạt động: 5:00 – 21:00 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 2 | Tuyến xe buýt: Bác Cổ – BX Yên Nghĩa | Thời gian hoạt động: 5:00 – 22:30 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 03A | Tuyến xe buýt: BX Giáp Bát – BX Gia Lâm | Thời gian hoạt động: 5:00 – 21:00 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 0...

Top 3:
- Final score: 1.2986
- Embedding score: 0.1411
- Lexical score: 1.1675
- Metadata bonus: 0.3400
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 53}
- Preview: Tuyến buýt số 04 : Long Biên ⇄ Bến xe Nước Ngầm Long Biên-quay đầu tại đối diện phố Hàng Than-Yên Phụ- Điểm trung chuyển Long Biên - Trần Nhật Duật - Nguyễn Hữu Huân - Lý Thái Tổ - Ngô Quyền - Hai Bà Trưng - Lê Thánh Tông - Trần Thánh Tông - Tăng Bạt Hổ - Yecxanh - Lò Đúc - Kim Ngưu - Nguyễn Tam Trinh-Cầu Voi- Tam Trinh - Đường Lĩnh Nam - Đường dẫn cầu Thanh Trì - Pháp Vân - Rẽ trái tại nút giao đường vành đai 3 và đ...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Hard filter: topic=metro
Soft preferences: {'preferred_terms': ['cat linh', 'ha dong', '12 ga', '05 30', '22 30'], 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'transport_type': 'metro'}

Top 1:
- Final score: 1.9636
- Embedding score: -0.0397
- Lexical score: 1.6854
- Metadata bonus: 0.5000
- Completeness bonus: 0.2000
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === METRO HÀ NỘI === METRO HÀ NỘI ================================================================================ === B1. TUYẾN 2A: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) === THÔNG TIN CHUNG: - Tên: Đường sắt đô thị Hà Nội tuyến 2A - Chiều dài: 13 km (toàn bộ trên cao) - Số ga: 12 ga - Khai thác chính thức: 06/11/2021 - Đơn vị vận hành: Công ty TNHH MTV Đường sắt Hà Nội (MRB) - Hotline: (024) 7307 0888 - Website: mrhan...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Hard filter: topic=law_traffic
Soft preferences: {'preferred_terms': ['an uong', '100 000', '300 000', 'san ga', 'trong tau'], 'section': 'quy_dinh_di_metro', 'transport_type': 'metro'}

Top 1:
- Final score: 1.6507
- Embedding score: 0.1239
- Lexical score: 1.3600
- Metadata bonus: 0.4200
- Completeness bonus: 0.1500
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === QUY ĐỊNH PHÁP LUẬT === QUY ĐỊNH & LUẬT PHÁP ================================================================================ QUY ĐỊNH ĐI XE BUÝT: - Không hút thuốc, không xả rác, giữ trật tự, không ăn uống mạnh - Nhường ghế cho người cao tuổi, khuyết tật, phụ nữ mang thai, trẻ em - Hành lý tay: không quá 20 kg - Không mang chất dễ cháy, nổ, chất độc, vật sắc nhọn nguy hiểm - Thanh toán tiền mặt hoặc thẻ điện tử t...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['giap bat', 'nhon', 'kim ma', 'cau giay', '32'], 'route_no': '32', 'transport_type': 'bus'}

Top 1:
- Final score: 1.7161
- Embedding score: 0.1032
- Lexical score: 1.4200
- Metadata bonus: 0.4200
- Completeness bonus: 0.1800
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '32', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 31}
- Preview: Tuyến xe buýt số 32: Bến xe Giáp Bát <> Nhổn Lộ trình: Bến xe Giáp Bát <> Giải Phóng <> Lê Duẩn <> Trần Nhân Tông <> Trần Bình Trọng <> Trần Hưng Đạo <> Quán Sứ <> Hai Bà Trưng <> Thợ Nhuộm <> Tràng Thị <> Điện Biên Phủ <> Trần Phú <> Kim Mã <> Càu Giấy <> Điểm trung chuyển Cầu Giấy <> Cầu Giấy <> Xuân Thuỷ <> Hồ Tùng Mậu <> Diễn <> Đường 3/2 <> Phố Nhổn <> Nhổn. Thời gian hoạt động: 5:00 – 22:30. Giá vé: 7.000 VNĐ....

Top 2:
- Final score: 1.4377
- Embedding score: 0.1838
- Lexical score: 1.3700
- Metadata bonus: 0.3400
- Completeness bonus: 0.0000
- Source: bus_brt_hanoi.txt
- Metadata: {'doc_id': 'bus_brt_hanoi', 'source': 'bus_brt_hanoi.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '7', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === XE BUÝT HÀ NỘI === XE BUÝT HÀ NỘI (CHI TIẾT CÁC TUYẾN QUAN TRỌNG) ================================================================================ TỔNG QUAN: - Đơn vị quản lý chính: Tổng công ty Vận tải Hà Nội (Transerco) - Website: transerco.com.vn | timbus.vn - App: Tìm Buýt (iOS & Android) | Hotline: 1900 1296 - Giá vé từ 01/11/2024: 8.000đ (<15km) đến 20.000đ (>40km) - Thẻ vé điện tử liên thông đang thí điểm...

Top 3:
- Final score: 1.2522
- Embedding score: 0.1267
- Lexical score: 1.1000
- Metadata bonus: 0.3400
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'sentence', 'chunk_index': 19}
- Preview: Tuyến xe buýt 20C: Nhổn <> Võng Xuyên Lộ trình: Nhổn (Điểm trung chuyển xe buýt Nhổn) <> Nhổn <> Quay đầu tại Cumj Công nghiệp vừa và nhỏ Từ Liêm <> Quốc lộ 32 <> Ngã tư Nhổn <> Tây Tựu <> Thượng Cát <> Đê Liên Trì <> Đê Hữu Hồng <> Tiên Tân <> Trung Châu <> Hát Môn <> Ngã tư huyện (Cụm 11, Võng Xuyên). Thời gian hoạt động: 5:23 – 18:08. Giá vé: 9.000 VNĐ. Tần suất: 30 phút/chuyến. Tuyến xe buýt 21A: Bến xe Giáp Bát...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Hard filter: topic=law_education
Soft preferences: {'preferred_terms': ['hoc bong loai kha', 'muc tran hoc phi', 'diem c khoan 1', 'ket qua hoc tap', 'diem ren luyen'], 'article_no': '7', 'topic': 'law_education', 'clause_no': '3'}

Top 1:
- Final score: 1.4407
- Embedding score: 0.0332
- Lexical score: 1.4767
- Metadata bonus: 0.2000
- Completeness bonus: 0.1000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'article_no': '7', 'article_title': 'Học bổng khuyến khích học tập', 'strategy': 'sentence', 'chunk_index': 8}
- Preview: Điều 7. Học bổng khuyến khích học tập 1. Đối tượng xét, cấp học bổng khuyến khích học tập: a) Học sinh trường trung học phổ thông chuyên (sau đây gọi chung là trường chuyên), học sinh trung học phổ thông chuyên trong cơ sở giáo dục đại học có kết quả rèn luyện và kết quả học tập đạt mức cao nhất trong các mức đánh giá kết quả rèn luyện, kết quả học tập của học sinh trung học phổ thông thuộc kỳ xét, cấp học bổng và có...

Top 2:
- Final score: 0.8463
- Embedding score: 0.1653
- Lexical score: 0.9267
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'article_no': '8', 'article_title': 'Học bổng khuyến khích học tập', 'strategy': 'sentence', 'chunk_index': 11}
- Preview: Việc xét, cấp học bổng đối với đối tượng quy định tại điểm c khoản 1 Điều này: a) Hiệu trưởng căn cứ vào nguồn học bổng khuyến khích học tập xác định số lượng suất học bổng cho từng khóa học, ngành học. Trong trường hợp số lượng người học thuộc diện được xét, cấp học bổng nhiều hơn số suất học bổng thì việc xét, cấp học bổng do hiệu trưởng quyết định; b) Hiệu trưởng căn cứ vào kết quả học tập và rèn luyện của người h...

Top 3:
- Final score: 0.8140
- Embedding score: 0.0554
- Lexical score: 0.9067
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'sentence', 'chunk_index': 9}
- Preview: 3. Mức học bổng đối với đối tượng quy định tại điểm c khoản 1 Điều này: a) Học bổng loại Khá: Mức học bổng bằng hoặc cao hơn mức trần học phí hiện hành của ngành, chuyên ngành, nghề mà người học đó phải đóng tại trường do hiệu trưởng hoặc giám đốc quy định (sau đây gọi chung là hiệu trưởng) đối với người học có điểm trung bình chung học tập và điểm rèn luyện đều đạt loại Khá trở lên. Đối với các trường tư thục mức họ...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Top-3 Content Correct?: No
- Đánh giá: Cần đẩy mạnh hơn clause 3 Điều 7 hoặc point a của clause 3 lên Top-1.

## Strategy: recursive

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['noi bai', 'cau giay', 'cau thang long', '5 00', '21 35', '8 000', 'gia ve', 'thoi gian hoat dong'], 'route_no': '7', 'route_no_norm': '7', 'transport_type': 'bus', 'topic': 'bus_city'}

Top 1:
- Final score: 2.8394
- Embedding score: 0.0732
- Lexical score: 2.0025
- Metadata bonus: 1.1700
- Completeness bonus: 0.1800
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '7', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 18}
- Preview: Lộ trình: Bến xe Giáp Bát <> Giải Phóng <> Kim Đồng <> Quay đầu tại điểm mở <> Kim Đồng <> Giải Phóng <> Ngọc Hồi <> Thường Tín <> Đường 429 <> Đường trục huyện Phú Túc, Hoàng Long <> Phúc Túc (Nhà văn hoá thôn Lưu Đông). Thời gian hoạt động: 5:45 – 18:15. Giá vé: 9.000 VNĐ. Tuyến xe buýt số 7: Cầu Giấy <> Nội Bài

Top 2:
- Final score: 2.5299
- Embedding score: -0.1055
- Lexical score: 1.6975
- Metadata bonus: 1.1700
- Completeness bonus: 0.1000
- Source: bus_brt_hanoi.txt
- Metadata: {'doc_id': 'bus_brt_hanoi', 'source': 'bus_brt_hanoi.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '7', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 1}
- Preview: TUYẾN 07 (Nội Bài – Bến xe Mỹ Đình): - Lộ trình: Sân bay Nội Bài → QL2 → Cầu Thăng Long → Trần Duy Hưng → Bến xe Mỹ Đình - Giờ: 05:30 – 22:00 | Tần suất: 15–20 phút | Giá: 9.000 đồng - Thời gian: 45–50 phút | Đây là tuyến phổ biến nhất từ Nội Bài TUYẾN 17 (Nội Bài – Long Biên): - Lộ trình: Sân bay Nội Bài → QL5 → Cầu Đuống → Long Biên - Giờ: 05:30 – 22:00 | Tần suất: 20–30 phút | Giá: 9.000 đồng

Top 3:
- Final score: 1.0883
- Embedding score: 0.3047
- Lexical score: 0.8000
- Metadata bonus: 0.3400
- Completeness bonus: 0.0000
- Source: danh_sach_tuyen_buyt.txt
- Metadata: {'doc_id': 'danh_sach_tuyen_buyt', 'source': 'danh_sach_tuyen_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 35}
- Preview: - Mã số: Phủ Tây Hồ | Tuyến xe buýt: 31, 55, 57, 58, 90 | Thời gian hoạt động: Đền thờ thánh Mẫu, nổi tiếng với kiến trúc đẹp và không gian linh thiêng. - Mã số: Cầu Long Biên | Tuyến xe buýt: 14, 21, 35, 50, 55 | Thời gian hoạt động: Cây cầu lịch sử bắc qua sông Hồng, từng chứng kiến nhiều biến cố lịch sử của thủ đô. - Mã số: Chợ Đồng Xuân | Tuyến xe buýt: 01, 14, 36, 52, 55 | Thời gian hoạt động: Chợ truyền thống l...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Top-3 Content Correct?: No
- Đánh giá: Vẫn cần gom route 7 đầy đủ hơn để một chunk duy nhất chứa lộ trình + giờ + giá.

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Hard filter: topic=metro
Soft preferences: {'preferred_terms': ['cat linh', 'ha dong', '12 ga', '05 30', '22 30'], 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'transport_type': 'metro'}

Top 1:
- Final score: 1.9179
- Embedding score: -0.0149
- Lexical score: 1.6085
- Metadata bonus: 0.5000
- Completeness bonus: 0.2000
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'recursive', 'chunk_index': 3}
- Preview: GIỜ HOẠT ĐỘNG: - Chuyến đầu: 05:30 - Chuyến cuối: 22:30 - Tần suất cao điểm: 6 phút/chuyến - Tần suất thường: 10 phút/chuyến - Thời gian toàn tuyến: ~23 phút GIÁ VÉ METRO CÁT LINH – HÀ ĐÔNG: - 1–4 ga: 8.000 đồng - 5–8 ga: 10.000 đồng - 9–12 ga (toàn tuyến): 15.000 đồng - Vé ngày: 30.000 đồng - Vé tháng thường: 200.000 đồng - Vé tháng sinh viên: 100.000 đồng - Miễn phí: Trẻ dưới 6 tuổi, người ≥60 tuổi, người khuyết tậ...

Top 2:
- Final score: 1.7085
- Embedding score: 0.0200
- Lexical score: 1.4615
- Metadata bonus: 0.5000
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'recursive', 'chunk_index': 0}
- Preview: === METRO HÀ NỘI === METRO HÀ NỘI ================================================================================ === B1. TUYẾN 2A: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) === THÔNG TIN CHUNG: - Tên: Đường sắt đô thị Hà Nội tuyến 2A - Chiều dài: 13 km (toàn bộ trên cao) - Số ga: 12 ga - Khai thác chính thức: 06/11/2021 - Đơn vị vận hành: Công ty TNHH MTV Đường sắt Hà Nội (MRB) - Hotline: (024) 7307 0888 - Website: mrhan...

Top 3:
- Final score: 1.6948
- Embedding score: -0.0580
- Lexical score: 1.4615
- Metadata bonus: 0.5000
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_fragment', 'strategy': 'recursive', 'chunk_index': 1}
- Preview: LỘ TRÌNH 12 GA (Cát Linh → Hà Đông): Ga 01 – Cát Linh: Quận Đống Đa | Điểm đầu, gần Đại học Kiến trúc, kết nối nhiều tuyến buýt Ga 02 – La Thành: Quận Đống Đa | Gần Văn Miếu Quốc Tử Giám (đi bộ ~800m) Ga 03 – Thái Hà: Quận Đống Đa | Khu thương mại Thái Hà, nhiều quán ăn Ga 04 – Láng: Quận Đống Đa | Gần ĐH Quốc gia Hà Nội, bệnh viện Nhi Ga 05 – Thượng Đình: Quận Thanh Xuân | Khu công nghiệp cao su Thượng Đình Ga 06 –...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Hard filter: topic=law_traffic
Soft preferences: {'preferred_terms': ['an uong', '100 000', '300 000', 'san ga', 'trong tau'], 'section': 'quy_dinh_di_metro', 'transport_type': 'metro'}

Top 1:
- Final score: 1.6484
- Embedding score: 0.1111
- Lexical score: 1.3600
- Metadata bonus: 0.4200
- Completeness bonus: 0.1500
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'quy_dinh_di_metro', 'transport_type': 'metro', 'strategy': 'recursive', 'chunk_index': 1}
- Preview: QUY ĐỊNH ĐI METRO: - NGHIÊM CẤM ăn uống trong tàu và trên sân ga (phạt 100.000–300.000đ) - Không hút thuốc trong toàn bộ khu vực nhà ga - Không mang xe đạp, xe máy lên tàu (trừ xe đẩy em bé gấp gọn) - Không chụp ảnh tại khu vực vận hành, buồng lái - Không đứng sát cửa, không giữ cửa tàu - Vượt vạch vàng an toàn: có thể bị phạt - Mang theo vé/thẻ hợp lệ khi soát vé

Top 2:
- Final score: 0.7697
- Embedding score: -0.0188
- Lexical score: 0.5200
- Metadata bonus: 0.2600
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'quy_dinh_di_xe_buyt', 'transport_type': 'bus', 'strategy': 'recursive', 'chunk_index': 0}
- Preview: === QUY ĐỊNH PHÁP LUẬT === QUY ĐỊNH & LUẬT PHÁP ================================================================================ QUY ĐỊNH ĐI XE BUÝT: - Không hút thuốc, không xả rác, giữ trật tự, không ăn uống mạnh - Nhường ghế cho người cao tuổi, khuyết tật, phụ nữ mang thai, trẻ em - Hành lý tay: không quá 20 kg - Không mang chất dễ cháy, nổ, chất độc, vật sắc nhọn nguy hiểm - Thanh toán tiền mặt hoặc thẻ điện tử t...

Top 3:
- Final score: 0.4948
- Embedding score: -0.0296
- Lexical score: 0.1000
- Metadata bonus: 0.2600
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'chunk_type': 'regulation_fragment', 'section': 'luat_giao_thong', 'strategy': 'recursive', 'chunk_index': 2}
- Preview: LUẬT GIAO THÔNG – NGHỊ ĐỊNH 100/2019/NĐ-CP (Mức phạt xe cơ giới): - Không có GPLX: 800.000 – 1.200.000đ (xe máy) | 4.000.000 – 6.000.000đ (ô tô) - Vượt đèn đỏ: 4.000.000 – 6.000.000đ (xe máy) | 6.000.000 – 8.000.000đ (ô tô) - Nồng độ cồn 0,25–0,4 mg/l khí thở: 6.000.000 – 8.000.000đ + tước GPLX 10–12 tháng - Nồng độ cồn >0,4 mg/l (xe máy): 30.000.000 – 40.000.000đ + tước GPLX 22–24 tháng - Không đội mũ bảo hiểm: 200....

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['giap bat', 'nhon', 'kim ma', 'cau giay', '32'], 'route_no': '32', 'transport_type': 'bus'}

Top 1:
- Final score: 1.4524
- Embedding score: 0.1710
- Lexical score: 1.1500
- Metadata bonus: 0.4200
- Completeness bonus: 0.0800
- Source: bus_brt_hanoi.txt
- Metadata: {'doc_id': 'bus_brt_hanoi', 'source': 'bus_brt_hanoi.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'route_no': '32', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 4}
- Preview: TUYẾN 32 (Bến xe Mỹ Đình – ĐH Quốc gia HN): - Lộ trình: Bến xe Mỹ Đình → Phạm Hùng → Nhổn → Hoài Đức → ĐH Quốc gia HN - Giờ: 05:30 – 21:30 | Tần suất: 20–25 phút | Giá: 9.000 đồng TUYẾN 34 (Trần Khánh Dư – Nhổn): - Lộ trình: Trần Khánh Dư → Hoàn Kiếm → Kim Mã → Cầu Giấy → Nhổn - Giờ: 05:30 – 21:30 | Tần suất: 15–20 phút | Giá: 9.000 đồng - Kết nối Metro tuyến 3 tại ga Nhổn và Cầu Giấy

Top 2:
- Final score: 1.1170
- Embedding score: 0.1712
- Lexical score: 0.8800
- Metadata bonus: 0.3400
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 125}
- Preview: Tuyến buýt số 24 : Long Biên ⇄ Cầu Giấy Long Biên - Trần Nhật Duật - Trần Quang Khải - Trần Khánh Dư - Trung chuyển xe buýt Trần Khánh Dư - Nguyễn Khoái - Minh Khai - Đại La - Trường Chinh - Ngã tư Sở - Đường Láng - Cầu Giấy Tuyến buýt số 25 : BV Nhiệt đới TW CS2 ⇄ Bến xe Giáp Bát

Top 3:
- Final score: 1.0150
- Embedding score: 0.1830
- Lexical score: 0.7200
- Metadata bonus: 0.3400
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'chunk_type': 'bus_route_fragment', 'strategy': 'recursive', 'chunk_index': 93}
- Preview: Bến xe Nước Ngầm - Ngọc Hồi - Giải Phóng - Bến xe Giáp Bát (Quảng trường Bến xe Giáp Bát) - Giải Phóng - Đại La - Minh Khai - Cầu Vĩnh Tuy - Đàm Quang Trung - Chu Huy Mân - Hội Xá - Vũ Xuân Thiều - Đường Phúc Lợi - Ngõ 193 Phúc lợi - Ngách 195/9 Phúc Lợi - Ngõ 195 Phúc Lợi - Phúc Lợi (đối diện trường THPT Phúc Lợi). Tuyến buýt số 04 : Long Biên ⇄ Bến xe Nước Ngầm

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Top-3 Content Correct?: No
- Đánh giá: Cần tinh chỉnh thêm metadata và hybrid reranking.

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Hard filter: topic=law_education
Soft preferences: {'preferred_terms': ['hoc bong loai kha', 'muc tran hoc phi', 'diem c khoan 1', 'ket qua hoc tap', 'diem ren luyen'], 'article_no': '7', 'topic': 'law_education', 'clause_no': '3'}

Top 1:
- Final score: 1.1616
- Embedding score: 0.2237
- Lexical score: 1.1500
- Metadata bonus: 0.2000
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'article_no': '7', 'article_title': 'Học bổng khuyến khích học tập', 'strategy': 'recursive', 'chunk_index': 31}
- Preview: Điều 7. Học bổng khuyến khích học tập 1. Đối tượng xét, cấp học bổng khuyến khích học tập: a) Học sinh trường trung học phổ thông chuyên (sau đây gọi chung là trường chuyên), học sinh trung học phổ thông chuyên trong cơ sở giáo dục đại học có kết quả rèn luyện và kết quả học tập đạt mức cao nhất trong các mức đánh giá kết quả rèn luyện, kết quả học tập của học sinh trung học phổ thông thuộc kỳ xét, cấp học bổng và có...

Top 2:
- Final score: 0.6714
- Embedding score: 0.1316
- Lexical score: 0.6667
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'article_title': 'Học bổng khuyến khích học tập', 'strategy': 'recursive', 'chunk_index': 41}
- Preview: d) Ngoài học bổng khuyến khích học tập theo quy định tại Nghị định này, Chủ tịch Ủy ban nhân dân cấp tỉnh có thể có các chế độ, chính sách khác đối với học sinh trường chuyên, trường năng khiếu thuộc địa phương hoặc do địa phương quản lý. 6. Việc xét, cấp học bổng đối với đối tượng quy định tại điểm c khoản 1 Điều này: a) Hiệu trưởng căn cứ vào nguồn học bổng khuyến khích học tập xác định số lượng suất học bổng cho t...

Top 3:
- Final score: 0.6701
- Embedding score: 0.1492
- Lexical score: 0.6600
- Metadata bonus: 0.0400
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'chunk_type': 'legal_fragment', 'strategy': 'recursive', 'chunk_index': 36}
- Preview: Khá trở lên. Đối với các trường tư thục mức học bổng tối thiểu do hiệu trưởng quy định. Đối với những ngành nghề đào tạo không thu học phí thì áp dụng theo đơn giá được Nhà nước đặt hàng, giao nhiệm vụ cho nhóm ngành đào tạo của trường; b) Học bổng loại Giỏi: Mức học bổng cao hơn loại khá do hiệu trưởng quy định đối với người học có điểm trung bình chung học tập đạt loại Giỏi trở lên và điểm rèn luyện đạt loại tốt tr...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Top-3 Content Correct?: No
- Đánh giá: Cần đẩy mạnh hơn clause 3 Điều 7 hoặc point a của clause 3 lên Top-1.

## Strategy: domain_aware

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['noi bai', 'cau giay', 'cau thang long', '5 00', '21 35', '8 000', 'gia ve', 'thoi gian hoat dong'], 'route_no': '7', 'route_no_norm': '7', 'transport_type': 'bus', 'topic': 'bus_city'}

Top 1:
- Final score: 3.9272
- Embedding score: -0.1267
- Lexical score: 2.4375
- Metadata bonus: 1.3900
- Completeness bonus: 0.8000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'bus_route_7', 'source': 'lich_trinh_buyt.txt', 'source_parts': ['bus_brt_hanoi.txt', 'danh_sach_tuyen_buyt.txt', 'lich_trinh_buyt.txt'], 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 5, 'chunk_type': 'bus_route_aggregate', 'route_no': '7', 'route_no_raw': '7', 'route_no_norm': '7'}
- Preview: Tuyến buýt số 7 (tổng hợp theo tuyến) [lich_trinh_buyt.txt] Tuyến xe buýt số 7: Cầu Giấy <> Nội Bài Lộ trình: Bãi đỗ xe Cầu Giấy <> Điểm trung chuyển Cầu Giấy <> Nguyễn Văn Huyên <> Hoàng Quốc Việt <> Phạm Văn Đồng <> Cầu Thăng Long <> Võ Văn Kiệt <> Đường dưới cầu vượt Kim Chung <> Võ Văn Kiệt <> Sân bay Nội Bài. Thời gian hoạt động: 5:00 – 21:35. Giá vé: 8.000 VNĐ. [lich_trinh_buyt.txt] Tuyến buýt số 07 : Cầu Giấy...

Top 2:
- Final score: 1.1702
- Embedding score: 0.2431
- Lexical score: 1.1425
- Metadata bonus: 0.2100
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'bus_route_9', 'source': 'lich_trinh_buyt.txt', 'source_parts': ['lich_trinh_buyt.txt'], 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 7, 'chunk_type': 'bus_route_aggregate', 'route_no': '9', 'route_no_raw': '9', 'route_no_norm': '9'}
- Preview: Tuyến buýt số 9 (tổng hợp theo tuyến) [lich_trinh_buyt.txt] Tuyến xe buýt số 9: Bờ Hồ <> Bờ Hồ Lộ trình: Bãi đỗ xe Bờ Hồ <> Đình Tiên Hoàng <> Lê Thái Tổ <> Bà Triệu <> Hồ Xuân Hương <> Nguyễn Bỉnh Khiêm <> Trần Nhân Tông <> Lê Duẩn <> Khâm Thiên <> Đường mới (Vành đai 1) <> Quay đầu tại điểm mở dải phân cách <> Đường mới (Vành đai 1) <> Nguyễn Lương Bằng <> Tây Sơn <> Ngã tư Sở <> Láng <> Láng Hạ <> Huỳnh Thúc Kháng...

Top 3:
- Final score: 1.1190
- Embedding score: 0.1827
- Lexical score: 1.0800
- Metadata bonus: 0.2100
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'bus_route_26', 'source': 'lich_trinh_buyt.txt', 'source_parts': ['danh_sach_tuyen_buyt.txt', 'lich_trinh_buyt.txt'], 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 25, 'chunk_type': 'bus_route_aggregate', 'route_no': '26', 'route_no_raw': '26', 'route_no_norm': '26'}
- Preview: Tuyến buýt số 26 (tổng hợp theo tuyến) [lich_trinh_buyt.txt] Tuyến buýt số 26 : Mai Động ⇄ Sân vận động Quốc Gia Mai Động (Đường vào XN buýt Thăng Long cũ, qua cầu Đền Lừ, gần bãi đỗ xe Đền Lừ 2) - Nguyễn Tam Trinh - Cầu Voi - Nguyễn Tam Trinh- Kim Ngưu - Thanh Nhàn - Lê Thanh Nghị - Giải Phóng - Xã Đàn - Phạm Ngọc Thạch - Chùa Bộc - Thái Hà - Huỳnh Thúc Kháng - Nguyễn Chí Thanh - Đê La Thành - Cầu Giấy - Điểm trung...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Hard filter: topic=metro
Soft preferences: {'preferred_terms': ['cat linh', 'ha dong', '12 ga', '05 30', '22 30'], 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'transport_type': 'metro'}

Top 1:
- Final score: 1.9405
- Embedding score: -0.1715
- Lexical score: 1.6854
- Metadata bonus: 0.5000
- Completeness bonus: 0.2000
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'domain_aware', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_section', 'chunk_index': 0, 'section': 'full_route'}
- Preview: === B1. TUYẾN 2A: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) === THÔNG TIN CHUNG: - Tên: Đường sắt đô thị Hà Nội tuyến 2A - Chiều dài: 13 km (toàn bộ trên cao) - Số ga: 12 ga - Khai thác chính thức: 06/11/2021 - Đơn vị vận hành: Công ty TNHH MTV Đường sắt Hà Nội (MRB) - Hotline: (024) 7307 0888 - Website: mrhanoi.gov.vn LỘ TRÌNH 12 GA (Cát Linh → Hà Đông): Ga 01 – Cát Linh: Quận Đống Đa | Điểm đầu, gần Đại học Kiến trúc, kế...

Top 2:
- Final score: 1.7496
- Embedding score: 0.0891
- Lexical score: 1.4446
- Metadata bonus: 0.5000
- Completeness bonus: 0.1200
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'domain_aware', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_section', 'chunk_index': 3, 'section': 'gio_hoat_dong'}
- Preview: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) GIỜ HOẠT ĐỘNG : - Chuyến đầu: 05:30 - Chuyến cuối: 22:30 - Tần suất cao điểm: 6 phút/chuyến - Tần suất thường: 10 phút/chuyến - Thời gian toàn tuyến: ~23 phút

Top 3:
- Final score: 1.6970
- Embedding score: -0.0459
- Lexical score: 1.4615
- Metadata bonus: 0.5000
- Completeness bonus: 0.0800
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'domain_aware', 'route_no': '2A', 'line_name': 'cat_linh_ha_dong', 'chunk_type': 'metro_section', 'chunk_index': 2, 'section': 'lo_trinh_va_ga'}
- Preview: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) LỘ TRÌNH 12 GA (Cát Linh → Hà Đông): Ga 01 – Cát Linh: Quận Đống Đa | Điểm đầu, gần Đại học Kiến trúc, kết nối nhiều tuyến buýt Ga 02 – La Thành: Quận Đống Đa | Gần Văn Miếu Quốc Tử Giám (đi bộ ~800m) Ga 03 – Thái Hà: Quận Đống Đa | Khu thương mại Thái Hà, nhiều quán ăn Ga 04 – Láng: Quận Đống Đa | Gần ĐH Quốc gia Hà Nội, bệnh viện Nhi Ga 05 – Thượng Đình: Quận Thanh Xuân | Khu côn...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Hard filter: topic=law_traffic
Soft preferences: {'preferred_terms': ['an uong', '100 000', '300 000', 'san ga', 'trong tau'], 'section': 'quy_dinh_di_metro', 'transport_type': 'metro'}

Top 1:
- Final score: 1.6484
- Embedding score: 0.1111
- Lexical score: 1.3600
- Metadata bonus: 0.4200
- Completeness bonus: 0.1500
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 1, 'chunk_type': 'regulation_section', 'section': 'quy_dinh_di_metro', 'transport_type': 'metro'}
- Preview: QUY ĐỊNH ĐI METRO: - NGHIÊM CẤM ăn uống trong tàu và trên sân ga (phạt 100.000–300.000đ) - Không hút thuốc trong toàn bộ khu vực nhà ga - Không mang xe đạp, xe máy lên tàu (trừ xe đẩy em bé gấp gọn) - Không chụp ảnh tại khu vực vận hành, buồng lái - Không đứng sát cửa, không giữ cửa tàu - Vượt vạch vàng an toàn: có thể bị phạt - Mang theo vé/thẻ hợp lệ khi soát vé

Top 2:
- Final score: 0.7553
- Embedding score: -0.1009
- Lexical score: 0.5200
- Metadata bonus: 0.2600
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 0, 'chunk_type': 'regulation_section', 'section': 'quy_dinh_di_xe_buyt', 'transport_type': 'bus'}
- Preview: QUY ĐỊNH ĐI XE BUÝT: - Không hút thuốc, không xả rác, giữ trật tự, không ăn uống mạnh - Nhường ghế cho người cao tuổi, khuyết tật, phụ nữ mang thai, trẻ em - Hành lý tay: không quá 20 kg - Không mang chất dễ cháy, nổ, chất độc, vật sắc nhọn nguy hiểm - Thanh toán tiền mặt hoặc thẻ điện tử trước/khi lên xe

Top 3:
- Final score: 0.5815
- Embedding score: 0.2427
- Lexical score: 0.1600
- Metadata bonus: 0.2600
- Completeness bonus: 0.0000
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 2, 'chunk_type': 'regulation_section', 'section': 'luat_giao_thong'}
- Preview: LUẬT GIAO THÔNG – NGHỊ ĐỊNH 100/2019/NĐ-CP (Mức phạt xe cơ giới): - Không có GPLX: 800.000 – 1.200.000đ (xe máy) | 4.000.000 – 6.000.000đ (ô tô) - Vượt đèn đỏ: 4.000.000 – 6.000.000đ (xe máy) | 6.000.000 – 8.000.000đ (ô tô) - Nồng độ cồn 0,25–0,4 mg/l khí thở: 6.000.000 – 8.000.000đ + tước GPLX 10–12 tháng - Nồng độ cồn >0,4 mg/l (xe máy): 30.000.000 – 40.000.000đ + tước GPLX 22–24 tháng - Không đội mũ bảo hiểm: 200....

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Hard filter: topic=bus_city
Soft preferences: {'preferred_terms': ['giap bat', 'nhon', 'kim ma', 'cau giay', '32'], 'route_no': '32', 'transport_type': 'bus'}

Top 1:
- Final score: 1.4321
- Embedding score: 0.1950
- Lexical score: 1.0200
- Metadata bonus: 0.5600
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'bus_route_3A', 'source': 'lich_trinh_buyt.txt', 'source_parts': ['danh_sach_tuyen_buyt.txt', 'lich_trinh_buyt.txt'], 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 38, 'chunk_type': 'bus_route_aggregate', 'route_no': '3A', 'route_no_raw': '3A', 'route_no_norm': '3A'}
- Preview: Tuyến buýt số 3A (tổng hợp theo tuyến) [lich_trinh_buyt.txt] Tuyến xe buýt số 3A: Bến xe Giáp Bát <> Bến xe Gia Lâm Lộ trình: Bến xe Giáp Bát <> Giải Phóng <> Lê Duẩn <> Nguyễn Thượng Hiền <> Yết Kiêu <> Trần Hưng Đạo <> Trần Khánh Dư <> Trần Quang Khải <> Trần Nhật Duật <> Long Biên (Điểm quay đầu trước phố Hàng Khoai) <> Trần Nhật Duật <> Cầu Chương Dương <> Nguyễn Văn Cừ <> Nguyễn Sơn <> Ngọc Lâm <> Ngô Gia Khảm <...

Top 2:
- Final score: 1.4282
- Embedding score: 0.1725
- Lexical score: 1.0200
- Metadata bonus: 0.5600
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'bus_route_6A', 'source': 'lich_trinh_buyt.txt', 'source_parts': ['danh_sach_tuyen_buyt.txt', 'lich_trinh_buyt.txt'], 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 62, 'chunk_type': 'bus_route_aggregate', 'route_no': '6A', 'route_no_raw': '6A', 'route_no_norm': '6A'}
- Preview: Tuyến buýt số 6A (tổng hợp theo tuyến) [lich_trinh_buyt.txt] Tuyến xe buýt số 6A: Bến xe Giáp Bát <> Cầu Giẽ Lộ trình: Bến xe Giáp Bát <> Giải Phóng <> Kim Đồng <> Giải Phóng <> Ngọc Hồi <> Quốc lộ 1 <> Liên Ninh <> Quán Gánh <> Thị trấn Thường Tín <> Tía <> Đỗ Xá <> Nghệ <> Thị trấn Phú Xuyên <> Guột <> Cầu Giẽ (Ngã ba đường ra cao tốc Pháp Vân – Cầu Giẽ). Thời gian hoạt động: 5:03 – 20:05. Giá vé: 9.000 VNĐ. [lich_...

Top 3:
- Final score: 1.4228
- Embedding score: 0.1416
- Lexical score: 1.0200
- Metadata bonus: 0.5600
- Completeness bonus: 0.0000
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'bus_route_22C', 'source': 'lich_trinh_buyt.txt', 'source_parts': ['danh_sach_tuyen_buyt.txt', 'lich_trinh_buyt.txt'], 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'domain_aware', 'chunk_index': 122, 'chunk_type': 'bus_route_aggregate', 'route_no': '22C', 'route_no_raw': '22C', 'route_no_norm': '22C'}
- Preview: Tuyến buýt số 22C (tổng hợp theo tuyến) [lich_trinh_buyt.txt] Tuyến buýt số 22C : Bến xe Giáp Bát ⇄ Khu đô thị Dương Nội Bến xe Giáp Bát - Giải Phóng - Kim Đồng - Quay đầu tại điểm mở - Kim Đồng - Giải Phóng - Nguyễn Hữu Thọ - Cầu Dậu - Nghiêm Xuân Yêm - Nguyễn Xiển - Nguyễn Trãi - Trần Phú (Hà Đông) - Quang Trung (Hà Đông) - Chu Văn An (Hà Đông) - Vạn Phúc - Tố Hữu - Đường trục Bắc Hà Đông - Khu đô thị Dương Nội (Ch...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: No
- Top-3 Content Correct?: No
- Đánh giá: Cần tinh chỉnh thêm metadata và hybrid reranking.

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Hard filter: topic=law_education
Soft preferences: {'preferred_terms': ['hoc bong loai kha', 'muc tran hoc phi', 'diem c khoan 1', 'ket qua hoc tap', 'diem ren luyen'], 'article_no': '7', 'topic': 'law_education', 'clause_no': '3'}

Top 1:
- Final score: 2.4954
- Embedding score: 0.2278
- Lexical score: 1.7700
- Metadata bonus: 0.4400
- Completeness bonus: 0.6900
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 22, 'chunk_type': 'legal_clause_point', 'article_no': '7', 'article_title': 'Học bổng khuyến khích học tập', 'clause_no': '3', 'point': 'c'}
- Preview: Điều 7. Học bổng khuyến khích học tập 3. 3. Mức học bổng đối với đối tượng quy định tại điểm c khoản 1 Điều này: a) Học bổng loại Khá: Mức học bổng bằng hoặc cao hơn mức trần học phí hiện hành của ngành, chuyên ngành, nghề mà người học đó phải đóng tại trường do hiệu trưởng hoặc giám đốc quy định (sau đây gọi chung là hiệu trưởng) đối với người học có điểm trung bình chung học tập và điểm rèn luyện đều đạt loại Khá t...

Top 2:
- Final score: 1.4181
- Embedding score: 0.0570
- Lexical score: 1.3433
- Metadata bonus: 0.2600
- Completeness bonus: 0.1000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 17, 'chunk_type': 'legal_clause', 'article_no': '7', 'article_title': 'Học bổng khuyến khích học tập', 'clause_no': '1'}
- Preview: Điều 7. Học bổng khuyến khích học tập 1. Đối tượng xét, cấp học bổng khuyến khích học tập: a) Học sinh trường trung học phổ thông chuyên (sau đây gọi chung là trường chuyên), học sinh trung học phổ thông chuyên trong cơ sở giáo dục đại học có kết quả rèn luyện và kết quả học tập đạt mức cao nhất trong các mức đánh giá kết quả rèn luyện, kết quả học tập của học sinh trung học phổ thông thuộc kỳ xét, cấp học bổng và có...

Top 3:
- Final score: 1.3040
- Embedding score: 0.2241
- Lexical score: 1.2767
- Metadata bonus: 0.2600
- Completeness bonus: 0.0000
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'domain_aware', 'chunk_index': 26, 'chunk_type': 'legal_clause', 'article_no': '7', 'article_title': 'Học bổng khuyến khích học tập', 'clause_no': '6'}
- Preview: Điều 7. Học bổng khuyến khích học tập 6. Việc xét, cấp học bổng đối với đối tượng quy định tại điểm c khoản 1 Điều này: a) Hiệu trưởng căn cứ vào nguồn học bổng khuyến khích học tập xác định số lượng suất học bổng cho từng khóa học, ngành học. Trong trường hợp số lượng người học thuộc diện được xét, cấp học bổng nhiều hơn số suất học bổng thì việc xét, cấp học bổng do hiệu trưởng quyết định; b) Hiệu trưởng căn cứ vào...

Nhận xét:
- Expected file hit in Top-3: Yes
- Top-1 Content Correct?: Yes
- Top-3 Content Correct?: Yes
- Đánh giá: Top-1 chunk đã đủ nội dung để trả lời.

# Summary Table

| Query ID | Strategy | Top-1 Source | Top-1 Score | Top-1 Content Correct? | Top-3 Content Correct? | Expected file hit in Top-3? | Nhận xét |
|---|---|---|---:|---|---|---|---|
| Q1 | fixed_size | danh_sach_tuyen_buyt.txt | 3.0303 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q2 | fixed_size | metro_hanoi.txt | 1.7891 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q3 | fixed_size | quy_dinh_phap_luat.txt | 1.5594 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q4 | fixed_size | lich_trinh_buyt.txt | 1.6066 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q5 | fixed_size | tai_lieu_phap_ly.txt | 0.7534 | No | No | Yes | Cần đẩy mạnh hơn clause 3 Điều 7 hoặc point a của clause 3 lên Top-1. |
| Q1 | sentence | bus_brt_hanoi.txt | 3.1296 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q2 | sentence | metro_hanoi.txt | 1.9636 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q3 | sentence | quy_dinh_phap_luat.txt | 1.6507 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q4 | sentence | lich_trinh_buyt.txt | 1.7161 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q5 | sentence | tai_lieu_phap_ly.txt | 1.4407 | No | No | Yes | Cần đẩy mạnh hơn clause 3 Điều 7 hoặc point a của clause 3 lên Top-1. |
| Q1 | recursive | lich_trinh_buyt.txt | 2.8394 | No | No | Yes | Vẫn cần gom route 7 đầy đủ hơn để một chunk duy nhất chứa lộ trình + giờ + giá. |
| Q2 | recursive | metro_hanoi.txt | 1.9179 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q3 | recursive | quy_dinh_phap_luat.txt | 1.6484 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q4 | recursive | bus_brt_hanoi.txt | 1.4524 | No | No | Yes | Cần tinh chỉnh thêm metadata và hybrid reranking. |
| Q5 | recursive | tai_lieu_phap_ly.txt | 1.1616 | No | No | Yes | Cần đẩy mạnh hơn clause 3 Điều 7 hoặc point a của clause 3 lên Top-1. |
| Q1 | domain_aware | lich_trinh_buyt.txt | 3.9272 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q2 | domain_aware | metro_hanoi.txt | 1.9405 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q3 | domain_aware | quy_dinh_phap_luat.txt | 1.6484 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |
| Q4 | domain_aware | lich_trinh_buyt.txt | 1.4321 | No | No | Yes | Cần tinh chỉnh thêm metadata và hybrid reranking. |
| Q5 | domain_aware | tai_lieu_phap_ly.txt | 2.4954 | Yes | Yes | Yes | Top-1 chunk đã đủ nội dung để trả lời. |

# Comparison With Previous Benchmark

- Trước tối ưu, retrieval thường đúng file nhưng sai chunk, đặc biệt ở Q1, Q4 và Q5.
- Sau tối ưu lần 1, metadata chi tiết hơn, routing và hybrid reranking đã giúp tăng mạnh chất lượng content-level; `domain_aware` đạt khoảng 4/5 Top-1 content đúng.
- Sau tối ưu lần 2, Q1 được cải thiện nhờ chunk tổng hợp theo tuyến buýt; Q5 được cải thiện nhờ tách Điều 7 theo khoản và ưu tiên clause 3 mạnh hơn.
- Điểm khó còn lại thường đến từ dữ liệu gốc không đồng nhất giữa các file hoặc OCR pháp lý dài.
