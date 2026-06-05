# Bao Cao Lab 7: Embedding & Vector Store

**Ho ten:** Hoàng Trọng Vĩnh  
**Nhom:** Bàn D5  
**Ngay:** 05/06/2026

---

## 1. Warm-up (5 diem)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghia la gi?**  
High cosine similarity nghia la hai vector embedding co huong gan nhau trong khong gian vector, tuong ung voi hai doan van ban co noi dung hoac ngu nghia gan nhau. Trong bai lab nay, dieu do thuong co nghia la hai cau dang de cap cung mot doi tuong, mot su kien, hoac mot thong tin tra loi.

**Vi du HIGH similarity:**
- Sentence A: "Metro Cat Linh - Ha Dong co 12 ga."
- Sentence B: "Tuyen 2A Cat Linh - Ha Dong gom 12 nha ga."
- Tai sao tuong dong: Ca hai cau deu noi ve cung mot tuyen metro va cung thong tin chinh la so luong ga.

**Vi du LOW similarity:**
- Sentence A: "Xe buyt so 7 di Noi Bai."
- Sentence B: "Hoc bong khuyen khich hoc tap loai Kha tinh theo hoc phi."
- Tai sao khac: Hai cau thuoc hai chu de khac nhau hoan toan, mot cau ve giao thong cong cong, mot cau ve chinh sach hoc bong.

**Tai sao cosine similarity duoc uu tien hon Euclidean distance cho text embeddings?**  
Cosine similarity tap trung vao huong cua vector nen phu hop hon voi embeddings van ban, vi dieu quan trong thuong la su giong nhau ve nghia chu khong phai do lon tuyet doi cua vector. Euclidean distance de bi anh huong boi do lon vector hon, trong khi cosine similarity on dinh hon khi so sanh cac vector da duoc chuan hoa.

### Chunking Math (Ex 1.2)

**Document 10,000 ky tu, chunk_size=500, overlap=50. Bao nhieu chunks?**  
Trinh bay phep tinh:
- `step = chunk_size - overlap = 500 - 50 = 450`
- `num_chunks = ceil((10000 - 500) / 450) + 1`
- `= ceil(9500 / 450) + 1`
- `= 22 + 1 = 23`

**Dap an:** 23 chunks.

**Neu overlap tang len 100, chunk count thay doi the nao? Tai sao muon overlap nhieu hon?**  
Khi `overlap = 100` thi `step = 400`, so chunk se la `ceil((10000 - 500) / 400) + 1 = ceil(9500 / 400) + 1 = 24 + 1 = 25`. Overlap nhieu hon giup giu lai ngu canh giua hai chunk lien tiep, nhung doi lai so chunk tang len va chi phi retrieval cung tang.

---

## 2. Document Selection — Nhom (10 diem)

### Domain & Ly Do Chon

**Domain:** Giao thong cong cong Ha Noi va quy dinh/phap ly lien quan.

**Tai sao nhom chon domain nay?**  
Bo du lieu nay co nhieu kieu tai lieu khac nhau, gom lich trinh xe buyt, danh sach tuyen, thong tin metro, BRT, quy dinh khi di metro/xe buyt va van ban phap ly giao duc. Nho vay, nhom co the kiem tra retrieval tren nhieu dang cau hoi khac nhau nhu gia ve, gio hoat dong, dinh tuyen, quy dinh cam, va tra cuu noi dung phap ly. Domain nay cung phu hop de thu metadata filter theo `topic` nhu `bus_city`, `metro`, `law_traffic`, va `law_education`.

### Data Inventory

| # | Ten tai lieu | Nguon | So ky tu | Metadata da gan |
|---|--------------|-------|----------|-----------------|
| 1 | `lich_trinh_buyt.txt` | File text noi bo trong `data/` | 82158 | `topic=bus_city`, `category=route_schedule`, `city=hanoi`, `transport_type=bus` |
| 2 | `danh_sach_tuyen_buyt.txt` | File text noi bo trong `data/` | 16825 | `topic=bus_city`, `category=route_schedule`, `city=hanoi`, `transport_type=bus` |
| 3 | `bus_brt_hanoi.txt` | File text noi bo trong `data/` | 4123 | `topic=bus_city`, `category=route_schedule`, `city=hanoi`, `transport_type=bus` |
| 4 | `metro_hanoi.txt` | File text noi bo trong `data/` | 3214 | `topic=metro`, `category=route_schedule`, `city=hanoi`, `transport_type=metro` |
| 5 | `quy_dinh_phap_luat.txt` | File text noi bo trong `data/` | 1405 | `topic=law_traffic`, `category=regulation`, `city=hanoi` |
| 6 | `tai_lieu_phap_ly.txt` | File text noi bo trong `data/` | 57758 | `topic=law_education`, `category=legal_document`, `city=hanoi` |

