from src.embeddings import _mock_embed, LocalEmbedder, OpenAIEmbedder
from src.chunking import compute_similarity
import os

# Define 5 pairs of sentences to test
pairs = [
    (
        "The quick brown fox jumps over the lazy dog.",
        "A swift brown fox leaps over a sleepy dog."
    ),
    (
        "Quantum computing represents a major leap in computational power.",
        "Entangled qubits can perform calculations much faster than classical bits."
    ),
    (
        "I love cooking fresh Italian pasta on Sunday evenings.",
        "Deep learning models require massive datasets and GPUs to train."
    ),
    (
        "Artificial intelligence will transform the future of education.",
        "AI is going to revolutionize how students learn and teachers teach."
    ),
    (
        "We need to filter data before storing it in the collection.",
        "Pre-filtering metadata ensures that the vector store queries are fast and relevant."
    )
]

def run_test(embedder, label):
    print(f"=== Testing Cosine Similarity with {label} ===")
    print(f"Backend name: {getattr(embedder, '_backend_name', embedder.__class__.__name__)}\n")
    
    for i, (a, b) in enumerate(pairs, start=1):
        vec_a = embedder(a)
        vec_b = embedder(b)
        score = compute_similarity(vec_a, vec_b)
        print(f"Pair {i}:")
        print(f"  Sentence A: \"{a}\"")
        print(f"  Sentence B: \"{b}\"")
        print(f"  Similarity Score: {score:.4f}")
        print()

def main():
    # 1. Run with Mock Embedder
    run_test(_mock_embed, "Mock Embedder (Fallback)")
    
    # 2. Try to run with Local Embedder (sentence-transformers)
    try:
        import sentence_transformers
        local_embedder = LocalEmbedder()
        run_test(local_embedder, "Local Semantic Embedder (all-MiniLM-L6-v2)")
    except ImportError:
        print("=== Local Embedder (sentence-transformers) is not installed ===")
        print("To test with a real local embedding model, run:")
        print("  pip install sentence-transformers")
        print()

if __name__ == "__main__":
    main()
