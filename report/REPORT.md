# Bao Cao Lab 7: Embedding & Vector Store

**Ho ten:** [Đỗ Đức TUệ]  
**Nhom:** [D5]  
**Ngay:** 05/06/2026

---

## 1. Warm-up

### Cosine Similarity

**High cosine similarity nghia la gi?**  
High cosine similarity nghia la hai vector co huong gan nhau, nen hai van ban duoc xem la gan nhau ve mat bieu dien embedding. Trong retrieval, score cao thuong cho thay chunk co kha nang lien quan hon voi query.

**Vi du HIGH similarity:**

- Sentence A: Xe buyt so 7 di tu Cau Giay den Noi Bai.
- Sentence B: Tuyen 7 ket noi Cau Giay voi san bay Noi Bai.
- Tai sao tuong dong: Hai cau cung noi ve tuyen xe buyt so 7 va diem den Noi Bai.

**Vi du LOW similarity:**

- Sentence A: Metro Cat Linh - Ha Dong co 12 ga.
- Sentence B: Hoc bong sinh vien loai Kha duoc tinh theo hoc phi.
- Tai sao khac: Hai cau thuoc hai domain khac nhau, mot cau ve metro va mot cau ve hoc bong.

**Tai sao cosine similarity duoc uu tien hon Euclidean distance cho text embeddings?**  
Cosine similarity tap trung vao huong cua vector, phu hop khi so sanh y nghia van ban. Euclidean distance bi anh huong nhieu boi do lon vector, trong khi text embedding thuong can so sanh muc do gan nhau ve ngu nghia.

### Chunking Math

**Document 10,000 ky tu, chunk_size=500, overlap=50. Bao nhieu chunks?**  
Step = 500 - 50 = 450.  
So chunks = ceil((10000 - 500) / 450) + 1 = ceil(9500 / 450) + 1 = 23 chunks.

**Neu overlap tang len 100, chunk count thay doi the nao?**  
Step = 500 - 100 = 400. So chunks = ceil((10000 - 500) / 400) + 1 = 25 chunks. Overlap lon hon lam tang so chunk, nhung giup giu ngu canh giua hai chunk lien tiep.

---

## 2. Document Selection - Nhom

### Domain & Ly Do Chon

**Domain:** He thong tra cuu giao thong cong cong Ha Noi, mo rong them mot phan phap ly giao thong va phap ly giao duc.

Nhom chon domain nay vi du lieu co nhieu thong tin cu the ve tuyen xe buyt, metro, BRT, gia ve, lich trinh va quy dinh. Day la domain phu hop de kiem tra retrieval vi nguoi dung thuong hoi cac cau hoi rat cu the, vi du tuyen nao, gia bao nhieu, gio hoat dong nao, hoac quy dinh nao ap dung.

### Data Inventory

| # | Ten tai lieu | Nguon | So ky tu | Metadata da gan |
|---|---|---|---:|---|
| 1 | `lich_trinh_buyt.txt` | `data/` | 105527 | `source`, `topic=bus_city`, `chunk_index`, `strategy` |
| 2 | `bus_brt_hanoi.txt` | `data/` | 5238 | `source`, `topic=bus_city`, `chunk_index`, `strategy` |
| 3 | `metro_hanoi.txt` | `data/` | 4128 | `source`, `topic=metro`, `chunk_index`, `strategy` |
| 4 | `quy_dinh_phap_luat.txt` | `data/` | 1758 | `source`, `topic=law_traffic`, `chunk_index`, `strategy` |
| 5 | `tai_lieu_phap_ly.txt` | `data/` | 77755 | `source`, `topic=law_education`, `chunk_index`, `strategy` |

### Metadata Schema

