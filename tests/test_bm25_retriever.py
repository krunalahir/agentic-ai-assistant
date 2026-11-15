"""Offline tests for the keyword (BM25) retriever.

Uses the real rank_bm25 package (pure Python, no network).
"""

from rag.Retriever.bm25_retriever import BM25Retriever

CHUNKS = [
    {"id": 1, "text": "Paris is the capital of France"},
    {"id": 2, "text": "The Eiffel Tower is located in Paris"},
    {"id": 3, "text": "Berlin is the capital of Germany"},
]


def test_keyword_query_ranks_matching_chunk_first():
    retriever = BM25Retriever(CHUNKS)
    results = retriever.retrieve("capital Germany", k=1)
    assert results[0]["id"] == 3


def test_retrieve_respects_k():
    retriever = BM25Retriever(CHUNKS)
    assert len(retriever.retrieve("Paris", k=2)) == 2


def test_retrieve_returns_chunk_dicts():
    retriever = BM25Retriever(CHUNKS)
    for chunk in retriever.retrieve("Eiffel Tower", k=3):
        assert "id" in chunk and "text" in chunk
