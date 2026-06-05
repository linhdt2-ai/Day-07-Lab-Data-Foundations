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
        retrieved = self.store.search(question, top_k=top_k)
        context = []
        for index, item in enumerate(retrieved, start=1):
            content = item.get("content", "")
            metadata = item.get("metadata", {})
            source = metadata.get("source")
            context.append(f"[{index}] {content}" + (f" (source={source})" if source else ""))

        prompt = (
            "Use the retrieved context to answer the question.\n\n"
            "Context:\n"
            + "\n\n".join(context)
            + "\n\nQuestion: "
            + question
            + "\nAnswer:"
        )
        response = self.llm_fn(prompt)
        return response if isinstance(response, str) else str(response)