| Truong metadata | Kieu | Vi du gia tri | Tai sao huu ich cho retrieval? |
|---|---|---|---|
| `source` | string | `metro_hanoi.txt` | Biet ket qua lay tu file nao |
| `topic` | string | `metro` | Loc theo domain nhu metro, xe buyt, phap ly |
| `chunk_index` | int | `9` | Biet vi tri chunk trong tai lieu goc |
| `strategy` | string | `recursive_300` | Ghi lai chien luoc chunking khi benchmark |

---

## 3. Chunking Strategy - Ca Nhan Chon, Nhom So Sanh

### Baseline Analysis

Chay `ChunkingStrategyComparator().compare()` voi `chunk_size=300`.

| Tai lieu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|---|---|---:|---:|---|
| `bus_brt_hanoi.txt` | FixedSizeChunker | 14 | 294.5 | Medium |
| `bus_brt_hanoi.txt` | SentenceChunker | 5 | 823.8 | High but chunks too long |
| `bus_brt_hanoi.txt` | RecursiveChunker | 21 | 194.6 | High |
| `metro_hanoi.txt` | FixedSizeChunker | 11 | 292.2 | Medium |
| `metro_hanoi.txt` | SentenceChunker | 1 | 3212.0 | Too large |
| `metro_hanoi.txt` | RecursiveChunker | 16 | 199.2 | High |
| `quy_dinh_phap_luat.txt` | FixedSizeChunker | 5 | 281.0 | Medium |
| `quy_dinh_phap_luat.txt` | SentenceChunker | 1 | 1403.0 | Too large |
| `quy_dinh_phap_luat.txt` | RecursiveChunker | 8 | 174.1 | High |

### Strategy Cua Toi

**Loai:** `RecursiveChunker(chunk_size=300)`

**Mo ta cach hoat dong:**  
Strategy nay tach van ban theo thu tu uu tien: doan van, dong, cau, tu, roi cuoi cung moi cat cung theo kich thuoc. Neu mot doan ngan hon `chunk_size` thi giu nguyen. Neu doan qua dai thi tiep tuc chia bang separator nho hon.

**Tai sao toi chon strategy nay cho domain nhom?**  
Du lieu giao thong cong cong co cau truc theo tung tuyen, tung muc gia ve va tung quy dinh. `RecursiveChunker` giup giu cac thong tin lien quan trong cung mot chunk tot hon so voi cat cung theo so ky tu.

### So Sanh: Strategy Cua Toi vs Baseline

| Tai lieu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|---|---|---:|---:|---|
| `metro_hanoi.txt` | FixedSize baseline | 11 | 292.2 | Co the cat ngang muc thong tin |
| `metro_hanoi.txt` | **Recursive 300 cua toi** | 16 | 199.2 | Chunk ngan hon, giu cau truc tot hon |
| `quy_dinh_phap_luat.txt` | FixedSize baseline | 5 | 281.0 | Co the tron nhieu quy dinh |
| `quy_dinh_phap_luat.txt` | **Recursive 300 cua toi** | 8 | 174.1 | De loc va doc hon |

### So Sanh Voi Thanh Vien Khac

| Thanh vien | Strategy | Retrieval Score (/10) | Diem manh | Diem yeu |
|---|---|---:|---|---|
| Toi | RecursiveChunker 300 | 7 | Giu cau truc tuyen/muc tot, phu hop metadata filter | Ket qua van phu thuoc embedding |
| Ban A | FixedSize 300 overlap 50 | 6 | De cai dat, chunk deu kich thuoc | Co the cat ngang thong tin tuyen |
| Ban B | SentenceChunker 2 | 6 | Chunk de doc neu cau ngan | Voi file dai it dau cau, chunk co the qua lon |

**Strategy nao tot nhat cho domain nay? Tai sao?**  
`RecursiveChunker` phu hop nhat voi domain nay vi tai lieu co cau truc muc ro rang. No giu duoc ngu canh cua tuyen xe, gia ve va quy dinh, trong khi van tao chunk du ngan de search.

---

## 4. My Approach - Ca Nhan

### Chunking Functions