Ghi chu: khi build knowledge base cho benchmark, script bo qua `benchmark_queries.md` va cac file `.md`/`.txt` khong thuoc bo 6 tai lieu chinh.

### Metadata Schema

| Truong metadata | Kieu | Vi du gia tri | Tai sao huu ich cho retrieval? |
|----------------|------|---------------|-------------------------------|
| `doc_id` | `str` | `lich_trinh_buyt` | Dung de xac dinh tai lieu goc va ho tro xoa theo document trong store |
| `source` | `str` | `metro_hanoi.txt` | Giup truy vet ket qua retrieval ve file nao |
| `topic` | `str` | `metro` | Ho tro metadata filter, giam nhieu giua cac nhom tai lieu khac nhau |
| `category` | `str` | `route_schedule` | Phan biet lich trinh, quy dinh va van ban phap ly |
| `city` | `str` | `hanoi` | Huu ich neu mo rong sang du lieu nhieu tinh/thanh |
| `transport_type` | `str` | `bus` | Tach nho giao thong duong bo voi metro |
| `strategy` | `str` | `fixed_size` | Giup so sanh ket qua giua cac chien luoc chunking |
| `chunk_index` | `int` | `99` | Cho biet vi tri chunk trong tai lieu goc |

---

## 3. Chunking Strategy — Ca nhan chon, nhom so sanh (15 diem)

### Baseline Analysis

Trong Phase 2, toi chay benchmark tren toan bo 6 tai lieu voi 3 chien luoc chunking sau:

| Strategy | Cau hinh | Tong so chunk | Nhan xet ngan |
|---|---|---:|---|
| FixedSizeChunker | `chunk_size=500`, `overlap=50` | 372 | On dinh, so chunk deu, de lam baseline |
| SentenceChunker | `max_sentences_per_chunk=5` | 132 | Giu cau tot hon nhung phu thuoc manh vao cau truc van ban |
| RecursiveChunker | `chunk_size=500` | 405 | Linh hoat hon, co gang ton trong doan/dong/cau |

FixedSizeChunker co Top-1 source dung cho ca 5 query trong bang summary benchmark. SentenceChunker van dat `expected file hit in top-3 = Yes` cho ca 5 query, nhung Q1 bi lech Top-1 sang `tai_lieu_phap_ly.txt` va Q2 co score am du source dung. RecursiveChunker cho ket qua content-level tot nhat o Q3 vi Top-1 chua dung doan "NGHIEM CAM an uong trong tau va tren san ga (phat 100.000-300.000d)", nhung Q1 va Q5 van co Top-1 lech sang tai lieu phap ly.

### Strategy Cua Toi

**Loai:** FixedSizeChunker

**Mo ta cach hoat dong:**  
FixedSizeChunker cat van ban theo cua so co do dai co dinh va cho phep overlap giua hai chunk lien tiep. Trong implementation cua bai lab, moi chunk toi da `chunk_size` ky tu va cac chunk lien ke chia se `overlap` ky tu de giam nguy co mat ngu canh. Chien luoc nay khong can hieu cau truc cau hay doan van, nen don gian, de debug, va cho ket qua on dinh tren nhieu loai tai lieu.

**Tai sao toi chon strategy nay cho domain nhom?**  
Bo du lieu nhom co su pha tron giua lich trinh xe buyt rat dai, tai lieu dang list/bullet, va van ban phap ly OCR khong deu. Trong benchmark thuc te, FixedSizeChunker la baseline on dinh nhat o muc source-level: Top-1 source dung cho ca 5/5 query, cao hon hai chien luoc con lai.

