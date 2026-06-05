# Phase 2 Benchmark Results

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

## Strategy: fixed_size

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Filter: Khong

Top 1:
- Score: 0.3381
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'fixed_size', 'chunk_index': 99}
- Preview: ưng – Phạm Hùng – Đỗ Đức Dục – Miếu Đầm – Cầu vượt Mễ Trì – đường Cường Kiên – KĐT Trung Văn Tuyến buýt số 22B : Khu đô thị Kiến Hưng ⇄ Bến xe Mỹ Đình Khu đô thị Kiến Hưng (Cạnh tòa nhà 19T6) - Đường nội bộ khu giãn dân Mậu Lương - Đường Mậu Lương - Đường Phúc La, Văn Phú (Khu đô thị Xa La) - Phùng Hưng (Hà Đông) - Trần Phú (Hà Đông) - Nguyễn Trãi - Khuất Duy Tiến - Phạm Hùng - quay đầu tại ngã tư...

Top 2:
- Score: 0.3355
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'fixed_size', 'chunk_index': 14}
- Preview: cơ quan nhà nư ớc thì cơ s ở giáo d ục không cần phải cung c ấp các văn b ản trên và ch ỉ cần cung c ấp thông tin đ ể có cơ s ở đối chiếu, khai thác d ữ liệu; đ) Báo cáo đánh giá tác đ ộng của việc chuy ển đổi về nhân s ự, tài chính, tài sản và phương án x ử lý (Mẫu số 02 tại Phụ lục kèm theo Ngh ị định này); e) Trường hợp hồ sơ có tài liệu bằng tiếng nước ngoài thì phải được dịch ra tiếng Việt; b...

Top 3:
- Score: 0.3130
- Source: bus_brt_hanoi.txt
- Metadata: {'doc_id': 'bus_brt_hanoi', 'source': 'bus_brt_hanoi.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'fixed_size', 'chunk_index': 1}
- Preview: I BÀI === TUYẾN 07 (Nội Bài – Bến xe Mỹ Đình): - Lộ trình: Sân bay Nội Bài → QL2 → Cầu Thăng Long → Trần Duy Hưng → Bến xe Mỹ Đình - Giờ: 05:30 – 22:00 | Tần suất: 15–20 phút | Giá: 9.000 đồng - Thời gian: 45–50 phút | Đây là tuyến phổ biến nhất từ Nội Bài TUYẾN 17 (Nội Bài – Long Biên): - Lộ trình: Sân bay Nội Bài → QL5 → Cầu Đuống → Long Biên - Giờ: 05:30 – 22:00 | Tần suất: 20–30 phút | Giá: 9....

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: lich_trinh_buyt.txt, bus_brt_hanoi.txt

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Filter: topic=metro

Top 1:
- Score: 0.1627
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'fixed_size', 'chunk_index': 4}
- Preview: dài: 12,5 km (8,5 km trên cao + 4 km ngầm) - Số ga: 12 ga (8 ga trên cao + 4 ga ngầm) - Đoạn trên cao: Vận hành thương mại từ 08/08/2024 - Đoạn ngầm: Đang thi công, dự kiến hoàn thành cuối 2027 - Website: metrohanoi.vn LỘ TRÌNH 12 GA: [ĐANG KHAI THÁC – 8 ga trên cao] Ga 01 – Nhổn: Huyện Từ Liêm | Điểm đầu, bãi đỗ xe rộng Ga 02 – Minh Khai: Quận Nam Từ Liêm | Khu dân cư Ga 03 – Phú Diễn: Quận Bắc T...

Top 2:
- Score: 0.0649
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'fixed_size', 'chunk_index': 5}
- Preview: ừ Liêm | Gần cầu Diễn Ga 05 – Lê Đức Thọ: Quận Nam Từ Liêm | Trục đường Lê Đức Thọ Ga 06 – Đại học Quốc gia: Quận Cầu Giấy | Gần ĐH Quốc gia Hà Nội Ga 07 – Chùa Hà: Quận Cầu Giấy | Gần chùa Hà (cầu duyên nổi tiếng) Ga 08 – Cầu Giấy: Quận Cầu Giấy | Điểm chuyển tiếp lên/xuống tuyến trên cao [ĐANG XÂY DỰNG – 4 ga ngầm, dự kiến 2027] Ga 09 – Kim Mã (S9): Quận Ba Đình | Gần bến xe Kim Mã, kết nối BRT...

