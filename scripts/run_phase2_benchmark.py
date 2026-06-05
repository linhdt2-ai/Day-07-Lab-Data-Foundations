from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src import Document, EmbeddingStore, FixedSizeChunker, RecursiveChunker, SentenceChunker


DATA_DIR = ROOT_DIR / "data"
REPORT_DIR = ROOT_DIR / "report"
REPORT_PATH = REPORT_DIR / "phase2_benchmark_results.md"

TOPIC_BY_FILE = {
    "lich_trinh_buyt.txt": "bus_city",
    "danh_sach_tuyen_buyt.txt": "bus_city",
    "bus_brt_hanoi.txt": "bus_city",
    "metro_hanoi.txt": "metro",
    "quy_dinh_phap_luat.txt": "law_traffic",
    "tai_lieu_phap_ly.txt": "law_education",
}

CATEGORY_BY_FILE = {
    "lich_trinh_buyt.txt": "route_schedule",
    "danh_sach_tuyen_buyt.txt": "route_schedule",
    "bus_brt_hanoi.txt": "route_schedule",
    "metro_hanoi.txt": "route_schedule",
    "quy_dinh_phap_luat.txt": "regulation",
    "tai_lieu_phap_ly.txt": "legal_document",
}

TRANSPORT_TYPE_BY_FILE = {
    "lich_trinh_buyt.txt": "bus",
    "danh_sach_tuyen_buyt.txt": "bus",
    "bus_brt_hanoi.txt": "bus",
    "metro_hanoi.txt": "metro",
}

BENCHMARKS = [
    {
        "id": "Q1",
        "question": "Xe buýt số 7 từ Nội Bài đến Cầu Giấy giá bao nhiêu và mấy giờ?",
        "gold_answer": "Giá 8.000đ, giờ hoạt động 05:00–21:35, tuyến Cầu Giấy – Nội Bài qua Cầu Thăng Long.",
        "expected_files": ["lich_trinh_buyt.txt", "bus_brt_hanoi.txt"],
        "filter": None,
    },
    {
        "id": "Q2",
        "question": "Metro Cát Linh–Hà Đông có bao nhiêu ga và chạy mấy giờ?",
        "gold_answer": "12 ga, hoạt động 05:30–22:30, giờ cao điểm 6 phút/chuyến, toàn tuyến 23 phút.",
        "expected_files": ["metro_hanoi.txt"],
        "filter": {"topic": "metro"},
    },
    {
        "id": "Q3",
        "question": "Quy định về việc ăn uống trên metro Hà Nội?",
        "gold_answer": "Nghiêm cấm ăn uống; mức phạt từ 100.000–300.000đ trong tàu và sân ga.",
        "expected_files": ["quy_dinh_phap_luat.txt"],
        "filter": {"topic": "law_traffic"},
    },
    {
        "id": "Q4",
        "question": "Từ Bến xe Giáp Bát đến Nhổn đi tuyến nào?",
        "gold_answer": "Tuyến 32: Giáp Bát → Kim Mã → Cầu Giấy → Nhổn.",
        "expected_files": ["lich_trinh_buyt.txt", "danh_sach_tuyen_buyt.txt"],
        "filter": {"topic": "bus_city"},
    },
    {
        "id": "Q5",
        "question": "Học bổng khuyến khích học tập loại Khá dành cho sinh viên đại học là bao nhiêu?",
        "gold_answer": "Mức học bổng ≥ mức trần học phí hiện hành, căn cứ Điều 7, Nghị định 66/2026.",
        "expected_files": ["tai_lieu_phap_ly.txt"],
        "filter": {"topic": "law_education"},
    },
]


def load_source_documents() -> tuple[list[Document], list[str], list[str]]:
    docs: list[Document] = []
    used_files: list[str] = []
    skipped_files: list[str] = []

    for path in sorted(DATA_DIR.iterdir()):
        if not path.is_file():
            continue
        if path.name == "benchmark_queries.md":
            skipped_files.append(path.name)
            continue
        if path.suffix.lower() not in {".txt", ".md"}:
            skipped_files.append(path.name)
            continue
        if path.name not in TOPIC_BY_FILE:
            skipped_files.append(path.name)
            continue

        content = path.read_text(encoding="utf-8").strip()
        if not content:
            skipped_files.append(path.name)
            continue

        metadata = {
            "doc_id": path.stem,
            "source": path.name,
            "topic": TOPIC_BY_FILE[path.name],
            "category": CATEGORY_BY_FILE.get(path.name, "document"),
            "city": "hanoi",
        }
        transport_type = TRANSPORT_TYPE_BY_FILE.get(path.name)
        if transport_type:
            metadata["transport_type"] = transport_type

        docs.append(Document(id=path.stem, content=content, metadata=metadata))
        used_files.append(path.name)

    return docs, used_files, skipped_files