**`SentenceChunker.chunk` - approach:**  
Ham dung regex `(?<=[.!?])\s+` de tach cau sau dau `.`, `!`, `?`. Sau do gom moi `max_sentences_per_chunk` cau thanh mot chunk va bo khoang trang thua.

**`RecursiveChunker.chunk` / `_split` - approach:**  
Ham co base case la text ngan hon `chunk_size` thi tra ve luon. Neu text qua dai, ham thu tach bang separator hien tai; phan nao van qua dai se de quy tiep voi separator nho hon.

### EmbeddingStore

**`add_documents` + `search` - approach:**  
Moi document duoc chuyen thanh record gom `id`, `content`, `metadata` va `embedding`. Khi search, query cung duoc embed roi tinh dot product voi tung record, sap xep score giam dan va tra ve top-k.

**`search_with_filter` + `delete_document` - approach:**  
`search_with_filter` loc metadata truoc, sau do moi search trong tap ung vien da loc. `delete_document` xoa tat ca record co `metadata["doc_id"]` trung voi doc id can xoa.

### KnowledgeBaseAgent

**`answer` - approach:**  
Agent goi `store.search(question, top_k)`, ghep content cua cac chunk thanh context, sau do tao prompt gom context, question va answer marker. Cuoi cung prompt duoc dua vao `llm_fn`.

### Test Results

```text
============================= 42 passed in 0.08s =============================
```

**So tests pass:** 42 / 42

---

## 5. Similarity Predictions - Ca Nhan

Vi benchmark dang dung `MockEmbedder`, diem actual khong phan anh ngu nghia that su ma phan anh vector gia lap.

| Pair | Sentence A | Sentence B | Du doan | Actual Score | Dung? |
|---|---|---|---|---:|---|
| 1 | Xe buyt so 7 di Noi Bai | Tuyen 7 di Cau Giay den Noi Bai | high | 0.041 | No |
| 2 | Metro Cat Linh Ha Dong co 12 ga | Hoc bong sinh vien loai Kha | low | -0.085 | Yes |
| 3 | Nghiem cam an uong tren metro | Quy dinh khong an uong trong tau | high | 0.076 | No |
| 4 | Ben xe Giap Bat den Nhon | Gia ve metro Cat Linh Ha Dong | low | -0.093 | Yes |
| 5 | Hoc bong loai Kha | Muc hoc bong bang hoac cao hon muc tran hoc phi | high | 0.088 | No |

**Ket qua nao bat ngo nhat?**  
Nhung cap cau co nghia gan nhau lai co score rat thap vi `MockEmbedder` khong hieu ngu nghia tieng Viet. Dieu nay cho thay embedding backend anh huong lon den chat luong retrieval; pipeline dung chua du, vector phai co y nghia.

---

## 6. Results - Ca Nhan

### Benchmark Queries & Gold Answers

| # | Query | Gold Answer |
|---|---|---|
| 1 | Xe buyt so 7 tu Noi Bai den Cau Giay gia bao nhieu va may gio? | Gia 8.000d, gio hoat dong 05:00-21:35, tuyen Cau Giay - Noi Bai qua cau Thang Long. |
| 2 | Metro Cat Linh - Ha Dong co bao nhieu ga va chay may gio? | 12 ga, hoat dong 05:30-22:30, gio cao diem 6 phut/chuyen, toan tuyen 23 phut. |
| 3 | Quy dinh ve viec an uong tren metro Ha Noi? | Nghiem cam an uong; muc phat tu 100.000-300.000d trong tau va san ga. |
| 4 | Tu Ben xe Giap Bat den Nhon di tuyen nao? | Tuyen 32: Giap Bat -> Kim Ma -> Cau Giay -> Nhon. |
| 5 | Hoc bong khuyen khich hoc tap loai Kha danh cho sinh vien dai hoc la bao nhieu? | Muc hoc bong bang hoac cao hon muc tran hoc phi hien hanh cua nganh. |