Top 3:
- Score: 0.0415
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'fixed_size', 'chunk_index': 1}
- Preview: át Linh → Hà Đông): Ga 01 – Cát Linh: Quận Đống Đa | Điểm đầu, gần Đại học Kiến trúc, kết nối nhiều tuyến buýt Ga 02 – La Thành: Quận Đống Đa | Gần Văn Miếu Quốc Tử Giám (đi bộ ~800m) Ga 03 – Thái Hà: Quận Đống Đa | Khu thương mại Thái Hà, nhiều quán ăn Ga 04 – Láng: Quận Đống Đa | Gần ĐH Quốc gia Hà Nội, bệnh viện Nhi Ga 05 – Thượng Đình: Quận Thanh Xuân | Khu công nghiệp cao su Thượng Đình Ga 06...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: metro_hanoi.txt

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Filter: topic=law_traffic

Top 1:
- Score: 0.1403
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'fixed_size', 'chunk_index': 3}
- Preview: y): 300.000 – 400.000đ | ô tô: 3.000.000 – 5.000.000đ

Top 2:
- Score: -0.0263
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'fixed_size', 'chunk_index': 1}
- Preview: METRO: - NGHIÊM CẤM ăn uống trong tàu và trên sân ga (phạt 100.000–300.000đ) - Không hút thuốc trong toàn bộ khu vực nhà ga - Không mang xe đạp, xe máy lên tàu (trừ xe đẩy em bé gấp gọn) - Không chụp ảnh tại khu vực vận hành, buồng lái - Không đứng sát cửa, không giữ cửa tàu - Vượt vạch vàng an toàn: có thể bị phạt - Mang theo vé/thẻ hợp lệ khi soát vé LUẬT GIAO THÔNG – NGHỊ ĐỊNH 100/2019/NĐ-CP (M...

Top 3:
- Score: -0.1578
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'fixed_size', 'chunk_index': 2}
- Preview: .200.000đ (xe máy) | 4.000.000 – 6.000.000đ (ô tô) - Vượt đèn đỏ: 4.000.000 – 6.000.000đ (xe máy) | 6.000.000 – 8.000.000đ (ô tô) - Nồng độ cồn 0,25–0,4 mg/l khí thở: 6.000.000 – 8.000.000đ + tước GPLX 10–12 tháng - Nồng độ cồn >0,4 mg/l (xe máy): 30.000.000 – 40.000.000đ + tước GPLX 22–24 tháng - Không đội mũ bảo hiểm: 200.000 – 400.000đ - Dùng điện thoại khi lái xe máy: 800.000 – 1.000.000đ | ô...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: quy_dinh_phap_luat.txt

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Filter: topic=bus_city

Top 1:
- Score: 0.3646
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'fixed_size', 'chunk_index': 123}
- Preview: Hoàng Diệu - Nguyễn Biểu - Quán Thánh - Thụy Khuê - Hoàng Quốc Việt - Phạm Văn Đồng - Đỗ Nhuận - Bãi đỗ xe Nam Thăng Long. Tuyến buýt số 46 : Bến xe Mỹ Đình ⇄ Thị trấn Đông Anh Bến xe Mỹ Đình - Phạm Hùng - quay đầu tại làng Đình Thôn - Phạm Hùng - Phạm Văn Đồng - Cầu Thăng Long - Đường 6 km (Vĩnh Ngọc) - Vân Trì - Đường 5 kéo dài - Đường 6 km (Vĩnh Ngọc) - Quốc lộ 3 - Đường Cổ Loa - Thị trấn Đông...

