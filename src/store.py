from __future__ import annotations

import math
from typing import Any, Callable

from .chunking import _dot
from .embeddings import _mock_embed
from .models import Document


class EmbeddingStore:
    """
    A vector store for text chunks.

    Tries to use ChromaDB if available; falls back to an in-memory store.
    The embedding_fn parameter allows injection of mock embeddings for tests.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        embedding_fn: Callable[[str], list[float]] | None = None,
    ) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._collection = None
        self._next_index = 0

        try:
            import chromadb  # noqa: F401
            from chromadb.config import Settings

            client = chromadb.Client(Settings())
            self._collection = client.create_collection(name=self._collection_name)
            self._use_chroma = True
        except Exception:
            self._use_chroma = False
            self._collection = None

    def _make_record(self, doc: Document) -> dict[str, Any]:
        embedding = self._embedding_fn(doc.content)
        return {
            "id": doc.id,
            "content": doc.content,
            "metadata": {**doc.metadata, "doc_id": doc.id},
            "embedding": embedding,
        }

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        query_embedding = self._embedding_fn(query)
        scored = []
        for record in records:
            embedding = record.get("embedding")
            if embedding is None:
                continue
            score = _dot(query_embedding, embedding)
            if not math.isfinite(score):
                score = 0.0
            scored.append({**record, "score": score})

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def add_documents(self, docs: list[Document]) -> None:
        """
        Embed each document's content and store it.

        For ChromaDB: use collection.add(ids=[...], documents=[...], embeddings=[...])
        For in-memory: append dicts to self._store
        """
        records = [self._make_record(doc) for doc in docs]

        if self._use_chroma and self._collection is not None:
            ids = [record["id"] for record in records]
            documents = [record["content"] for record in records]
            embeddings = [record["embedding"] for record in records]
            metadatas = [record["metadata"] for record in records]
            try:
                self._collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
            except Exception:
                self._use_chroma = False
                self._collection = None
                self._store.extend(records)
        else:
            self._store.extend(records)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Find the top_k most similar documents to query.

        For in-memory: compute dot product of query embedding vs all stored embeddings.
        """
        if self._use_chroma and self._collection is not None:
            try:
                query_embedding = self._embedding_fn(query)
                results = self._collection.query(query_embeddings=[query_embedding], n_results=top_k)
                output = []
                for i, content in enumerate(results.get("documents", [[]])[0] if isinstance(results.get("documents", []), list) else []):
                    metadata = results.get("metadatas", [[]])[0][i] if results.get("metadatas") else {}
                    score = results.get("distances", [[]])[0][i] if results.get("distances") else 0.0
                    output.append({"content": content, "metadata": metadata, "score": score})
                return output
            except Exception:
                self._use_chroma = False
                self._collection = None

        return self._search_records(query=query, records=self._store, top_k=top_k)

    def get_collection_size(self) -> int:
        """Return the total number of stored chunks."""
        if self._use_chroma and self._collection is not None:
            try:
                return self._collection.count()
            except Exception:
                return len(self._store)
        return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        """
        Search with optional metadata pre-filtering.

        First filter stored chunks by metadata_filter, then run similarity search.
        """
        if metadata_filter is None:
            return self.search(query, top_k=top_k)

        filtered = [
            record
            for record in self._store
            if all(record.get("metadata", {}).get(key) == value for key, value in metadata_filter.items())
        ]
        return self._search_records(query=query, records=filtered, top_k=top_k)

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove all chunks belonging to a document.

        Returns True if any chunks were removed, False otherwise.
        """
        original_len = len(self._store)
        self._store = [record for record in self._store if record.get("metadata", {}).get("doc_id") != doc_id]
        return len(self._store) < original_len
