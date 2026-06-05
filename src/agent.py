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
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        results = self.store.search(question, top_k=top_k)

        context_parts = []
        for index, result in enumerate(results, start=1):
            content = result.get("content") or result.get("text")

            if content is None and "document" in result:
                document = result["document"]
                content = getattr(document, "content", None) or getattr(document, "text", None)

            if content:
                context_parts.append(f"[{index}] {content}")

        context = "\n\n".join(context_parts)
        if not context:
            context = "No relevant context was found in the knowledge base."

        prompt = (
            "Use the following context to answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )

        response = self.llm_fn(prompt)
        if not isinstance(response, str) or not response.strip():
            return "I could not generate an answer from the retrieved context."

        return response.strip()