Top 2:
- Score: 0.2858
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'fixed_size', 'chunk_index': 68}
- Preview: Tuyến xe buýt số 51: Trần Khánh Dư <> Công viên Cầu Giấy Lộ trình: Bãi đỗ xe Trần Khánh Dư <> Nguyễn Khoái <> Lạc Trung <> Thanh Nhàn <> Võ Thị Sáu <> Trần Khát Chân <> Đại Cồ Việt <> Xã Đàn <> Phạm Ngọc Thạch <> Chùa Bộc <> Tây Sơn <> Thái Thịnh <> Láng Hạ <> Quay đầu tại gầm cầu vượt Láng Hạ <> Láng Hạ <> Lê Văn Lương <> Hoàng Đạo Thuý <> Trần Duy Hưng <> Quay đầu tại gần cầu vượt Nguyễn Chí Tha...

Top 3:
- Score: 0.2325
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'fixed_size', 'chunk_index': 151}
- Preview: Xuyên). Tuyến buýt số 92 : Nhổn ⇄ Tây Đằng Nhổn - đường Cầu Diễn - đường Cầu Diễn - Phố Nhổn - Quốc lộ 32 - thị trấn Tây Đằng (Ba Vì) - Đường 411 - Tây Đằng. Tuyến buýt số 93 : Nam Thăng Long ⇄ Bắc Sơn Nam Thăng Long (điểm đỗ xe buýt trên đường đỗ Nhuận, cạnh cổng công viên Hòa Bình) - Đỗ Nhuận - quay đầu tại điểm mở - Đỗ Nhuận - Phạm Văn Đồng - cầu Thăng Long - Võ Văn Kiệt - Quốc lộ 2 - Quốc lộ 3...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: lich_trinh_buyt.txt, danh_sach_tuyen_buyt.txt

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Filter: topic=law_education

Top 1:
- Score: 0.3741
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'fixed_size', 'chunk_index': 29}
- Preview: đồng trường của cơ sở giáo dục nghề nghiệp tư thục (sau đây gọi chung là hội đồng trường tư thục) báo cáo các nhà đầu tư xem xét thông qua tiêu chuẩn, phương án nhân sự hiệu trưởng, phó hiệu trưởng của cơ sở giáo dục tư thục do hội đồng trường tư thục đề xuất đáp ứng thủ tục, quy trình theo quy định tại khoản 2 Điều này và nêu rõ quy trình xác định nhân sự hiệu trưởng, phó hiệu trưởng của cơ sở gi...

Top 2:
- Score: 0.2804
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'fixed_size', 'chunk_index': 89}
- Preview: 5, 6 Điều 35 của Nghị định số 142/2025/NĐ - CP ngày 12 tháng 6 năm 2025 của Chính phủ quy định về phân định thẩm quyền của chính quyền địa phương hai cấp trong lĩnh vực quản lý nhà nước của Bộ Giáo dục và Đào tạo và Điều 6 của Nghị định số 143/2025/NĐ -CP ngày 12 tháng 6 năm 2025 của Chính phủ quy định về phân quyền, phân cấp trong lĩnh vực quản lý nhà nước của Bộ Giáo dục và Đào tạo hết hiệu lực...

Top 3:
- Score: 0.2684
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'fixed_size', 'chunk_index': 91}
- Preview: người học chương trình giáo dục phổ thông trong cơ sở giáo dục công lập; quyết địn h mức hỗ trợ học phí đối với trẻ em mầm non, học sinh phổ thông, người học chương trình giáo dục phổ thông trong cơ sở giáo dục dân lập, tư thục theo thẩm quyền quản lý để áp dụng tại địa phương. Ủy ban nhân dân tỉnh, thành phố quyết định chi tiết danh mục các khoản thu, mức thu và cơ chế quản lý thu, chi đối với dị...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: tai_lieu_phap_ly.txt

## Strategy: sentence

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Filter: Khong

Top 1:
- Score: 0.3176
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'sentence', 'chunk_index': 22}
- Preview: Không phong tặng đối với cá nhân đang bị truy cứu trách nhiệm pháp lý, đang có tranh chấp, khiếu nại nghiêm trọng liên quan đến đạo đức, uy tín khoa học. Trong trường hợp người được phong tặng vi phạm pháp luật của Việt Nam, pháp luật của nước sở tại và các điều ước quốc tế mà Việt Nam là thành viên thì căn cứ thẩm quyền quy định tại điểm b khoản 3 Điều này, người có thẩm quyền xem xét, quyết định...