def build_chunk_documents(strategy_name: str, chunker, source_docs: list[Document]) -> list[Document]:
    chunk_docs: list[Document] = []

    for doc in source_docs:
        chunks = chunker.chunk(doc.content)
        for chunk_index, chunk in enumerate(chunks):
            text = chunk.strip()
            if not text:
                continue

            metadata = dict(doc.metadata)
            metadata.update(
                {
                    "strategy": strategy_name,
                    "chunk_index": chunk_index,
                }
            )
            chunk_docs.append(
                Document(
                    id=f"{doc.id}_chunk_{chunk_index}",
                    content=text,
                    metadata=metadata,
                )
            )

    return chunk_docs


def preview_text(text: str, limit: int = 400) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[:limit].rstrip() + "..."


def format_filter(metadata_filter: dict | None) -> str:
    if not metadata_filter:
        return "Khong"
    return ", ".join(f"{key}={value}" for key, value in metadata_filter.items())


def evaluate_strategy(strategy_name: str, chunker, source_docs: list[Document]) -> tuple[dict, int]:
    chunk_docs = build_chunk_documents(strategy_name, chunker, source_docs)
    store = EmbeddingStore(collection_name=f"phase2_{strategy_name}")
    store.add_documents(chunk_docs)

    strategy_results = {"name": strategy_name, "queries": []}
    for benchmark in BENCHMARKS:
        metadata_filter = benchmark["filter"]
        if metadata_filter:
            results = store.search_with_filter(benchmark["question"], top_k=3, metadata_filter=metadata_filter)
        else:
            results = store.search(benchmark["question"], top_k=3)

        expected_hit = any(
            result.get("metadata", {}).get("source") in benchmark["expected_files"]
            for result in results
        )

        top_source = results[0].get("metadata", {}).get("source", "-") if results else "-"
        top_score = results[0].get("score", 0.0) if results else 0.0

        strategy_results["queries"].append(
            {
                "benchmark": benchmark,
                "results": results,
                "expected_hit": expected_hit,
                "top_source": top_source,
                "top_score": top_score,
            }
        )

    return strategy_results, len(chunk_docs)


def build_report(
    used_files: list[str],
    skipped_files: list[str],
    strategy_outputs: list[dict],
) -> str:
    lines = ["# Phase 2 Benchmark Results", "", "## Dataset", "", "Danh sach file da dung:"]
    for name in used_files:
        lines.append(f"- {name}")

    lines.extend(["", "File bi bo qua:"])
    for name in skipped_files:
        lines.append(f"- {name}")

    for strategy_output in strategy_outputs:
        lines.extend(["", f"## Strategy: {strategy_output['name']}"])
        for query_result in strategy_output["queries"]:
            benchmark = query_result["benchmark"]
            lines.extend(
                [
                    "",
                    f"### {benchmark['id']}",
                    f"Question: {benchmark['question']}",
                    f"Gold Answer: {benchmark['gold_answer']}",
                    f"Filter: {format_filter(benchmark['filter'])}",
                    "",
                ]
            )

            results = query_result["results"]
            if not results:
                lines.append("Khong co ket qua.")
            else:
                for index, result in enumerate(results, start=1):
                    metadata = result.get("metadata", {})
                    lines.extend(
                        [
                            f"Top {index}:",
                            f"- Score: {result.get('score', 0.0):.4f}",
                            f"- Source: {metadata.get('source', '-')}",
                            f"- Metadata: {metadata}",
                            f"- Preview: {preview_text(result.get('content') or result.get('text') or '')}",
                            "",
                        ]
                    )

            hit_text = "Yes" if query_result["expected_hit"] else "No"
            lines.extend(
                [
                    "Nhan xet:",
                    f"- Expected file hit in Top-3: {hit_text}",
                    f"- Expected files: {', '.join(benchmark['expected_files'])}",
                ]
            )

    lines.extend(
        [
            "",
            "# Summary Table",
            "",
            "| Query ID | Strategy | Top-1 Source | Top-1 Score | Expected file hit in Top-3? | Nhan xet |",
            "|---|---|---|---:|---|---|",
        ]
    )

    for strategy_output in strategy_outputs:
        for query_result in strategy_output["queries"]:
            benchmark = query_result["benchmark"]
            hit_text = "Yes" if query_result["expected_hit"] else "No"
            note = "Matched expected source" if query_result["expected_hit"] else "No expected source in top-3"
            lines.append(
                f"| {benchmark['id']} | {strategy_output['name']} | {query_result['top_source']} | "
                f"{query_result['top_score']:.4f} | {hit_text} | {note} |"
            )

    return "\n".join(lines) + "\n"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    source_docs, used_files, skipped_files = load_source_documents()
    strategies = {
        "fixed_size": FixedSizeChunker(chunk_size=500, overlap=50),
        "sentence": SentenceChunker(max_sentences_per_chunk=5),
        "recursive": RecursiveChunker(chunk_size=500),
    }

    print(f"Loaded {len(used_files)} data files for benchmarking.")

    strategy_outputs = []
    for strategy_name, chunker in strategies.items():
        strategy_output, chunk_count = evaluate_strategy(strategy_name, chunker, source_docs)
        strategy_outputs.append(strategy_output)
        print(f"{strategy_name}: {chunk_count} chunks")

    report_content = build_report(used_files, skipped_files, strategy_outputs)
    REPORT_PATH.write_text(report_content, encoding="utf-8")
    print(f"Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
