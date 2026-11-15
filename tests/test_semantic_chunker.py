"""Offline tests for SemanticChunker using a deterministic fake embedder."""

from rag.Chunking.semantic_chunker import SemanticChunker


class FakeEmbedder:
    """Maps sentences to unit vectors by topic word so that sentences about
    the same topic are identical (distance 0) and different topics are
    orthogonal (distance 1)."""

    def embed_documents(self, chunks):
        return [self._vec(c["text"]) for c in chunks]

    def embed_query(self, query):
        return self._vec(query)

    @staticmethod
    def _vec(text):
        if text.startswith("Alpha"):
            return [1.0, 0.0]
        return [0.0, 1.0]


def make_chunker():
    return SemanticChunker(embedder=FakeEmbedder(), threshold_percentile=95)


def test_split_into_sentences_basic():
    chunker = make_chunker()
    sentences = chunker._split_into_sentences(
        "First sentence. Second sentence! Is this third? Yes it is."
    )
    assert sentences == ["First sentence.", "Second sentence!",
                         "Is this third?", "Yes it is."]


def test_single_topic_document_stays_one_chunk():
    chunker = make_chunker()
    chunks = chunker.chunk(["Alpha one. Alpha two. Alpha three."])
    assert len(chunks) == 1
    assert chunks[0]["text"] == "Alpha one. Alpha two. Alpha three."


def test_topic_change_creates_breakpoint():
    chunker = make_chunker()
    doc = "Alpha one. Alpha two. Beta one. Beta two."
    chunks = chunker.chunk([doc])
    assert len(chunks) == 2
    assert chunks[0]["text"] == "Alpha one. Alpha two."
    assert chunks[1]["text"] == "Beta one. Beta two."


def test_chunk_ids_are_sequential_across_documents():
    chunker = make_chunker()
    chunks = chunker.chunk(["Alpha only here.", "Beta only here."])
    assert [c["id"] for c in chunks] == [1, 2]


def test_empty_documents_return_no_chunks():
    chunker = make_chunker()
    assert chunker.chunk([]) == []
    assert chunker.chunk([""]) == []