Top 2:
- Score: 0.3099
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'sentence', 'chunk_index': 49}
- Preview: Xác nhận anh/chị:............................................................................................ Hiện là …. lớp:.................. Khóa:................ Thời gian khóa học:.........

Top 3:
- Score: 0.2854
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'sentence', 'chunk_index': 51}
- Preview: Tuyến xe buýt số 53A: Hoàng Quốc Việt <> Đông Anh Lộ trình: Điểm đỗ xe buýt Hoàng Quốc Việt <> Phạm Văn Đồng <> Cầu Thăng Long <> Bắc Thăng Long Nội Bài <> Đường 6 km (Vĩnh Ngọc) <> Thôn Phương Trạch <> Thôn Vân Nội <> Thôn Vân Trì <> Rẽ phải Quốc lộ 5 kéo dài <> Quay đầu tại điểm mở <> Quốc lộ 5 <> Vân Trì <> Cầu tránh Vân Trì <> Quốc lộ 23 <> Cao Lỗ <> Thị trấn Đông Anh. Thời gian hoạt động: 5:1...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: lich_trinh_buyt.txt, bus_brt_hanoi.txt

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Filter: topic=metro

Top 1:
- Score: -0.0397
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === METRO HÀ NỘI === METRO HÀ NỘI ================================================================================ === B1. TUYẾN 2A: CÁT LINH – HÀ ĐÔNG (ĐANG HOẠT ĐỘNG) === THÔNG TIN CHUNG: - Tên: Đường sắt đô thị Hà Nội tuyến 2A - Chiều dài: 13 km (toàn bộ trên cao) - Số ga: 12 ga - Khai thác chính thức: 06/11/2021 - Đơn vị vận hành: Công ty TNHH MTV Đường sắt Hà Nội (MRB) - Hotline: (024) 7307 0...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: metro_hanoi.txt

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Filter: topic=law_traffic

Top 1:
- Score: 0.1239
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'sentence', 'chunk_index': 0}
- Preview: === QUY ĐỊNH PHÁP LUẬT === QUY ĐỊNH & LUẬT PHÁP ================================================================================ QUY ĐỊNH ĐI XE BUÝT: - Không hút thuốc, không xả rác, giữ trật tự, không ăn uống mạnh - Nhường ghế cho người cao tuổi, khuyết tật, phụ nữ mang thai, trẻ em - Hành lý tay: không quá 20 kg - Không mang chất dễ cháy, nổ, chất độc, vật sắc nhọn nguy hiểm - Thanh toán tiền mặ...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: quy_dinh_phap_luat.txt

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Filter: topic=bus_city

Top 1:
- Score: 0.2142
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'sentence', 'chunk_index': 49}
- Preview: Giá vé: 7.000 VNĐ. Tần suất: 10 – 20 phút/chuyến. Tuyến xe buýt số 52A: Công viên Thống Nhất <> Lệ Chi Lộ trình: Công viên Thống Nhất <> Trần Nhân Tông <> Bà Triệu <> Lê Đại Hành <> Bạch Mai <> Minh Khai <> Cầu Mai Động <> Minh Khai <> Cầu Vĩnh Tuy <> Đường dẫn cầu Vĩnh Tuy <> Nguyễn Văn Linh <> Nguyễn Đức Thuận <> Cầu vượt Phú Thuỵ <> Ỷ Lan <> Dương Xá <> Ngã tư Sủi <> Đường 181 <> Phú Thị <> Keo...

Top 2:
- Score: 0.2018
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'sentence', 'chunk_index': 9}
- Preview: Giá vé: 7.000 VNĐ. Tần suất: 13 – 30 phút/chuyến. Tuyến xe buýt số 10B: Khu đô thị Times City <> Trung Mầu Lộ trình: Bệnh viện VinMec <> Minh Khai <> Nguyễn Khoái <> Trần Khánh Dư <> Trần Quang Khải <> Yên Phụ <> Quay đầu tại 92 Yên Phụ <> Điểm trung chuyển Long Biên <> Trần Nhật Duật <> Cầu Chương Dương <> Nguyễn Văn Cừ <> Ngô Gia Tự <> Cầu Đuống <> Hà Huy Tập <> Quốc lộ 1A <> Dốc Lã <> Trường Yê...

