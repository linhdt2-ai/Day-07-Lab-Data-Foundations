import os
from pathlib import Path
from src.chunking import ChunkingStrategyComparator

DATA_DIR = Path("data")

def get_inventory():
    print("=== Section 2: Data Inventory ===")
    files = sorted([f for f in DATA_DIR.iterdir() if f.suffix in ['.txt', '.md']])
    
    metadata_map = {
        "chunking_experiment_report.md": {"category": "experiment", "difficulty": "intermediate"},
        "customer_support_playbook.txt": {"category": "support", "difficulty": "easy"},
        "python_intro.txt": {"category": "programming", "difficulty": "easy"},
        "rag_system_design.md": {"category": "architecture", "difficulty": "hard"},
        "vector_store_notes.md": {"category": "database", "difficulty": "intermediate"},
        "vi_retrieval_notes.md": {"category": "nlp", "difficulty": "intermediate"},
    }

    print(f"| # | Document Name | Source | Char Count | Metadata |")
    print(f"|---|---|---|---|---|")
    for i, file_path in enumerate(files, start=1):
        content = file_path.read_text(encoding="utf-8")
        char_count = len(content)
        meta = metadata_map.get(file_path.name, {"category": "general", "difficulty": "easy"})
        meta_str = f"category: {meta['category']}, difficulty: {meta['difficulty']}"
        print(f"| {i} | {file_path.name} | Local data | {char_count} | {meta_str} |")
    print("\n")

def run_comparison():
    print("=== Section 3: Baseline Analysis ===")
    target_files = ["python_intro.txt", "rag_system_design.md", "customer_support_playbook.txt"]
    comparator = ChunkingStrategyComparator()
    
    for file_name in target_files:
        file_path = DATA_DIR / file_name
        if not file_path.exists():
            continue
        text = file_path.read_text(encoding="utf-8")
        print(f"Document: {file_name}")
        print(f"| Strategy | Chunk Count | Avg Length | Preserves Context? |")
        print(f"|---|---|---|---|")
        
        result = comparator.compare(text, chunk_size=200)
        
        # FixedSizeChunker
        fixed = result["fixed_size"]
        print(f"| FixedSizeChunker | {fixed['count']} | {fixed['avg_length']:.1f} | No (word-cutting) |")
        
        # SentenceChunker
        by_sentences = result["by_sentences"]
        print(f"| SentenceChunker | {by_sentences['count']} | {by_sentences['avg_length']:.1f} | Yes (sentence-preserving) |")
        
        # RecursiveChunker
        recursive = result["recursive"]
        print(f"| RecursiveChunker | {recursive['count']} | {recursive['avg_length']:.1f} | Yes (layout-preserving) |")
        print("\n")

if __name__ == "__main__":
    get_inventory()
    run_comparison()