**Code snippet (neu custom):**
```python
# Khong ap dung vi toi su dung FixedSizeChunker built-in
```

### So Sanh: Strategy cua toi vs Baseline

| Strategy | Top-1 source dung? | Top-3 co file mong doi? | Nhan xet retrieval quality |
|---|---:|---:|---|
| FixedSizeChunker | 5/5 | 5/5 | On dinh nhat o source-level, nhung content-level van chua tot o Q2, Q4, Q5 |
| SentenceChunker | 3/5 neu xet Top-1 source | 5/5 | Giu cau tot hon nhung khong hop voi du lieu list/OCR dai |
| RecursiveChunker | 3/5 neu xet Top-1 source | 5/5 | Tot voi quy dinh ngan co cau truc ro, dac biet la Q3 |

### So Sanh Với Thanh Vien Khac

| Thanh vien | Strategy | Retrieval Score (/10) | Diem manh | Diem yeu |
|---|---|---:|---|---|
| Toi | FixedSizeChunker | 8/10 | On dinh, de tai lap, Top-1 source dung 5/5 | Cat ngang cau, co the lech noi dung trong tai lieu dai |
| [Can bo sung] | SentenceChunker | [Can bo sung] | Giu cau va ngu nghia bo cuc tot hon khi tai lieu sach | Kem on dinh voi list dai va van ban OCR |
| [Can bo sung] | RecursiveChunker | [Can bo sung] | Giu cau truc doan/cau tot hon trong mot so truong hop | Van co the lech sang source phap ly dai |

**Strategy nao tot nhat cho domain nay? Tai sao?**  
Neu danh gia o source-level, FixedSizeChunker la lua chon tot nhat trong benchmark nay vi Top-1 source dung ca 5/5 query. Neu danh gia o content-level, RecursiveChunker cho thay tiem nang tot hon voi du lieu co cau truc ro, vi o Q3 chunk Top-1 chua dung thong tin can tra loi. Dieu nay cho thay khong nen chi nhin vao file hit, ma can xem chunk co that su chua cau tra loi hay khong.

---

## 4. My Approach — Ca nhan (10 diem)

Giai thich cach tiep can cua toi khi implement cac phan chinh trong package `src`.

### Chunking Functions

**`SentenceChunker.chunk` — approach:**  
Toi dung regex de tach cau theo cac dau cau pho bien nhu `.`, `!`, `?` va khoang trang/xuong dong theo sau, nhung van giu dau cau trong moi cau. Sau do, toi gom toi da `max_sentences_per_chunk` cau vao mot chunk, `strip()` moi chunk va bo qua chunk rong.

**`RecursiveChunker.chunk` / `_split` — approach:**  
Toi dung danh sach separator `["\n\n", "\n", ". ", " ", ""]` va tach de quy tu separator "tho" den "min". Neu doan hien tai van qua dai, ham tiep tuc tach bang separator tiep theo; neu het separator hoac separator rong thi cat cung theo `chunk_size`. Base case la khi text rong hoac do dai chunk da nho hon hoac bang `chunk_size`.

### EmbeddingStore

**`add_documents` + `search` — approach:**  
Toi luu in-memory moi record duoi dang dictionary gom `id`, `content`, `text`, `metadata`, `document`, va `embedding`. Khi search, store embed query, tinh diem tuong dong bang dot product voi embedding da luu, sap xep giam dan theo score, va tra ve toi da `top_k` ket qua.

**`search_with_filter` + `delete_document` — approach:**  
Voi `search_with_filter`, toi loc theo metadata truoc roi moi chay similarity search tren tap con, cach nay giam nhieu ro hon so voi search xong moi loc. Voi `delete_document`, toi xoa tat ca record co `metadata["doc_id"]` trung voi document can xoa va tra ve `True/False` tuy theo co xoa duoc hay khong.

### KnowledgeBaseAgent

**`answer` — approach:**  
Toi cho agent retrieve top-k chunk tu store, trich xuat noi dung tu `content` hoac `text`, sau do build mot prompt RAG don gian gom context va question. Cuoi cung, agent goi `llm_fn(prompt)` va co fallback de dam bao `answer()` luon tra ve chuoi khong rong ngay ca khi khong retrieve duoc context hoac `llm_fn` tra ve chuoi trang.