Top 3:
- Score: 0.1962
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'sentence', 'chunk_index': 26}
- Preview: Tần suất: 10 – 20 phút/chuyến. Tuyến xe buýt số 16: Mai Động <> Sân vận động Mỹ Đình Lộ trình: Mai Động (Đường vào Xí nghiệp buýt Thăng Long cũ) <> Nguyễn Tam Trinh <> Cầu Mai Động <> Kim Ngưu <> Thanh Nhàn <> Lê Thanh Nghị <> Giải Phóng <> Xã Đàn <> Phạm Ngọc Thạch <> Chùa Bộc <> Thái Hà <> Huỳnh Thúc Kháng <> Nguyễn Chí Thanh <> Đe La Thành <> Cầu Giấy <> Điểm trung chuyển Cầu Giấy <> Cầu Giấy <...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: lich_trinh_buyt.txt, danh_sach_tuyen_buyt.txt

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Filter: topic=law_education

Top 1:
- Score: 0.2663
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'sentence', 'chunk_index': 23}
- Preview: 2. Điều kiện được phong tặng: a) Đáp ứng các điều kiện quy định tại khoản 2 Điều 9 của Nghị định này; b) Có bằng tiến sĩ. 3. Quy trình phong tặng thực hiện theo quy định tại khoản 3 Điều 9 của Nghị định này. 4.

Top 2:
- Score: 0.2057
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'sentence', 'chunk_index': 42}
- Preview: (3) Người/cơ quan có thẩm quyền quyết định chuyển đổi. (4) Quyền hạn, chức vụ của người đứng đầu cơ quan, tổ chức, cá nhân đề nghị chuyển đổi. CÔNG BÁO/S ố 155/Ngày 22 -03-2026 26 Mẫu số 03 ….(1)…… ________ CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc _____________________________________ Số:……./QĐ -……. …., ngày …. tháng ...

Top 3:
- Score: 0.1836
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'sentence', 'chunk_index': 58}
- Preview: (7) Tên đơn vị được giao nhiệm vụ. (8) Hiệu lực thi hành của quyết định. (9) Trách nhiệm tổ chức thực hiện quyết định. CÔNG BÁO/S ố 155/Ngày 22 -03-2026 31 Phụ lục DANH SÁCH NGƯỜI HỌC HƯỞNG HỌC BỔNG CHÍNH SÁCH (Kèm theo Quyết định số:……/QĐ -……. ngày … tháng … năm … của….) Đơn vị tính: đồng TT Nội dung Ngày tháng năm sinh Loại đối tượng chính sách Dân tộc Cơ sở giáo dục đang theo học Số tháng hỗ tr...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: tai_lieu_phap_ly.txt

## Strategy: recursive

### Q1
Question: Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?
Gold Answer: Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.
Filter: Khong

Top 1:
- Score: 0.3307
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'recursive', 'chunk_index': 19}
- Preview: Điều 5. Chuyển đổi cơ sở giáo dục nghề nghiệp tư thục sang cơ sở giáo dục nghề nghiệp tư thục hoạt động không vì lợi nhuận 1. Hồ sơ chuyển đổi bao gồm: a) Tờ trình đề nghị chuyển đổi ( Mẫu số 01 tại Phụ lục kèm theo Nghị định này); b) Văn bản cam kết của các nhà đầu tư đại diện ít nhất 75% tổng số vốn góp đối với cơ sở giáo dục nghề nghiệp tư thục chuyển sang cơ sở giáo dục nghề nghiệp tư thục hoạ...

Top 2:
- Score: 0.3241
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'recursive', 'chunk_index': 165}
- Preview: Tuyến buýt số 56B : Học viện Phật Giáo ⇄ Học viện Phật Giáo Học viện Phật Giáo VN - đường vào đền Sóc - QL3 - Tỉnh lộ 131 - đường Núi Đôi - Tỉnh lộ 131 (đi qua các xã Đan Tảo, Xuân Giang, Tiên Tảo, Việt Long, Đồng Xoài, Lương Phú) - Đê Lương Phúc - Thôn Ngô Đạo - Ngã ba Tân Thành - Tỉnh lộ 296 - Bắc Phú - Tân Minh - Núi Đôi - đường Núi Đôi - Tỉnh lộ 131 - QL3 - Sóc Sơn - đường vào đền Sóc - Học vi...

