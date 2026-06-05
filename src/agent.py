from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store   = store
        self.llm_fn  = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        # Bước 1: retrieve top-k chunks liên quan
        results = self.store.search(question, top_k=top_k)

        # Bước 2: build context string
        context_lines = [f"[{i + 1}] {r['content']}" for i, r in enumerate(results)]
        context = "\n".join(context_lines)

        # Bước 3: build prompt và gọi LLM
        prompt = (
            "You are a helpful assistant. Answer the question using ONLY the context below.\n"
            "If the context does not contain the answer, say \"I don't know.\"\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            "Answer:"
        )
        return self.llm_fn(prompt)