### Test Results

```
python -m pytest tests/ -v
42 passed in 0.10s
```

**So tests pass:** 42 / 42

---

## 5. Similarity Predictions — Ca nhan (5 diem)

Actual score duoi day duoc tinh bang `_mock_embed` ket hop `compute_similarity()`, vi `_mock_embed` la embedder mac dinh cua bai lab.

| Pair | Sentence A | Sentence B | Du doan | Actual Score | Dung? |
|------|-----------|-----------|---------|--------------:|-------|
| 1 | Metro Cat Linh - Ha Dong co 12 ga. | Tuyen 2A co tong cong 12 nha ga. | high | -0.2011 | Khong |
| 2 | Xe buyt so 7 di tu Cau Giay den Noi Bai. | Tuyen 07 ket noi Cau Giay voi san bay Noi Bai. | high | -0.0541 | Khong |
| 3 | Khong duoc an uong tren metro. | Hanh khach bi cam an uong trong tau va san ga. | high | 0.1375 | Co |
| 4 | Tuyen 32 di Nhon. | Hoc bong loai Kha can cu muc tran hoc phi. | low | -0.0406 | Co |
| 5 | BRT Kim Ma - Yen Nghia co lan duong rieng. | Danh hieu Tien si danh du khong thay the hoc vi. | low | -0.0514 | Co |

**Ket qua nao bat ngo nhat? Dieu nay noi gi ve cach embeddings bieu dien nghia?**  
Dieu bat ngo nhat la hai cap du doan "high" o pair 1 va pair 2 lai cho score am. Dieu nay cho thay `_mock_embed` chi la backend gia lap de test tinh dung cua pipeline, khong phan anh on dinh quan he ngu nghia thuc su. Neu muon danh gia retrieval nghiem tuc hon, can dung embedding model that thay vi chi dua vao mock embedding.

---

## 6. Results — Ca nhan (10 diem)

Chay 5 benchmark queries cua nhom tren implementation ca nhan trong package `src`.

### Benchmark Queries & Gold Answers (nhom thong nhat)

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | Xe buyt so 7 tu Noi Bai den Cau Giay gia bao nhieu va may gio? | Gia 8.000d, gio hoat dong 05:00-21:35, tuyen Cau Giay - Noi Bai qua Cau Thang Long. |
| 2 | Metro Cat Linh-Ha Dong co bao nhieu ga va chay may gio? | 12 ga, hoat dong 05:30-22:30, gio cao diem 6 phut/chuyen, toan tuyen 23 phut. |
| 3 | Quy dinh ve viec an uong tren metro Ha Noi? | Nghiem cam an uong; muc phat tu 100.000-300.000d trong tau va san ga. |
| 4 | Tu Ben xe Giap Bat den Nhon di tuyen nao? | Tuyen 32: Giap Bat -> Kim Ma -> Cau Giay -> Nhon. |
| 5 | Hoc bong khuyen khich hoc tap loai Kha danh cho sinh vien dai hoc la bao nhieu? | Muc hoc bong >= muc tran hoc phi hien hanh, can cu Dieu 7, Nghi dinh 66/2026. |

### Ket Qua Cua Toi

Toi chon strategy ca nhan la `fixed_size` vi day la strategy on dinh nhat trong bang summary benchmark.