Top 3:
- Score: 0.3124
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'recursive', 'chunk_index': 114}
- Preview: vụ, quyền hạn của cơ quan, tổ chức ban hành quyết định; các văn bản pháp lý liên quan trực tiếp đến vấn đề giải quyết trong nội dung quyết định; quyết định giao dự toán chi ngân sách trong năm đã được cấp có th ẩm quyền giao). (6) Ghi rõ đối tượng được hưởng học bổng chính sách (sinh viên theo chế độ cử tuyển; học sinh trường dự bị đại học, trường phổ thông dân tộc nội trú; học viên là thương binh...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: lich_trinh_buyt.txt, bus_brt_hanoi.txt

### Q2
Question: Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?
Gold Answer: 12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.
Filter: topic=metro

Top 1:
- Score: 0.1056
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'recursive', 'chunk_index': 8}
- Preview: GIỜ HOẠT ĐỘNG (Đoạn trên cao Nhổn – Cầu Giấy): - 05:30 – 22:00 hàng ngày - Cao điểm: theo biểu đồ thực tế - Thấp điểm & cuối tuần: 10 phút/chuyến - Tối (19:30–22:00): 15 phút/chuyến - Từ 01/02/2026: 100% soát vé điện tử sinh trắc học GIÁ VÉ METRO NHỔN – CẦU GIẤY: - Tương đương tuyến 2A: 8.000–15.000 đồng tùy số ga - Vé ngày: 30.000 đồng

Top 2:
- Score: 0.0379
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'recursive', 'chunk_index': 6}
- Preview: Ga 08 – Cầu Giấy: Quận Cầu Giấy | Điểm chuyển tiếp lên/xuống tuyến trên cao

Top 3:
- Score: 0.0274
- Source: metro_hanoi.txt
- Metadata: {'doc_id': 'metro_hanoi', 'source': 'metro_hanoi.txt', 'topic': 'metro', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'metro', 'strategy': 'recursive', 'chunk_index': 7}
- Preview: [ĐANG XÂY DỰNG – 4 ga ngầm, dự kiến 2027] Ga 09 – Kim Mã (S9): Quận Ba Đình | Gần bến xe Kim Mã, kết nối BRT Ga 10 – Cát Linh (S10): Quận Đống Đa | Kết nối tuyến 2A (Cát Linh – Hà Đông) Ga 11 – Văn Miếu (S11): Quận Đống Đa | Gần Văn Miếu Quốc Tử Giám Ga 12 – Ga Hà Nội (S12): Quận Hoàn Kiếm | Kết nối ga đường sắt quốc gia Hà Nội

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: metro_hanoi.txt

### Q3
Question: Quy định về việc ăn uống trên metro Hà Nội?
Gold Answer: Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.
Filter: topic=law_traffic

Top 1:
- Score: 0.1111
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'recursive', 'chunk_index': 1}
- Preview: QUY ĐỊNH ĐI METRO: - NGHIÊM CẤM ăn uống trong tàu và trên sân ga (phạt 100.000–300.000đ) - Không hút thuốc trong toàn bộ khu vực nhà ga - Không mang xe đạp, xe máy lên tàu (trừ xe đẩy em bé gấp gọn) - Không chụp ảnh tại khu vực vận hành, buồng lái - Không đứng sát cửa, không giữ cửa tàu - Vượt vạch vàng an toàn: có thể bị phạt - Mang theo vé/thẻ hợp lệ khi soát vé

Top 2:
- Score: 0.0102
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'recursive', 'chunk_index': 3}
- Preview: - Dùng điện thoại khi lái xe máy: 800.000 – 1.000.000đ | ô tô: 1.000.000 – 2.000.000đ - Đi ngược chiều (xe máy): 300.000 – 400.000đ | ô tô: 3.000.000 – 5.000.000đ

