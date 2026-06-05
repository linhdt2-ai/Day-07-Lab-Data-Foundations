# Workflow Lab 7: Embedding & Vector Store

Workflow lab hiện tại là một pipeline RAG mini:

```text
Raw data files
      |
      v
Load documents from data/hanoi
      |
      v
Chunk documents
      |
      v
Embed each chunk
      |
      v
Store chunks + embeddings + metadata
      |
      v
User query / benchmark query
      |
      v
Embed query
      |
      v
Similarity search
      |
      v
Top-k retrieved chunks
      |
      v
Agent builds prompt from chunks
      |
      v
LLM / answer / evaluation
```

## 1. So Do Tong Quan

```text
+-------------------------+
| data/hanoi/*.txt        |
| bus, metro, legal docs  |
+-----------+-------------+
            |
            v
+-------------------------+
| Load Document objects   |
| id, content, metadata   |
+-----------+-------------+
            |
            v
+-------------------------+
| RecursiveChunker        |
| chunk_size = 2500       |
| 7 files -> 74 chunks    |
+-----------+-------------+
            |
            v
+-------------------------+
| Embedding Function      |
| mock OR Gemini          |
+-----------+-------------+
            |
            v
+-------------------------+
| EmbeddingStore          |
| content                 |
| metadata                |
| embedding vector        |
+-----------+-------------+
            |
            v
+-------------------------+
| Query from benchmark    |
| 5 group questions       |
+-----------+-------------+
            |
            v
+-------------------------+
| Query embedding         |
+-----------+-------------+
            |
            v
+-------------------------+
| Similarity search       |
| dot product ranking     |
+-----------+-------------+
            |
            v
+-------------------------+
| Top-3 chunks            |
| score + source + chunk  |
+-----------+-------------+
            |
            v
+-------------------------+
| Compare with gold answer|
| Relevant? Yes/No        |
+-------------------------+
```

## 2. Load Data

Data nam trong:

```text
data/hanoi/
```

Gom 7 file:

```text
bus_brt_hanoi.txt
buyt_online_hanoi.txt
danh_sach_tuyen_buyt.txt
lich_trinh_buyt.txt
metro_hanoi.txt
quy_dinh_phap_luat.txt
tai_lieu_phap_ly.txt
```

Moi file duoc doc thanh noi dung text. Sau do code tao cac `Document`.

Mot `Document` co dang logic:

```python
Document(
    id="metro_hanoi-0",
    content="noi dung chunk...",
    metadata={
        "doc_id": "metro_hanoi",
        "source": "data/hanoi/metro_hanoi.txt",
        "chunk_index": 0,
        "category": "hanoi_transport",
    }
)
```

## 3. Chunking

Tai lieu dai khong nen embed nguyen file vi:

- File qua dai.
- De bi loang ngu canh.
- Search co the tra ve dung file nhung sai doan.

Nen minh dung:

```python
RecursiveChunker(chunk_size=2500)
```

No chia tai lieu theo thu tu uu tien:

```text
doan van -> dong -> cau -> tu -> ky tu
```

Trong data Ha Noi:

```text
7 files -> 74 chunks
```

## 4. Embedding

Sau khi co chunks, moi chunk duoc chuyen thanh vector.

Minh co 2 huong:

```text
_mock_embed
```

Dung cho test, on dinh, khong can API key, nhung khong hieu ngu nghia that.

```text
GeminiEmbedder
```

Dung `gemini-embedding-2`, hieu ngu nghia tot hon, dung cho benchmark thuc te.

So sanh:

```text
Mock baseline: 2 / 5 relevant top-3
Gemini:        5 / 5 relevant top-3
```

## 5. Store

`EmbeddingStore` luu moi chunk thanh record:

```text
id
content
metadata
embedding
```

Khi goi:

```python
store.add_documents(docs)
```

No embed tung chunk roi luu vao memory.

## 6. Search

Khi co query, vi du:

```text
Metro Cat Linh-Ha Dong co bao nhieu ga va chay may gio?
```

Workflow search la:

```text
query -> embedding vector
query vector so voi chunk vectors
sort theo score giam dan
tra top_k chunks
```

Trong code, similarity hien dung dot product. Vi Gemini vector duoc normalize trong script, dot product luc nay tuong duong gan voi cosine similarity.

## 7. Evaluation

Nhom co 5 query + gold answer.

Vi du:

```text
Query:
Metro Cat Linh-Ha Dong co bao nhieu ga va chay may gio?

Gold Answer:
12 ga, hoat dong 05:30-22:30, gio cao diem 6 phut/chuyen, toan tuyen 23 phut
```

Khi search, minh xem top-3 co chunk lien quan khong.

Ket qua Gemini:

```text
5 / 5 query co relevant chunk trong top-3
```

## 8. Agent

`KnowledgeBaseAgent` la buoc RAG cuoi cung.

No lam:

```text
question
  -> store.search(question, top_k=3)
  -> lay context chunks
  -> build prompt
  -> goi llm_fn(prompt)
  -> tra answer
```

Prompt dang logic:

```text
Answer the user's question using only the retrieved context.

Retrieved context:
[Context 1] source=...
...
Question: ...
Answer:
```

## 9. Tom Tat Cuc Ngan

```text
Data Ha Noi
-> chia nho bang RecursiveChunker
-> embed bang Gemini
-> luu vao EmbeddingStore
-> embed query
-> search top-3 chunks gan nhat
-> so voi gold answer
-> ket qua 5/5 relevant top-3
```

Diem cot loi cua lab la chung minh minh hieu: retrieval quality phu thuoc vao ca data, chunking, metadata, embedding model va cach danh gia bang benchmark queries, khong chi la code chay duoc.
