from pathlib import Path
from src.chunking import FixedSizeChunker, SentenceChunker, RecursiveChunker, HanoiTransitChunker

DATA_DIR = Path("data")

def main():
    files = ["metro_hanoi.txt", "bus_brt_hanoi.txt"]
    for file_name in files:
        file_path = DATA_DIR / file_name
        if not file_path.exists():
            print(f"File {file_name} does not exist!")
            continue
        text = file_path.read_text(encoding="utf-8")
        print(f"=== File: {file_name} (Length: {len(text)} chars) ===")
        
        # Instantiate chunkers
        fixed = FixedSizeChunker(chunk_size=500, overlap=50)
        sentence = SentenceChunker(max_sentences_per_chunk=3)
        recursive = RecursiveChunker(chunk_size=500)
        custom = HanoiTransitChunker(chunk_size=500)
        
        for name, chunker in [
            ("FixedSizeChunker", fixed),
            ("SentenceChunker", sentence),
            ("RecursiveChunker", recursive),
            ("HanoiTransitChunker (Custom)", custom)
        ]:
            chunks = chunker.chunk(text)
            count = len(chunks)
            avg_len = sum(len(c) for c in chunks) / count if count > 0 else 0
            print(f"  {name:30} | Chunks: {count:2} | Avg Len: {avg_len:5.1f}")
        print()

if __name__ == "__main__":
    main()