Top 3:
- Score: -0.0188
- Source: quy_dinh_phap_luat.txt
- Metadata: {'doc_id': 'quy_dinh_phap_luat', 'source': 'quy_dinh_phap_luat.txt', 'topic': 'law_traffic', 'category': 'regulation', 'city': 'hanoi', 'strategy': 'recursive', 'chunk_index': 0}
- Preview: === QUY ĐỊNH PHÁP LUẬT === QUY ĐỊNH & LUẬT PHÁP ================================================================================ QUY ĐỊNH ĐI XE BUÝT: - Không hút thuốc, không xả rác, giữ trật tự, không ăn uống mạnh - Nhường ghế cho người cao tuổi, khuyết tật, phụ nữ mang thai, trẻ em - Hành lý tay: không quá 20 kg - Không mang chất dễ cháy, nổ, chất độc, vật sắc nhọn nguy hiểm - Thanh toán tiền mặ...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: quy_dinh_phap_luat.txt

### Q4
Question: Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?
Gold Answer: Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.
Filter: topic=bus_city

Top 1:
- Score: 0.2872
- Source: danh_sach_tuyen_buyt.txt
- Metadata: {'doc_id': 'danh_sach_tuyen_buyt', 'source': 'danh_sach_tuyen_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'recursive', 'chunk_index': 18}
- Preview: - Mã số: 85 | Tuyến xe buýt: CV Nghĩa Đô – KĐT Văn Phú | Thời gian hoạt động: 5:00 - 21:00 | Giá vé tham khảo: 10.000 VNĐ - Mã số: 86 | Tuyến xe buýt: Ga Hà Nội – SB Nội Bài | Thời gian hoạt động: 5:05 - 21:40 | Giá vé tham khảo: 35.000 VNĐ - Mã số: 88 | Tuyến xe buýt: BX.Mỹ Đình – Xuân Mai | Thời gian hoạt động: 5:05 - 18:30 | Giá vé tham khảo: 20.000 VNĐ - Mã số: 89 | Tuyến xe buýt: BX.Yên Ngh...

Top 2:
- Score: 0.2723
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'recursive', 'chunk_index': 166}
- Preview: Nam Thăng Long (BĐX Nam Thăng Long) - Phạm Văn Đồng - Tân Xuân - Chân Cầu Thăng Long - Hoàng Tăng Bí - Cầu Liên Mạc 2 - Tân Phong - Yên Nội - Văn Tiến Dũng - Quốc lộ 32 - Nhổn(điểm trung chuyển xe buýt Nhổn) - Quốc lộ 32 - Ngã tư Nhổn - Tỉnh lộ 70 - Xuân Phương - Tây Mỗ - Đại Mỗ - Vạn Phúc - Ngã tư bưu điện Hà Đông - Quang Trung (Hà Đông) – Ba La – Quốc Lộ 6 – Yên Nghĩa - Đồng Mai – Cầu Mai Lĩnh –...

Top 3:
- Score: 0.2695
- Source: lich_trinh_buyt.txt
- Metadata: {'doc_id': 'lich_trinh_buyt', 'source': 'lich_trinh_buyt.txt', 'topic': 'bus_city', 'category': 'route_schedule', 'city': 'hanoi', 'transport_type': 'bus', 'strategy': 'recursive', 'chunk_index': 78}
- Preview: Lộ trình: Điểm trung chuyển Long Biên <> Yên Phụ <> Trần Nhật Duật <> Cầu Chương Dương <> Đê Long Biên <> Bồ Đề <> Tư Đình <> Cự Khối <> Đông Dư <> Qua ngã ba đi Bát Tràng <> Đường liên xã Kim Lan <> Bãi đỗ xe Kim Lan. Thời gian hoạt động: 5:14 – 19:42. Giá vé: 7.000 VNĐ. Tần suất: 28 – 33 phút/chuyến. Tuyến xe buýt số 48: Trần Khánh Dư <> Vạn Phúc

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: lich_trinh_buyt.txt, danh_sach_tuyen_buyt.txt

### Q5
Question: Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?
Gold Answer: Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.
Filter: topic=law_education