| # | Query | Top-1 Retrieved Chunk (tom tat) | Score | Relevant? | Agent Answer (tom tat) |
|---|-------|--------------------------------|------:|-----------|------------------------|
| 1 | Gia ve va gio tuyen 7 Noi Bai - Cau Giay | `lich_trinh_buyt.txt`, chunk Top-1 nam trong file dung nhung preview chua tap trung dung tuyen 7; Top-3 co `bus_brt_hanoi.txt` noi ve tuyen 07 Noi Bai - My Dinh | 0.3381 | Co o muc source-level, content-level chi dat mot phan | Agent co co hoi tra loi dung neu tong hop tu Top-3, nhung Top-1 don le chua du |
| 2 | Metro Cat Linh - Ha Dong | `metro_hanoi.txt`, Top-1 dung file va co thong tin "12 ga", nhung preview dang nghieng sang tuyen metro khac trong cung file | 0.1627 | Co, nhung can doc them chunk lien quan trong Top-3 de day du | Agent co the tra loi kha dung neu tong hop nhieu chunk |
| 3 | Cam an uong tren metro | `quy_dinh_phap_luat.txt`, Top-1 dung file nhung Top-2 moi chua ro cau "NGHIEM CAM an uong..." | 0.1403 | Co o source-level; content-level tot hon neu xet Top-2 | Agent co the tra loi dung neu nhin qua Top-3, khong chi Top-1 |
| 4 | Tuyen tu Giap Bat den Nhon | `lich_trinh_buyt.txt`, Top-1 dung file nhung preview chua dung tuyen 32 | 0.3646 | Co o source-level, chua du chinh xac o content-level | Agent de bi nham neu chi dua vao Top-1 |
| 5 | Hoc bong loai Kha | `tai_lieu_phap_ly.txt`, Top-1 dung file nhung preview chua roi dung Dieu 7 ve hoc bong | 0.3741 | Co file dung, nhung noi dung trich xuat chua dung trong tam | Agent co the tra loi chua chinh xac neu retrieval khong vao dung dieu khoan |

**Bao nhieu queries tra ve chunk relevant trong top-3?**  
- Theo tieu chi source-level: 5 / 5 vi ca 5 query deu co file mong doi xuat hien trong Top-3.
- Theo tieu chi content-level nghiem ngat: khoang 2 / 5 den 3 / 5. Q3 voi `recursive` la truong hop tot nhat vi chunk Top-1 chua truc tiep cau tra loi. Q4 va Q5 cho thay source dung nhung chunk chua roi dung thong tin can tra loi.

Nhan xet quan trong: trong benchmark retrieval, "Top-3 co file dung" moi chi la dau hieu cho thay he thong tim den dung tai lieu goc. De tra loi tot theo RAG, chunk duoc retrieve con phai chua dung noi dung can dung cho cau hoi, tuc la dung o muc content-level.

---

## 7. What I Learned (5 diem — Demo)

**Dieu hay nhat toi hoc duoc tu thanh vien khac trong nhom:**  
Toi hoc duoc rang metadata filter co tac dung rat ro trong viec giam nhieu, dac biet voi Q2, Q3, Q4, va Q5. Khi thu retrieval tren bo du lieu co nhieu chu de, filter theo `topic` giup thu hep pham vi search va tang kha nang tim ve dung nhom tai lieu.

**Dieu hay nhat toi hoc duoc tu nhom khac (qua demo):**  
[Can bo sung] Toi du kien se bo sung them nhan xet sau khi tong hop demo tren lop. Tuy nhien, bai hoc chung la chunking theo cau truc domain, vi du theo tuyen buyt hoac theo dieu khoan phap ly, thuong huu ich hon cat theo do dai co dinh.

**Neu lam lai, toi se thay doi gi trong data strategy?**  
Neu lam lai, toi se tach tai lieu dai theo cau truc domain thay vi chi chunk theo ky tu, vi du tach `lich_trinh_buyt.txt` theo tung tuyen va `tai_lieu_phap_ly.txt` theo tung dieu/khoan. Toi cung se uu tien embedding that thay cho `_mock_embed`, vi benchmark hien tai cho thay score co luc am hoac cao nhung chunk van chua dung noi dung can tra loi.

---

## Tu Danh Gia

| Tieu chi | Loai | Diem tu danh gia |
|----------|------|-------------------|
| Warm-up | Ca nhan | 5 / 5 |
| Document selection | Nhom | 9 / 10 |
| Chunking strategy | Nhom | 13 / 15 |
| My approach | Ca nhan | 9 / 10 |
| Similarity predictions | Ca nhan | 4 / 5 |
| Results | Ca nhan | 8 / 10 |
| Core implementation (tests) | Ca nhan | 30 / 30 |
| Demo | Nhom | 4 / 5 |
| **Tong diem tho** | | **82 / 90** |
| **Tong quy doi thang 100** | | **91.1 / 100** |

Ghi chu: Tong diem tu danh gia duoc quy doi tu thang 90 sang thang 100 theo cong thuc: diem quy doi = diem dat duoc / diem toi da x 100.