### Ket Qua Cua Toi

Script chay: `python group_benchmark.py`  
Tong chunks da load: 776  
Strategy: `RecursiveChunker(chunk_size=300)`

| # | Query | Top-1 Retrieved Chunk | Score | Relevant? | Agent Answer tom tat |
|---|---|---|---:|---|---|
| 1 | Xe buyt so 7 tu Noi Bai den Cau Giay gia bao nhieu va may gio? | `lich_trinh_buyt.txt`, chunk 111 | 0.406 | Partly | Co nhac Cau Giay nhung chua dung ro tuyen 7/gia/gio. |
| 2 | Metro Cat Linh - Ha Dong co bao nhieu ga va chay may gio? | `metro_hanoi.txt`, chunk 15 | 0.341 | Partly | Dung domain metro nhung top-1 la gia ve Nhon - Cau Giay. |
| 3 | Quy dinh ve viec an uong tren metro Ha Noi? | `quy_dinh_phap_luat.txt`, chunk 0 | 0.195 | Partly | Dung file phap luat, nhung top-1 la tieu de chung. |
| 4 | Tu Ben xe Giap Bat den Nhon di tuyen nao? | `lich_trinh_buyt.txt`, chunk 263 | 0.434 | No | Top-1 tra tuyen 30, chua dung tuyen 32. |
| 5 | Hoc bong khuyen khich hoc tap loai Kha danh cho sinh vien dai hoc la bao nhieu? | `tai_lieu_phap_ly.txt`, chunk 98 | 0.310 | Partly | Dung domain phap ly giao duc nhung chua dung chunk chua dap an. |

**Bao nhieu queries tra ve chunk relevant trong top-3?**  
Khoang 2 / 5 neu tinh dung domain; 0-1 / 5 neu yeu cau chunk chua dung dap an chi tiet.

**Nhan xet:**  
Metadata filter giup giam ket qua lac domain, dac biet voi Q2, Q3 va Q5. Tuy nhien, do dang dung `MockEmbedder`, retrieval chua hieu ngu nghia nen nhieu ket qua dung file nhung sai chunk. Neu dung `LocalEmbedder` hoac `OpenAIEmbedder`, chat luong search du kien se tot hon.

---

## 7. What I Learned

**Dieu hay nhat toi hoc duoc tu thanh vien khac trong nhom:**  
Toi hoc duoc rang cung mot bo tai lieu nhung cach chunking khac nhau co the tao ra ket qua retrieval rat khac. Strategy qua don gian co the lam mat ngu canh, trong khi strategy qua lon lai lam chunk kho search dung diem.

**Dieu hay nhat toi hoc duoc tu nhom khac qua demo:**  
Mot he thong RAG tot khong chi can code chay dung ma con can data sach, metadata hop ly va embedding phu hop ngon ngu/domain. Filter co the cai thien precision neu metadata duoc thiet ke tot.

**Neu lam lai, toi se thay doi gi trong data strategy?**  
Toi se tach cac file dai nhu `lich_trinh_buyt.txt` va `tai_lieu_phap_ly.txt` thanh cac muc nho hon theo tuyen/dieu khoan truoc khi chunk. Toi cung se thu embedding that cho tieng Viet de so sanh voi `MockEmbedder`.

---

## Tu Danh Gia

| Tieu chi | Loai | Diem tu danh gia |
|---|---|---:|
| Warm-up | Ca nhan | 5 / 5 |
| Document selection | Nhom | 9 / 10 |
| Chunking strategy | Nhom | 13 / 15 |
| My approach | Ca nhan | 10 / 10 |
| Similarity predictions | Ca nhan | 4 / 5 |
| Results | Ca nhan | 8 / 10 |
| Core implementation (tests) | Ca nhan | 30 / 30 |
| Demo | Nhom | 4 / 5 |
| **Tong** | | **83 / 100** |