Top 1:
- Score: 0.2696
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'recursive', 'chunk_index': 3}
- Preview: thục sang nhà trẻ, trường mẫu giáo, trường mầm non tư thục hoạt động không vì lợi nhuận 1. Hồ sơ chuyển đổi bao gồm: a) Tờ trình đề nghị chuyển đổi sang nhà trẻ, trường mẫu giáo, trường mầm non tư thục hoạt động không vì lợi nhuận (Mẫu số 01 tại Phụ lục kèm theo Nghị định này); b) Văn bản cam kết của các nhà đầu tư đại diện ít nhất 75% tổng số vốn góp đối với nhà trẻ, trường mẫu giáo, trường mầm n...

Top 2:
- Score: 0.2451
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'recursive', 'chunk_index': 30}
- Preview: trưởng được kéo dài thời gian thực hiện nhiệm vụ cho đến khi hội đồng trường tư thục quyết định bổ nhiệm hiệu trư ởng của cơ sở giáo dục nghề nghiệp tư thục của nhiệm kỳ kế tiếp, trên cơ sở đề nghị của hội đồng trường tư thục nhiệm kỳ kế tiếp. 4. Thủ tục, quy trình bổ nhiệm cán bộ quản lý cơ sở giáo dục thành lập theo Hiệp định giữa Chính phủ Việt Nam với Chính phủ nước ngoài thực hiện theo Hiệp đ...

Top 3:
- Score: 0.2313
- Source: tai_lieu_phap_ly.txt
- Metadata: {'doc_id': 'tai_lieu_phap_ly', 'source': 'tai_lieu_phap_ly.txt', 'topic': 'law_education', 'category': 'legal_document', 'city': 'hanoi', 'strategy': 'recursive', 'chunk_index': 118}
- Preview: trường như sau: 1. Danh sách nhà đầu tư chuyển nhượng vốn STT Tên tổ chức, các nhân Số vốn chuyển nhượng (VNĐ/USD) 1 2 … 2. Danh sách nhà đầu tư nhận chuyển nhượng vốn STT Tên tổ chức, các nhân Số vốn nhận chuyển nhượng (VNĐ/USD) 1 2 … 3. Danh sách nhà đầu tư sau khi hoàn thành chuyển nhượng vốn tại thời điểm ngày … tháng… năm….. STT Tên tổ chức, các nhân Số vốn góp (VNĐ/USD) Tỷ lệ góp vốn (%) 1 2...

Nhan xet:
- Expected file hit in Top-3: Yes
- Expected files: tai_lieu_phap_ly.txt

# Summary Table

| Query ID | Strategy | Top-1 Source | Top-1 Score | Expected file hit in Top-3? | Nhan xet |
|---|---|---|---:|---|---|
| Q1 | fixed_size | lich_trinh_buyt.txt | 0.3381 | Yes | Matched expected source |
| Q2 | fixed_size | metro_hanoi.txt | 0.1627 | Yes | Matched expected source |
| Q3 | fixed_size | quy_dinh_phap_luat.txt | 0.1403 | Yes | Matched expected source |
| Q4 | fixed_size | lich_trinh_buyt.txt | 0.3646 | Yes | Matched expected source |
| Q5 | fixed_size | tai_lieu_phap_ly.txt | 0.3741 | Yes | Matched expected source |
| Q1 | sentence | tai_lieu_phap_ly.txt | 0.3176 | Yes | Matched expected source |
| Q2 | sentence | metro_hanoi.txt | -0.0397 | Yes | Matched expected source |
| Q3 | sentence | quy_dinh_phap_luat.txt | 0.1239 | Yes | Matched expected source |
| Q4 | sentence | lich_trinh_buyt.txt | 0.2142 | Yes | Matched expected source |
| Q5 | sentence | tai_lieu_phap_ly.txt | 0.2663 | Yes | Matched expected source |
| Q1 | recursive | tai_lieu_phap_ly.txt | 0.3307 | Yes | Matched expected source |
| Q2 | recursive | metro_hanoi.txt | 0.1056 | Yes | Matched expected source |
| Q3 | recursive | quy_dinh_phap_luat.txt | 0.1111 | Yes | Matched expected source |
| Q4 | recursive | danh_sach_tuyen_buyt.txt | 0.2872 | Yes | Matched expected source |
| Q5 | recursive | tai_lieu_phap_ly.txt | 0.2696 | Yes | Matched expected source |
