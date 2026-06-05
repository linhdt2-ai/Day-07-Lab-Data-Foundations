from pathlib import Path
import sys

from src import Document, EmbeddingStore, RecursiveChunker, _mock_embed


DATA_DIR = Path("data")

BENCHMARK_QUERIES = [
    {
        "id": "Q1",
        "query": "Xe buyt so 7 tu Noi Bai den Cau Giay gia bao nhieu va may gio?",
        "gold_answer": "Gia 8.000d, gio hoat dong 05:00-21:35, tuyen Cau Giay - Noi Bai qua cau Thang Long.",
        "metadata_filter": None,
    },
    {
        "id": "Q2",
        "query": "Metro Cat Linh - Ha Dong co bao nhieu ga va chay may gio?",
        "gold_answer": "12 ga, hoat dong 05:30-22:30, gio cao diem 6 phut/chuyen, toan tuyen 23 phut.",
        "metadata_filter": {"topic": "metro"},
    },
    {
        "id": "Q3",
        "query": "Quy dinh ve viec an uong tren metro Ha Noi?",
        "gold_answer": "Nghiem cam an uong; muc phat tu 100.000-300.000d trong tau va san ga.",
        "metadata_filter": {"topic": "law_traffic"},
    },
    {
        "id": "Q4",
        "query": "Tu Ben xe Giap Bat den Nhon di tuyen nao?",
        "gold_answer": "Tuyen 32: Giap Bat -> Kim Ma -> Cau Giay -> Nhon.",
        "metadata_filter": {"topic": "bus_city"},
    },
    {
        "id": "Q5",
        "query": "Hoc bong khuyen khich hoc tap loai Kha danh cho sinh vien dai hoc la bao nhieu?",
        "gold_answer": "Muc hoc bong >= muc tran hoc phi hien hanh cua nganh.",
        "metadata_filter": {"topic": "law_education"},
    },
]

FILES = [
    ("lich_trinh_buyt.txt", "bus_city"),
    ("bus_brt_hanoi.txt", "bus_city"),
    ("metro_hanoi.txt", "metro"),
    ("quy_dinh_phap_luat.txt", "law_traffic"),
    ("danh_sach_tuyen_buyt.txt", "bus_city"),
    ("tai_lieu_phap_ly.txt", "law_education"),
]


def load_chunked_documents() -> list[Document]:
    chunker = RecursiveChunker(chunk_size=300)
    docs: list[Document] = []

    for filename, topic in FILES:
        path = DATA_DIR / filename
        if not path.exists():
            print(f"Missing file: {path}")
            continue

        text = path.read_text(encoding="utf-8")
        chunks = chunker.chunk(text)
        for index, chunk in enumerate(chunks):
            docs.append(
                Document(
                    id=f"{path.stem}_{index}",
                    content=chunk,
                    metadata={
                        "source": filename,
                        "topic": topic,
                        "chunk_index": index,
                        "strategy": "recursive_300",
                    },
                )
            )

    return docs


def demo_llm(prompt: str) -> str:
    context = prompt.split("Context:", maxsplit=1)[-1].split("Question:", maxsplit=1)[0]
    return "Based on retrieved context: " + " ".join(context.split())[:220]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    docs = load_chunked_documents()
    store = EmbeddingStore(collection_name="group_benchmark", embedding_fn=_mock_embed)
    store.add_documents(docs)

    print(f"Loaded chunks: {store.get_collection_size()}")
    print("Strategy: RecursiveChunker(chunk_size=300)")
    print()

    for item in BENCHMARK_QUERIES:
        query_id = item["id"]
        query = item["query"]
        metadata_filter = item["metadata_filter"]

        if metadata_filter:
            results = store.search_with_filter(query, top_k=3, metadata_filter=metadata_filter)
        else:
            results = store.search(query, top_k=3)

        print("=" * 80)
        print(f"{query_id}: {query}")
        print(f"Gold answer: {item['gold_answer']}")
        print(f"Filter: {metadata_filter or 'None'}")
        print()

        for rank, result in enumerate(results, start=1):
            preview = " ".join(result["content"].split())[:220]
            source = result["metadata"].get("source")
            chunk_index = result["metadata"].get("chunk_index")
            score = result["score"]
            print(f"Top {rank}: score={score:.3f} source={source} chunk={chunk_index}")
            print(f"Preview: {preview}")
            print()

        context = "\n\n".join(result["content"] for result in results)
        answer = demo_llm(
            "Use the following context to answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{query}\n\n"
            "Answer:"
        )
        print(f"Agent answer preview: {answer}")
        print()


if __name__ == "__main__":
    main()
