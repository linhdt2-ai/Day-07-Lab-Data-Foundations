from __future__ import annotations

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
            import chromadb

            self._client = chromadb.Client()
            try:
                self._client.delete_collection(name=self._collection_name)
            except Exception:
                pass
            self._collection = self._client.get_or_create_collection(name=self._collection_name)
            self._use_chroma = True
        except Exception:
            self._use_chroma = False
            self._collection = None

    def _make_record(self, doc: Document) -> dict[str, Any]:
        metadata = dict(doc.metadata) if doc.metadata else {}
        metadata["doc_id"] = doc.id
        embedding = self._embedding_fn(doc.content)
        rec_id = f"{doc.id}_{self._next_index}"
        self._next_index += 1
        return {
            "id": rec_id,
            "content": doc.content,
            "embedding": embedding,
            "metadata": metadata,
        }

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        query_emb = self._embedding_fn(query)
        results = []
        for r in records:
            score = _dot(query_emb, r["embedding"])
            results.append({
                "id": r["id"],
                "content": r["content"],
                "metadata": r["metadata"],
                "score": score
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def add_documents(self, docs: list[Document]) -> None:
        """
        Embed each document's content and store it.

        For ChromaDB: use collection.add(ids=[...], documents=[...], embeddings=[...])
        For in-memory: append dicts to self._store
        """
        if self._use_chroma:
            ids = []
            documents = []
            embeddings = []
            metadatas = []
            for doc in docs:
                record = self._make_record(doc)
                ids.append(record["id"])
                documents.append(record["content"])
                embeddings.append(record["embedding"])
                metadatas.append(record["metadata"])
            self._collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
        else:
            for doc in docs:
                self._store.append(self._make_record(doc))

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Find the top_k most similar documents to query.

        For in-memory: compute dot product of query embedding vs all stored embeddings.
        """
        if self._use_chroma:
            query_emb = self._embedding_fn(query)
            results = self._collection.query(
                query_embeddings=[query_emb],
                n_results=top_k,
                include=["embeddings", "documents", "metadatas"]
            )
            formatted = []
            if results and results.get("ids") and results["ids"][0]:
                ids = results["ids"][0]
                docs = results["documents"][0]
                metadatas = results["metadatas"][0]
                embeddings = results["embeddings"][0]
                for idx, doc_text, meta, emb in zip(ids, docs, metadatas, embeddings):
                    formatted.append({
                        "id": idx,
                        "content": doc_text,
                        "metadata": meta,
                        "score": _dot(query_emb, emb)
                    })
                formatted.sort(key=lambda x: x["score"], reverse=True)
            return formatted
        else:
            return self._search_records(query, self._store, top_k)

    def get_collection_size(self) -> int:
        """Return the total number of stored chunks."""
        if self._use_chroma:
            return self._collection.count()
        else:
            return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        """
        Search with optional metadata pre-filtering.

        First filter stored chunks by metadata_filter, then run similarity search.
        """
        if self._use_chroma:
            query_emb = self._embedding_fn(query)
            where_clause = None
            if metadata_filter:
                if len(metadata_filter) == 1:
                    where_clause = metadata_filter
                elif len(metadata_filter) > 1:
                    where_clause = {"$and": [{k: v} for k, v in metadata_filter.items()]}
            
            results = self._collection.query(
                query_embeddings=[query_emb],
                n_results=top_k,
                where=where_clause,
                include=["embeddings", "documents", "metadatas"]
            )
            formatted = []
            if results and results.get("ids") and results["ids"][0]:
                ids = results["ids"][0]
                docs = results["documents"][0]
                metadatas = results["metadatas"][0]
                embeddings = results["embeddings"][0]
                for idx, doc_text, meta, emb in zip(ids, docs, metadatas, embeddings):
                    formatted.append({
                        "id": idx,
                        "content": doc_text,
                        "metadata": meta,
                        "score": _dot(query_emb, emb)
                    })
                formatted.sort(key=lambda x: x["score"], reverse=True)
            return formatted
        else:
            if not metadata_filter:
                filtered_records = self._store
            else:
                filtered_records = []
                for r in self._store:
                    meta = r["metadata"]
                    match = True
                    for k, v in metadata_filter.items():
                        if meta.get(k) != v:
                            match = False
                            break
                    if match:
                        filtered_records.append(r)
            return self._search_records(query, filtered_records, top_k)

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove all chunks belonging to a document.

        Returns True if any chunks were removed, False otherwise.
        """
        if self._use_chroma:
            count_before = self._collection.count()
            self._collection.delete(where={"doc_id": doc_id})
            return self._collection.count() < count_before
        else:
            initial_size = len(self._store)
            self._store = [r for r in self._store if r["metadata"].get("doc_id") != doc_id]
            return len(self._store) < initial_size
